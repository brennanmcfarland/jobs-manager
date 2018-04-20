NB for Josh: [a reference for markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links)
and in case you're wondering, there's lots of ways to convert markdown to pdf easily

# Design Document - Jobs Manager
Brennan McFarland and Joshua Reichman

### Overview
Our project consists of a program to monitor and manage the concurrent execution of other programs via command line.  The idea is that the user can queue up bash commands as "jobs" and the manager will then schedule CPU time to run them concurrently or with the appearance of concurrency if there is only one CPU core.  Preference will be given to processes that are queued first, and the user can also assign priority to certain jobs.  The processes will be scheduled in a manner similar to the popular telescope scheduling algorithm.  Additionally, the user can type a command to display the list of jobs and their status in a manner similar to the "top" command.  In a nutshell, the manager function similarly to queuing and viewing the status of batch processes on the HPC cluster.
