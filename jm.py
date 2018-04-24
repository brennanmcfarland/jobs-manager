import jmmanager as manager
from jmshell import ShellLoop
from multiprocessing import Process

manager_loop = Process(target=manager.manage_jobs)
manager_loop.start()
shell = ShellLoop()
shell.cmdloop()