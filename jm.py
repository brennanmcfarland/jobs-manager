import jmmanager as manager
from jmshell import ShellLoop
from multiprocessing import Process

#manager_loop = Process(target=manager.manage_jobs,args=(.5,)) # TODO: pipe output
#manager_loop.start()
shell = ShellLoop()
shell.cmdloop()
#shell_loop = Process(target=shell.cmdloop)
#shell_loop.start()
#manager.manage_jobs(.5)