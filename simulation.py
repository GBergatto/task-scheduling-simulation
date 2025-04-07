import random
import simpy
from config import SimulationConfig
from monitor import SimulationMonitor
from typing import Generator


class Scheduler:
    def __init__(self, config: SimulationConfig, env: simpy.Environment) -> None:
        self.config = config
        self.env = env
        self.servers = [simpy.Resource(env, capacity=config.capacities[i]) for i in range(config.n_servers)]
        self.loads = [0.0 for _ in range(config.n_servers)]
        self.current_server = 0
        self.algorithm = getattr(self, config.lb_algorithm)

    def schedule(self, duration: float) -> tuple[int, simpy.Resource]:
        server : simpy.Resource = self.algorithm()
        sid = self.servers.index(server)
        self.loads[sid] += duration
        return sid, server

    def round_robin(self) -> simpy.Resource:
        server = self.servers[self.current_server]
        self.current_server = (self.current_server + 1) % len(self.servers)
        return server

    def random_allocation(self) -> simpy.Resource:
        return random.choice(self.servers)

    def least_load(self) -> simpy.Resource:
        load_per_core = [self.loads[i] / self.config.capacities[i] for i in range(len(self.loads))]
        sid = load_per_core.index(min(load_per_core))
        return self.servers[sid]

    def least_connections(self) -> simpy.Resource:
        return min(self.servers, key=lambda s: (s.count + len(s.queue)) / self.config.capacities[self.servers.index(s)])


def task(config: SimulationConfig, env: simpy.Environment, task_id: int, task_scheduler: Scheduler, monitor: SimulationMonitor) -> Generator:
    arrival_time = env.now
    task_duration = random.uniform(config.task_duration_min, config.task_duration_max)
    server_id, server = task_scheduler.schedule(task_duration)
    # TODO: yield computation time

    # save load (per core) and size of queues after the task has been scheduled
    monitor.loads_over_time.append((env.now, [task_scheduler.loads[i] / config.capacities[i] for i in range(len(task_scheduler.loads))]))
    monitor.queue_lengths_over_time.append((env.now, [len(s.queue) for s in task_scheduler.servers]))

    with server.request() as req:
        yield req  # wait for server
        waited_time = env.now - arrival_time
        monitor.task_latencies.append(waited_time)

        print(f"Task {task_id} ({task_duration:.3}) arr={arrival_time:.2f}, start={env.now:.2f}, server={server_id}, wait={waited_time:.2f}")

        yield env.timeout(task_duration) # wait for task execution
        print(f"Task {task_id} finished at {env.now:.2f}")

        # WARNING: the load on the server is updated only at the end of a task
        # so when a long task is about to finish, the load still seems very high
        task_scheduler.loads[server_id] -= task_duration

        # simulate cost of sending load and connection information
        if task_scheduler.algorithm == task_scheduler.least_load:
            yield env.timeout(config.overhead_least_load)
        elif task_scheduler.algorithm == task_scheduler.least_connections:
            yield env.timeout(config.overhead_least_connections)

        # save load (per core) and size of queues after the task has finished
        monitor.finished_task_counter += 1
        monitor.loads_over_time.append((env.now, [task_scheduler.loads[i] / config.capacities[i] for i in range(len(task_scheduler.loads))]))
        monitor.queue_lengths_over_time.append((env.now, [len(s.queue) for s in task_scheduler.servers]))


def task_queue(config: SimulationConfig, env: simpy.Environment, task_scheduler: Scheduler, monitor: SimulationMonitor) -> Generator:
    """Generate tasks according to a given random distribution"""
    task_id = 0
    while True:
        yield env.timeout(random.expovariate(config.arrival_rate))  # Poisson arrivals
        env.process(task(config, env, task_id, task_scheduler, monitor))
        task_id += 1

