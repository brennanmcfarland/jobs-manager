import jmmanager as manager
from jmshell import ShellLoop
from multiprocessing import Process

manager_loop = Process(target=manager.manage_jobs) # TODO: pipe output
manager_loop.start()
shell = ShellLoop()
shell.cmdloop()