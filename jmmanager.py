from jmjob import JMJob
from sortedcontainers import SortedListWithKey
import psutil as ps
import time
import threading
import sys


cores = ps.cpu_count()
queueLock = threading.Lock() # a semaphore for the lock queue
queuedjobs = SortedListWithKey(key=lambda job: job.nice) # sorted by nice value
runningLock = threading.Lock() # a semaphore for the lock list of running jobs
runningjobs = [None]*cores
newid = 0


def add_job(command, parsed_command, priority):
    global newid
    newjob = JMJob(newid, command, parsed_command, priority)
    print("waiting for lock...")
    queueLock.acquire()
    queuedjobs.add(newjob)
    queueLock.release()
    newid += 1
    print("added job ", parsed_command)
    #list_jobs()


def list_jobs():
    print("CPU core usage: ", *[str(percent)+"%" for percent in ps.cpu_percent(.2, True)], sep='\n')
    print("ID   PID     STAT    NAME    TIME")
    queueLock.acquire()
    for job in queuedjobs:
        list_job(job, "Q")
    queueLock.release()
    print("printed queued jobs")
    runningLock.acquire()
    print("aquired running lock")
    sys.stdout.flush()
    # TODO: it's not printing the running job, but it's still completing if given the time,
    # so it's probably not getting added or re-added to the queue/running job slist properly
    for job in runningjobs:
        list_job(job, "R")
    print(runningjobs)
    runningLock.release()
    print("jobs listed")
    sys.stdout.flush()


def list_job(job, status):
    if job is not None:
        print(job.id, " ", job.pid, " ", status, " ", job.command, " ", "[time]")


def readd_job(job):
    job.nice -= 1
    queueLock.acquire()
    queuedjobs.add(job)
    queueLock.release()
    print("re-added job ", job.parsed_command)


def start_next_job():
    queueLock.acquire()
    try:
        #print("waiting for lock... ")
        next_job = queuedjobs.pop()
        next_job.start()
        print("started job ", next_job.id)
    except: next_job = None
    finally: queueLock.release()
    return next_job

def kill_job(job):
    runningLock.acquire()
    runningjob = job.id
    for j in range(len(runningjobs)):
        if runningjobs[j].id == runningjob.id:
            runningjobs[j].kill()
            print("killed job ", runningjob.id)
            runningLock.release()
    print(job, " is not a running job")
    runningLock.release()
    return None

class JMManager(threading.Thread):

    # thread methods

    def run(self):
        while True:
            self.manage_jobs(quantum=.5)

    # manager methods

    # called every time quantum
    def manage_jobs(self, quantum=.5):
        #print("[output of job, list of files for ls]")
        time.sleep(quantum)
        runningLock.acquire()
        for j in range(len(runningjobs)):
            self.manage_job(j)

        runningLock.release()

    def manage_job(self, j):
        # remove jobs completely if they're finished
        if runningjobs[j] is not None and runningjobs[j].subprocess.poll() is not None:
            runningjobs[j] = None
            print("finished job")
        # add jobs back to the queue if their CPU time has expired
        if runningjobs[j] is not None and runningjobs[j].nice == 0:
            readd_job(runningjobs[j])
            runningjobs[j] = None
            print("job time expired, re-queueing")
        if runningjobs[j] is None:
            next_job = start_next_job()
            if next_job is None: return
            print("about to add job", runningjobs)
            sys.stdout.flush()
            runningjobs[j] = next_job
            print("added job", runningjobs)
        else:
            runningjobs[j].nice -= 1
