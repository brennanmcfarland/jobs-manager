from jmjob import JMJob
from sortedcontainers import SortedListWithKey
import psutil as ps
import time
import threading


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


def start_next_job():
    try:
        queueLock.acquire()
        next_job = queuedjobs.pop()
        queueLock.release()
    except: return None
    next_job.start()
    return next_job


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
        for j in range(len(runningjobs)):
            #print(runningjobs[j])
            if runningjobs[j] is None or runningjobs[j].nice == 0:
                try:
                    queueLock.acquire()
                    runningjobs[j] = queuedjobs.pop()
                    queueLock.release()
                    runningjobs[j].start()
                except:
                    runningjobs[j] = None
                if runningjobs[j] is not None:
                    print(runningjobs[j])
            else:
                if runningjobs[j] is not None:
                    runningjobs[j].nice -= 1
    #     # TODO: add removed jobs back onto the queue with new nice value
