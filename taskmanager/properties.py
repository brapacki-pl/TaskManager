#Maximum number of processes inside the task manager. Processes tried to be added above maximum will be handled according to ADD_METHOD approach
MAX_CAPACITY = 10
#How to treat processes added above set max capacity. Possible values: default, priority, fifo and capacity (same as default)
ADD_METHOD = 'priority'
ENVIRONMENT = 'dev'