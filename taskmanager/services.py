from taskmanager import process_model as p
from taskmanager import properties

#general add service, invokes actual processing method based on setup
def add(process):
    """
    Adds a new process to ProcessList using algorithm from setup (capacity (default), FIFO, priority)
    """
    addMethod = properties.ADD_METHOD
    #add config based approach
    if (addMethod == None or addMethod == 'default' or addMethod == 'capacity'):
        return p.add_process_by_capacity(process)
    if (addMethod == 'fifo'):
        return p.add_process_by_fifo(process)
    if (addMethod == 'priority'):
        return p.add_process_by_priority(process)

def list(**kwargs):
    """
    Returns array of records represting existing processes in a raw, text format, not ProcessList object
    """
    responseList = p.get_processes(**kwargs)
    printableList = []
    for i in range(len(responseList)):
        printableList.append([responseList[i].pid, responseList[i].priority, responseList[i].createdOn])
    return printableList

def kill(pid):
    """
    Kills process in ProcessList with provided PID
    """
    process = p.get_process(pid=pid)
    process.kill()
    return

def kill_group(priority):
    """
    Kills all processes in ProcessList with provided priority
    """
    offset = 0
    for i in range(p.get_capacity()):
        process = p.get_process(index=i-offset)
        if (process.priority==priority):
            process.kill()
            offset+=1
    return

def kill_all():
    """
    Kills all processes in ProcessList 
    """
    capacity = p.get_capacity()
    while (capacity>0):
        p.get_process(index=0).kill()
        capacity = p.get_capacity()
    return

def createProcess(pid, priority):
    return p.SystemProcess(pid, priority)   