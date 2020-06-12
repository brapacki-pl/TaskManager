import unittest
from unittest.mock import patch, Mock
import datetime as dt
import sys
sys.path.append("../")
from taskmanager import properties
properties.MAX_CAPACITY = Mock(return_value=3).return_value

from taskmanager import process_model as pm
from taskmanager import services as s


class TestServices(unittest.TestCase):
    @patch('taskmanager.properties.ADD_METHOD', 'capacity')
    def test_add_capacity(self):
        """
        Test method add(process) assuming setup is set to capacity option
        """
        s.add(s.createProcess(1,'low'))
        s.add(s.createProcess(2,'low'))
        s.add(s.createProcess(3,'low'))
        response, message = s.add(s.createProcess(4,'low'))
        self.assertEqual(response, False)
        self.assertEqual(message,'Max capacity exceeded')

    @patch('taskmanager.properties.ADD_METHOD', 'fifo')
    def test_add_fifo(self):
        """
        Test method add(process) assuming setup is set to FIFO option
        """
        s.add(s.createProcess(1,'low'))
        s.add(s.createProcess(2,'low'))
        s.add(s.createProcess(3,'low'))
        response, message = s.add(s.createProcess(4,'low'))
        self.assertEqual(response, True)
        self.assertEqual(message,'Removed process pid 1')

    @patch('taskmanager.properties.ADD_METHOD', 'priority')
    def test_add_priority(self):
        """
        Test method add(process) assuming setup is set to priority option
        """
        s.add(s.createProcess(1,'high'))
        s.add(s.createProcess(2,'low'))
        s.add(s.createProcess(3,'medium'))
        response, message = s.add(s.createProcess(4,'medium'))
        self.assertEqual(response, True)
        self.assertEqual(message,'Removed process pid 2')
        response, message = s.add(s.createProcess(5,'low'))
        self.assertEqual(response, False)
        self.assertEqual(message,'No lower priority process to be removed was found')
        response, message = s.add(s.createProcess(6,'medium'))
        self.assertEqual(response, False)
        self.assertEqual(message,'No lower priority process to be removed was found')

    def test_list(self):
        """
        Test list method with sorting
        """
        s.add(s.createProcess(1,'high'))
        s.add(s.createProcess(2,'low'))
        s.add(s.createProcess(3,'medium'))
        returnedList = s.list()
        self.assertEqual(len(returnedList),3)
        #make sure list is sorted by created timestamp
        for i in range(1,3):
            self.assertGreaterEqual(returnedList[i][2],returnedList[i-1][2])
        
        #make sure list is sorted by priority
        returnedList = s.list(sortBy='priority')
        priorities = {'low':0,'medium':1,'high':2}
        for i in range(1,3):
            self.assertGreaterEqual(priorities[returnedList[i][1]]-priorities[returnedList[i-1][1]],0)

        #make sure list is sorted by pid
        returnedList = s.list(sortBy='pid')
        for i in range(1,3):
            self.assertGreaterEqual(returnedList[i][0],returnedList[i-1][0])

        #make sure list is sorted by pid in a reverse order
        returnedList = s.list(sortBy='pid', reverseOrder=True)
        for i in range(1,3):
            self.assertGreaterEqual(returnedList[i-1][0],returnedList[i][0])

    def test_kill(self):
        """
        Test kill option for a single process
        """
        s.add(s.createProcess(1,'high'))
        s.add(s.createProcess(2,'low'))
        self.assertEqual(len(s.list()),2)
        s.kill(1)
        self.assertEqual(len(s.list()),1)

    def test_kill_group(self):
        """
        Test kill option for a group of process with same priority
        """
        s.add(s.createProcess(1,'high'))
        s.add(s.createProcess(2,'low'))
        s.add(s.createProcess(3,'low'))
        self.assertEqual(len(s.list()),3)
        s.kill_group('low')
        self.assertEqual(len(s.list()),1)

    def test_kill_all(self):
        """
        Test kill option for all processes
        """
        s.add(s.createProcess(1,'high'))
        s.add(s.createProcess(2,'low'))
        s.add(s.createProcess(3,'low'))
        self.assertEqual(len(s.list()),3)
        s.kill_all()
        self.assertEqual(len(s.list()),0)

    #clean all processes between test cases
    @classmethod
    def tearDown(self):
        pList = pm.processList
        while (pList._get_capacity()>0):
            pList._get_process(0).kill()

if __name__ == '__main__':
    unittest.main()