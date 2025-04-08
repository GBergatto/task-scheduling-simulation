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

# scenario 1: baseline -> compare algorithms
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((2,10))

# scenario 2: heterogeneous servers
N_SERVERS.append(6)
CAPACITIES.append([3, 3, 3, 1, 1, 1])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))

# scenarios 3-4: few long tasks vs many short tasks (with same duration range)
# scenario 3
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((9,15))
# scenario 4
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(3)
TASK_DURATIONS.append((1,7))

# scenarios 5-6: same computing power in different configurations (6x1 vs 3x2)
# scenario 5
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,5))
# scenario 6
N_SERVERS.append(3)
CAPACITIES.append([2 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,5))

# scenarios 7-12: more servers x cores configurations (12x1 vs 6x2)
# scenario 7
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 8
N_SERVERS.append(6)
CAPACITIES.append([2 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 9
N_SERVERS.append(4)
CAPACITIES.append([3 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 10
N_SERVERS.append(3)
CAPACITIES.append([4 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
# scenario 11
N_SERVERS.append(2)
CAPACITIES.append([6 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))

# scenarios 12-13: task duration range
# scenario 12: large range
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,11))
# scenario 13: narrow range
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((5,7))

