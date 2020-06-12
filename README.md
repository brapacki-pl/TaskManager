# Task Manager

A sample python based module which allows manipulation of received OS processes by their PID and priority.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

Application logic resides in taskmanager module. There are 4 files:
process_model.py - contains data structure definitions and basic operations on those structures
services.py - represents actual interface to the module. These services should be invoked by importing application.
osmanager.py - externalized logic to manipulate local OS processes.
properties.py - properties file

Services.py functions:
add(process) - Adds a new process to ProcessList using algorithm from setup (capacity (default), FIFO, priority)
list(kwargs) - Returns array of records represting existing processes in a raw, text format, not ProcessList objects. 
	arguments (optional):
	sortBy - (pid (default), priority, createdOn) - defines sorting criteria
	reverseOrder - True|False(default) - sort in desc order
kill(pid) - Kills process in ProcessList with provided PID
kill_group(priority) - Kills all processes in ProcessList with provided priority
kill_all() - Kills all processes in ProcessList 

In order to allow easy testing a CMD app is created in the root folder under a name app.py
Run "python app.py" in order to use command-line like interface.

Commands:
add <pid> <priority> - adds a new process to task manager with provided PID and priority (low, medium, high)
list - lists all current processes
kill <pid> - kills process by its PID
kill_group <priority> - kills all processes with given priority
kill_all - kills all processes

### Prerequisites

Make sure python 3 and pip are installed on the system. 

### Installing

In order to install module just fork it or download from the repository to your local drive.

From the folder where it is downloaded run:

pip install -r requirements.txt

In order to install any needed libraries.

## Running the tests
Unit tests have been built with python unittest library.

Folder /tests contain 2 files with unit tests. Each corresponds to one of taskmanager files, either process_model or services file.

Services tests cover all test cases described in requirement form. Process_model could be better extended to cover more test cases as now it just focuses on critical functionality.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

