from dataclasses import dataclass

@dataclass
class SimulationConfig:
    n_servers: int
    capacities: list[int]
    lb_algorithm: str
    computation_overhead: float
    state_overhead: float
    arrival_rate: float
    task_duration_min: float
    task_duration_max: float

