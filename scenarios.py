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
CAPACITIES.append([2 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))

# scenario 2
N_SERVERS.append(6)
CAPACITIES.append([2 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((5,7)) # smaller range

