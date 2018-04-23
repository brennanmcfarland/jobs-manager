from jmjob import JMJob
from sortedcontainers import SortedListWithKey


jobs = SortedListWithKey()
newid = 0

def add_job(command, parsed_command, priority):
    global newid
    newjob = JMJob(newid, command, parsed_command, priority)
    jobs.add(newjob)
    newid += 1