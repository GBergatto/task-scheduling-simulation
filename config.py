from dataclasses import dataclass

@dataclass
class SimulationConfig:
    n_servers: int
    capacities: list[int]
    lb_algorithm: str
    overhead_least_load: float
    overhead_least_connections: float
    arrival_rate: float
    task_duration_min: float
    task_duration_max: float

