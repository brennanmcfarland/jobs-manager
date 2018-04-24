from jmjob import JMJob
from sortedcontainers import SortedListWithKey
import psutil as ps
from asyncio.locks import Lock
import time


cores = ps.cpu_count()
queueLock = Lock() # a semaphore for the lock queue
queuedjobs = SortedListWithKey(key=lambda job: job.nice) # sorted by nice value
runningjobs = [None for i in cores]
newid = 0

def add_job(command, parsed_command, priority):
    global newid
    newjob = JMJob(newid, command, parsed_command, priority)
    with (yield from queueLock):
        queuedjobs.add(newjob)
    newid += 1


# called every time quantum
def manage_jobs():
    time.sleep(.5)
    for j in range(len(runningjobs)):
        if runningjobs[j].nice == 0:
            runningjobs[j] = start_next_job()
        else:
            runningjobs[j].nice -= 1


def start_next_job():
    try:
        with (yield from queueLock):
            next_job = queuedjobs.pop()
    except: return None
    next_job.start()
    return next_job
