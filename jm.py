import jmmanager as manager
from jmshell import ShellLoop


manager_loop = manager.JMManager()
shell = ShellLoop()
manager_loop.start()
shell.cmdloop()