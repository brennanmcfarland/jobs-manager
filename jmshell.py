import cmd
import jmmanager


class ShellLoop(cmd.Cmd):
    """The loop for the application shell.  Note that method names must be in the form of
    do_<command name> to work.  Arguments are parsed automatically."""

    prompt = "jm> "

    def do_runjob(self, command):
        'add a job to the queue'
        priority = 100
        parsed_command = command.split()
        if parsed_command[0].isdigit():
            priority = parsed_command[0]
            parsed_command.pop(0)
            command = " ".join(parsed_command)
        jmmanager.add_job(command, parsed_command, priority)
        print("adding job ", parsed_command)

    def do_lsjobs(self, line):
        'display the list of jobs and their statuses and IDs'
        jmmanager.list_jobs()

    def do_killjob(self, job_identifier):
        'cancel the specified job, which can be either the job\'s ID or name'
        jmmanager.kill_job(job_identifier)
        print("killing job ", job_identifier)

    def emptyline(self):
        pass

    def do_exit(self, line):
        'ends program'
        return True

    def do_quit(self, line):
        'ends program'
        return True
