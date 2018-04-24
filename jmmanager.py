from jmjob import JMJob
from sortedcontainers import SortedListWithKey
import psutil as ps
from asyncio.locks import Lock
import time
import sys


cores = ps.cpu_count()
queueLock = Lock() # a semaphore for the lock queue
queuedjobs = SortedListWithKey(key=lambda job: job.nice) # sorted by nice value
runningLock = Lock() # a semaphore for the lock list of running jobs
runningjobs = [None]*cores
newid = 0

def add_job(command, parsed_command, priority):
    global newid
    newjob = JMJob(newid, command, parsed_command, priority)
    with (yield from queueLock):
        queuedjobs.add(newjob)
    newid += 1


# called every time quantum
def manage_jobs(quantum=.5):
    print("[output of job, list of files for ls]")
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


def start_next_job():
    try:
        with (yield from queueLock):
            next_job = queuedjobs.pop()
    except: return None
    next_job.start()
    return next_job
