SIM_TIME = 1000

ALGORITHMS = [
        "round_robin",
        "random_allocation",
        "least_load",
        "least_connections",
        ]


N_SERVERS = []
CAPACITIES = []
ARRIVAL_RATES = []
TASK_DURATIONS = []
STATIC_COMPUTATIONS = []
STATE_AWARE_COMPUTATIONS = []
STATE_OVERHEADS = []


# scenario 1: baseline -> compare algorithms
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))

# scenario 2: heterogeneous servers
N_SERVERS.append(6)
CAPACITIES.append([3, 3, 3, 1, 1, 1])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))

# scenarios 3-4: few long tasks vs many short tasks (with same duration range)
# scenario 3
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(1)
TASK_DURATIONS.append((5, 8))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 4
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(3)
TASK_DURATIONS.append((1,3))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))

# scenarios 5-6: same computing power in different configurations (6x1 vs 3x2)
# scenario 5
N_SERVERS.append(6)
CAPACITIES.append([1 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,5))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 6
N_SERVERS.append(3)
CAPACITIES.append([2 for _ in range(6)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,5))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))

# scenarios 7-12: more servers x cores configurations (12x1 vs 6x2)
# scenario 7
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 8
N_SERVERS.append(6)
CAPACITIES.append([2 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 9
N_SERVERS.append(4)
CAPACITIES.append([3 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 10
N_SERVERS.append(3)
CAPACITIES.append([4 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 11
N_SERVERS.append(2)
CAPACITIES.append([6 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))

# scenarios 12-13: task duration range
# scenario 12: large range
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((1,11))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))
# scenario 13: narrow range
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((5,7))
STATIC_COMPUTATIONS.append(0)
STATE_AWARE_COMPUTATIONS.append(0)
STATE_OVERHEADS.append((0,0))

# scenario 14: test effect of overhead on algorithms
N_SERVERS.append(12)
CAPACITIES.append([1 for _ in range(12)])
ARRIVAL_RATES.append(2)
TASK_DURATIONS.append((2,10))
STATIC_COMPUTATIONS.append(0.1)
STATE_AWARE_COMPUTATIONS.append(0.3)
STATE_OVERHEADS.append((0,10))

