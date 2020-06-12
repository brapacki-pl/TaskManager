import os
import signal
from taskmanager import properties

def kill_os_process(pid):
    """A stub function which tries to kill local OS system process identified by passed PID"""
    try:
        if (properties.ENVIRONMENT == 'dev'):
            #do no try to really kill process if environment is set to dev
            return
        else:
            os.kill(pid, signal.SIGTERM)
    except:
        #do not throw error, for now assume kill succeeded
        #TODO: implement error handling
        return



