import cmd
import jmmanager as manager


class ShellLoop(cmd.Cmd):
    """The loop for the application shell.  Note that method names must be in the form of
    do_<command name> to work.  Arguments are parsed automatically."""

    prompt = "jm> "

    def precmd(self, line):
        manager.manage_jobs()
        return line

    def do_runjob(self, command, priority = 100):
        parsed_command = command.split()
        manager.add_job(command, parsed_command, priority)

    def do_lsjobs(self, line):
        print("ID   PID     NICE STAT NAME TIME %CPU")
        print("0001 27129   03  R   ./test.c  0:00:10 50")

    def do_killjob(self, job_identifier):
        'job_identifier can be either ID or name'
        print("TODO: kill job ", job_identifier)

    def emptyline(self):
        pass

    def do_exit(self, line):
        return True

    def do_quit(self, line):
        return True
