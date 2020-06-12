from taskmanager import services as s
import cmd

class TaskManer(cmd.Cmd):

    def do_list(self, line):
        response = s.list()
        for i in range(len(response)):
            print(response[i])

    def do_add(self, line):
        args = line.split()
        process = s.createProcess (args[0], args[1])
        s.add(process)

    def do_kill(self, line):
        pid = line.split()[0]
        s.kill(int(pid))


    def do_kill_group(self, line):
        priority = line.split()[0]
        s.kill_group(priority)
    
    def do_kill_all(self, line):
        s.kill_all()

    def do_EOF(self, line):
        return 

    def do_exit(self, line):
        exit()

if __name__ == '__main__':
    TaskManer().cmdloop()
