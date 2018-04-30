import subprocess as sp
import datetime

ERROR_VAL = -1


class JMJob:

    priority = ERROR_VAL
    id = ERROR_VAL
    pid = ERROR_VAL
    command = ""
    parsed_command = []
    subprocess = None
    nice = 100
    start_time = 0

    def __init__(self, id, command, parsed_command, priority):
        print(command)
        self.command = command
        self.parsed_command = parsed_command
        self.priority = priority
        self.id = id
        self.start_time = datetime.datetime.now()
        self.nice = self.fix_nice(priority)

    def start(self):
        self.subprocess = sp.Popen(self.parsed_command)  # creates a new process
        self.pid = self.subprocess.pid
        self.status()

    def status(self):
        print("process ", self.command," started")
        print("ID: ", self.id, ", PID: ", self.pid)

    def is_terminated(self):
        return not self.subprocess.poll()

    @staticmethod
    def fix_nice(niceinput):
        if int(niceinput) > 100:
            return 100
        elif int(niceinput) < 0:
            return 0
        else:
            return int(niceinput)

    def kill(self):
        self.subprocess.kill()
