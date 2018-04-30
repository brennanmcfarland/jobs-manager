from jmjob import JMJob
from sortedcontainers import SortedListWithKey
import psutil as ps
import time
import threading
import sys
import datetime


cores = ps.cpu_count()
queueLock = threading.Lock() # a semaphore for the lock queue
queuedjobs = SortedListWithKey(key=lambda job: job.nice) # sorted by nice value
runningLock = threading.Lock() # a semaphore for the lock list of running jobs
runningjobs = [None]*cores
newid = 0


def add_job(command, parsed_command, priority):
    global newid
    newjob = JMJob(newid, command, parsed_command, priority)
    queueLock.acquire()
    queuedjobs.add(newjob)
    queueLock.release()
    newid += 1
    print("added job ", parsed_command)


# NOTE: python doesn't really give us a good way to display the CPU time of processes, so we just
# show the overall load of each core instead
def list_jobs():
    print("CPU core usage: ", *[str(percent)+"%" for percent in ps.cpu_percent(.2, True)], sep='\n')
    print("ID   PID  STAT    NAME                  TIME")
    queueLock.acquire()
    for job in queuedjobs:
        list_job(job, "Q")
    queueLock.release()
    runningLock.acquire()
    sys.stdout.flush()
    for job in runningjobs:
        list_job(job, "R")
    runningLock.release()
    print("------------")
    sys.stdout.flush()


def list_job(job, status):
    if job is not None:
        print(job.id, " ", job.pid, " ", status, " ", job.command, " ", datetime.datetime.now()-job.start_time)


def readd_job(job):
    job.nice -= 1
    queueLock.acquire()
    queuedjobs.add(job)
    queueLock.release()
    print("re-added job ", job.parsed_command)


def start_next_job():
    queueLock.acquire()
    try:
        #print("start_next_job waiting for lock... ")
        next_job = queuedjobs.pop()
        next_job.start()
        print("started job ", next_job.id)
    except IndexError:
        next_job = None
    finally: queueLock.release()
    return next_job


# job can be either name or id
def kill_job(job_identifier):
    runningLock.acquire()
    if kill_running_job(job_identifier) is None and kill_queued_job(job_identifier) is None:
        print(job_identifier, " is not a running job")
    else:
        print("killed job ", job_identifier)
    runningLock.release()
    return


# NOTE: in critical section for runningjobs
def kill_running_job(job_identifier):
    for j in range(len(runningjobs)):
        if runningjobs[j] is not None:
            if str(runningjobs[j].id) == job_identifier or job_identifier == runningjobs[j].command:
                runningjobs[j].kill()
                runningjobs[j] = None
                return job_identifier


# NOTE: in critical section for queuedjobs
def kill_queued_job(job_identifier):
    for j in range(len(queuedjobs)):
        if queuedjobs[j] is not None:
            if str(queuedjobs[j].id) == job_identifier or job_identifier == queuedjobs[j].command:
                queuedjobs[j].kill()
                del queuedjobs[j]
                return job_identifier


class JMManager(threading.Thread):

    # thread methods

    def run(self):
        while True:
            self.manage_jobs(quantum=.5)

    # manager methods

    # called every time quantum
    def manage_jobs(self, quantum=.5):
        time.sleep(quantum)
        runningLock.acquire()
        for j in range(len(runningjobs)):
            self.manage_job(j)

        runningLock.release()

    def manage_job(self, j):
        # remove jobs completely if they're finished
        if runningjobs[j] is not None and runningjobs[j].subprocess.poll() is not None:
            runningjobs[j] = None
        # add jobs back to the queue if their CPU time has expired
        if runningjobs[j] is not None and runningjobs[j].nice == 0:
            readd_job(runningjobs[j])
            runningjobs[j] = None
        if runningjobs[j] is None:
            next_job = start_next_job()
            if next_job is None: return
            sys.stdout.flush()
            runningjobs[j] = next_job
        else:
            runningjobs[j].nice -= 1
