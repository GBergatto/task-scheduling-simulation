SIM_TIME = 1000

ALGORITHMS = [
        "round_robin",
        "random_allocation",
        "least_load",
        "least_connections",
        ]

OVERHEADS = (0, 0)

N_SERVERS = []
CAPACITIES = []
ARRIVAL_RATES = []
TASK_DURATIONS = []

# scenario 1
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((2,10))

# scenario 2
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((5,7)) # smaller range

# scenario 3
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,5))

# scenario 4
N_SERVERS.append(3)
CAPACITIES.append([2 for _ in range(6)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((2,10))

# scenario 5: many short
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,5))

# scenario 6: multiple compution options for 12 cores tot
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 7
N_SERVERS.append(6)
CAPACITIES.append([2 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 8
N_SERVERS.append(4)
CAPACITIES.append([3 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 9
N_SERVERS.append(3)
CAPACITIES.append([4 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 10
N_SERVERS.append(2)
CAPACITIES.append([6 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 11
N_SERVERS.append(1)
CAPACITIES.append([12 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))

# scenario 12
N_SERVERS.append(6)
CAPACITIES.append([3, 3, 3, 1, 1, 1])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 13
N_SERVERS.append(6)
CAPACITIES.append([3, 1, 3, 1, 3, 1])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
