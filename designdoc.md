NB for Josh: [a reference for markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)
and in case you're wondering, there's lots of ways to convert markdown to pdf easily

# Design Document - Jobs Manager
Brennan McFarland and Joshua Reichman

### Overview
Our project consists of a program to monitor and manage the concurrent execution of other programs via command line.  The idea is that the user can queue up bash commands in an interactive terminal as "jobs" and the manager will then schedule CPU time to run them concurrently or with the appearance of concurrency if there is only one CPU core.  Preference will be given to processes that are queued first, and the user can also assign priority to certain jobs.  The processes will be scheduled in a manner similar to the popular telescope scheduling algorithm.  Additionally, the user can type a command to display the list of jobs and their status in a manner similar to the "top" command and stop running jobs as with "kill".  In a nutshell, the manager function similarly to queuing and viewing the status of batch processes on the HPC cluster.

### Files
TODO: add to/change this as we go
<br>
* __jobsmanager__ &emsp; - &emsp; a bash script to start the application
<br>
* __jm.py__ &emsp; - &emsp; runs the jobs manager application; python execution starts here
<br>
* __jmshell.py__ &emsp; - &emsp; contains the shell specification (a class inheriting from the cmd.Cmd class in the python standard library) that binds commands to program functions
<br>
* __jmmanager.py__ &emsp; - &emsp; handles the jobs themselves, keeping track of them and handling the calls bound by jmshell to create, kill and list new jobs TODO: may need to split this up
<br>
* __jmjob.py__ &emsp; - &emsp; a job and relevant information pertaining to id (ID, PID, etc)
<br>

### Data Structures
TODO: this section
### Usage and Sample Output
* __runjob *bash command*__ &emsp; - &emsp; add a job to the queue
<p>
<br>
\>runjob echo "hello!"<br>
hello!
</p>
* __runjob *priority* *bash command*__ &emsp; - &emsp; adds a job to the queue with the specified priority (an integer), with 1 being the highest priority
<p>
<br>
\>runjob 1 echo "hello!"<br>
hello!
</p>
* __lsjobs__ &emsp; - &emsp; display the list of jobs and their statuses and IDs (specific to the jobs manager, not the same as PIDs)
TODO: update the example below
<p>
<br>
\>lsjobs<br>
ID  &emsp; &emsp; PID &emsp; &emsp; STAT &emsp; &emsp; NAME &emsp; &emsp; TIME &emsp; &emsp; %CPU<br>
0001 &emsp;27129 &emsp; &emsp; R &emsp; &emsp; &emsp; sleep.c &emsp;&emsp;0:00:10 &emsp; &emsp; &emsp; 0
</p>
* __killjob *job*__ &emsp; - &emsp; cancel the specified job, which can be either the job's ID or name, with undefined behavior for which job of the same name is killed in the case of multiple of the same jobs
<p>
<br>
\>killjob 0001<br>
killing job 0001: sleep.c
</p>
