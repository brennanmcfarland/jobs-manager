from jmjob import JMJob
from sortedcontainers import SortedList


jobs = []
newid = 0

def add_job(command, parsed_command, priority):
    global newid
    newjob = JMJob(newid, command, parsed_command, priority)
    jobs.append(newjob)
    newid += 1