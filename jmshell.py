import cmd
import jmmanager


class ShellLoop(cmd.Cmd):
    """The loop for the application shell.  Note that method names must be in the form of
    do_<command name> to work.  Arguments are parsed automatically."""

    prompt = "jm> "

    def do_runjob(self, command, priority = 100):
        parsed_command = command.split()
        jmmanager.add_job(command, parsed_command, priority)
        print("adding job ", parsed_command)

    def do_lsjobs(self, line):
        jmmanager.list_jobs()

    def do_killjob(self, job_identifier):
        'job_identifier can be either ID or name'
        jmmanager.kill_job(job_identifier)
        print("killing job ", job_identifier)

    def emptyline(self):
        pass

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True
