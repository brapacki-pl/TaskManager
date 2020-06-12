from datetime import datetime
from operator import attrgetter
from functools import cmp_to_key
from taskmanager import osmanager as osm
from taskmanager import properties

#dictionary of priorities
priorities = {'low':0,'medium':1,'high':2}

#objects
class SystemProcess:
    def __init__(self, pid, priority):
        self.pid = int(pid)
        self.priority = priority
        self.createdOn = datetime.now() #assume process was created when object is instatiated

    def kill(self): 
        #tries to kill process on local OS, then removes object from Process List
        osm.kill_os_process(self.pid)
        remove_process(pid=self.pid)
        

class ProcessList:

    def __init__(self):
        self.processes = []
        self.maxCapacity = properties.MAX_CAPACITY

    def _add(self, process):
        #insert into list sorted by created time, so that original list is always indexed according to process time
        if (process != None):
            for i in range(len(self.processes)):
                if (self.processes[i].createdOn>process.createdOn):
                    self.processes = self.processes[:i] + [process] + self.processes[i:] 
                    return
            self.processes.append(process)
            return
                    
    def _remove(self, i):
        del self.processes[i]

    def _get_capacity(self):
        return len(self.processes)

    def _get_process(self,i):
        return self.processes[i]
    
    
#global variables
processList = ProcessList()

#module methods
def compare_priorities(process1, process2):
    """Compares priorities of 2 passed processes. Returns 1 if process 1 has higher priority, -1 if low and 0 if both have equal."""
    global priorities
    return priorities[process1.priority]-priorities[process2.priority]

def get_max_capacity():
    """Returns maximum capacity of instatiated ProcessList"""
    global processList
    return processList.maxCapacity


def get_process_list():
    """Returns instatiated ProcessList"""
    global processList
    return processList

def get_capacity():
    """Returns current capacity of instatiated ProcessList"""
    global processList
    return processList._get_capacity()

def get_process(**kwargs):
    """
    Returns process from instatiated ProcessList. 
    Possible arguments: 
    pid - then provide PID of process to be returned
    index - index of process within ProcessList"""
    global processList
    for key, value in kwargs.items():
        if (key=='pid'):
            for i in range(get_capacity()):
                if (processList._get_process(i).pid == value):
                    return processList._get_process(i)
        if (key=='index'):
            return processList._get_process(value)
                    
def remove_process(**kwargs):
    """
    Removes process from instatiated ProcessList. 
    Possible arguments: 
    pid - then provide PID of process to be removed
    index - index of process within ProcessList to be removed"""
    global processList
    for key, value in kwargs.items():
        if (key == 'pid'):
            for i in range(len(processList.processes)):
                if (processList.processes[i].pid == value):
                    processList._remove(i)
                    return
        if (key == 'index'):
            processList._remove(value)       
            return 

#default add service, will add processes to the list until capacity is reached
def add_process_by_capacity(process):
    """
    Adds new process to ProcessList using capacity based algorithm.
    If max capacity reached, new process is not added and first argument of response is False.
    Returns: True|False and description message"""
    global processList
    if (get_capacity()<get_max_capacity()):
        processList._add(process)
        return True, None
    else:
        return False, 'Max capacity exceeded'

#will add processes to the list and automatically remove based on fifo approach once capacity is reached
def add_process_by_fifo(process):
     """
    Adds new process to ProcessList using FIFO based algorithm.
    If max capacity reached, new process is added only if first added existing process was removed already.
    Returns: True|False and description message stating which PID was removed (if any)"""
    global processList
    if (get_capacity()<get_max_capacity()):
        processList._add(process)
        return True, None
    else:
        toRemoveProcess = processList._get_process(0)
        processList._remove(0)
        processList._add(process)
        return True, 'Removed process pid '+str(toRemoveProcess.pid)


#will add processes to the list and automaticall remove the lowest priority one once capacity is reached
def add_process_by_priority(process):
    """
    Adds new process to ProcessList using priority based algorithm.
    If max capacity reached, new process is added only if existing process with lower priority was removed.
    Returns: True|False and description message stating which PID was removed (if any)"""
    global processList
    #if there is capacity, add new process and finish
    if (processList._get_capacity()<processList.maxCapacity):
        processList._add(process)
        return True, None

    #if new there is no capacity and new process has low priority, do not add and exit
    if (process.priority == 'low'):
        return False, 'No lower priority process to be removed was found'

    #if new process has priority medium or high, try to add it to process list replacing lower priority process inside

    #find index of matching process to be replaced
    for i in range(processList._get_capacity()):
        p = processList._get_process(i)
        if (compare_priorities(p,process)<0):
            removedPid = p.pid
            p.kill()
            processList._add(process)
            return True, 'Removed process pid '+str(removedPid)
    
    #no process to be replaced was found
    return False, 'No lower priority process to be removed was found'

def get_processes(**kwargs):
    """
    Returns an instace of ProcessList with processes sorted according to passed params.
    Params:
    sortBy - possible values: default, priority, pid
    reverseOrder - True|False, stating order of sorting asc or desc
    """
    sortBy = 'pid' #default value for pid sort
    reverseOrder = False #default value for ordering type (ascending)

    #check if sortBy and/or reverseOrder params were passed, if yes replace default values with passed ones
    for key, value in kwargs.items():
        if (key == 'sortBy'):
            sortBy = value     
        if (key == 'reverseOrder'):
            reverseOrder = value

    global processList
    #return new array using default comparator
    if (sortBy != 'priority'):
        tempArray = sorted(processList.processes, key=attrgetter(sortBy), reverse=reverseOrder)
    #return new array using custom priorities comparator
    else:
        tempArray = sorted(processList.processes, key=cmp_to_key(compare_priorities), reverse=reverseOrder)
    return tempArray
            


