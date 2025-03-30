from simulation import Scheduler

SIM_TIME = 50  # Total simulation time

N_SERVERS = 2  # Number of servers
# Capacity = number of task that can be executed simultaneously by a server
CAPACITIES = [2*(i+1) for i in range(N_SERVERS)]
LB_ALGORITHM = Scheduler.least_connections  # Load balancing algorithm
OVERHEAD_LEAST_LOAD = 2
OVERHEAD_LEAST_CONNECTIONS = 1

ARRIVAL_RATE = 1.0  # Average arrival rate (lambda) for Poisson process
TASK_DURATION_MIN = 2  # Minimum task processing time
TASK_DURATION_MAX = 5  # Maximum task processing time

