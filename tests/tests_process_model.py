import unittest
from unittest.mock import patch, Mock
import datetime as dt
import sys
sys.path.append("../")

from taskmanager import properties
#set max capacity = 3 for tests purposes
properties.MAX_CAPACITY = Mock(return_value=3).return_value

from taskmanager import process_model as pm

class TestProcess(unittest.TestCase):

    def test_create_process(self):
        """
        Test that process object can be created
        """
        pid = 1
        priority = 'low'
        newProcess = pm.SystemProcess(pid, priority)
        self.assertEqual(newProcess.priority, priority)
        self.assertEqual(newProcess.pid, pid)
        self.assertIsInstance(newProcess.createdOn, dt.datetime)


    def test_create_process_pid_string(self):
        """
        Test that pid passed as string is also recognized
        """
        pid = '1'
        priority = 'low'
        newProcess = pm.SystemProcess(pid, priority)
        self.assertIsInstance(newProcess.pid, int)
    
    def test_create_different_priorities(self):
        """
        Test that process can be created with priority low, medium and high
        """
        lowProcess = pm.SystemProcess(1,'low')
        mediumProcess = pm.SystemProcess(2,'medium')
        highProcess = pm.SystemProcess(3, 'high')
        self.assertEqual(lowProcess.priority,'low')
        self.assertEqual(mediumProcess.priority,'medium')
        self.assertEqual(highProcess.priority,'high')

    def test_create_process_list(self):
        """
        Test that new instance of process list can be retrieved 
        """
        pl = pm.get_process_list()
        self.assertIsInstance(pl, pm.ProcessList)
    
    def test_process_list_add__remove(self):
        """
        Test that new process can be added and removed from the process list 
        """
        plist = pm.get_process_list()
        plist._add(pm.SystemProcess(1,'low'))
        self.assertEqual(plist._get_capacity(),1)
        plist._remove(0)
        self.assertEqual(plist._get_capacity(),0)
    
    def test_compare_priorities(self):
        """
        Test that function compare priorities returns 1, -1 and 0 for each respective case
        """
        p1 = pm.SystemProcess(1, 'low')
        p2 = pm.SystemProcess(2,'medium')
        self.assertEqual(pm.compare_priorities(p1,p2),-1)
        self.assertEqual(pm.compare_priorities(p2,p1),1)
        self.assertEqual(pm.compare_priorities(p1,p1),0
        )
    
    def test_add_by_capacity(self):
        """
        Test that adding by capacity works
        """
        pm.add_process_by_capacity(pm.SystemProcess(1,'low'))
        pm.add_process_by_capacity(pm.SystemProcess(2,'low'))
        pm.add_process_by_capacity(pm.SystemProcess(3,'low'))
        response, message = pm.add_process_by_capacity(pm.SystemProcess(4,'low'))
        self.assertEqual(response, False)
        self.assertEqual(message,'Max capacity exceeded')

    def test_add_by_fifo(self):
        """
        Test adding by fifo, the oldest process should be removed 
        """
        pm.add_process_by_fifo(pm.SystemProcess(1,'low'))
        pm.add_process_by_fifo(pm.SystemProcess(2,'low'))
        pm.add_process_by_fifo(pm.SystemProcess(3,'low'))
        response, message = pm.add_process_by_fifo(pm.SystemProcess(4,'low'))
        self.assertEqual(response, True)
        self.assertEqual(message,'Removed process pid 1')
        for i in range(3):
            self.assertNotEqual(pm.get_process(index=i).pid,1)

    def test_add_by_priority(self):
        """
        Test that adding by priority work
        """
        pm.add_process_by_priority(pm.SystemProcess(00,'medium'))
        pm.add_process_by_priority(pm.SystemProcess(10,'medium'))
        pm.add_process_by_priority(pm.SystemProcess(20,'low'))
        response, message = pm.add_process_by_priority(pm.SystemProcess(30,'medium'))
        self.assertEqual(response, True)
        self.assertEqual(message,'Removed process pid 20')
        for i in range(2):
            self.assertNotEqual(pm.get_process(index=i).pid,20)
        response, message = pm.add_process_by_priority(pm.SystemProcess(40,'low'))
        self.assertEqual(response, False)
        self.assertEqual(message,'No lower priority process to be removed was found')

    #clean all processes between test cases
    @classmethod
    def tearDown(self):
        pList = pm.processList
        while (pList._get_capacity()>0):
            pList._get_process(0).kill()

if __name__ == '__main__':
    unittest.main()