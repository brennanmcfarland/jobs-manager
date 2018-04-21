import subprocess as sp

ERROR_VAL = -1


class JMJob:

    priority = ERROR_VAL
    id = ERROR_VAL
    pid = ERROR_VAL
    command = ""
    subprocess = None

    def __init__(self, id, command, parsed_command, priority):
        print(command)
        self.command = command
        self.priority = priority
        self.id = id
        self.subprocess = sp.Popen(parsed_command) # creates a new process
        self.pid = self.subprocess.pid
        self.status()

    def status(self):
        print("process ", self.command," started")
        print("ID: ", self.id, ", PID: ", self.pid)

    def is_terminated(self):
        return not self.subprocess.poll()

    def kill(self):
        self.subprocess.kill()
