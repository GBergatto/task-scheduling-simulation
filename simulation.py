import random
import simpy
import simulation_parameters as sp
from typing import Callable


class Scheduler:
    def __init__(self, env: simpy.Environment, num_servers: int, capacity: int, algorithm: Callable[['Scheduler'], simpy.Resource]):
        self.env = env
        self.servers = [simpy.Resource(env, capacity=capacity) for _ in range(num_servers)]
        self.loads = [0.0 for _ in range(num_servers)]
        self.current_server = 0
        self.algorithm = algorithm

    def schedule(self, duration: float):
        server : simpy.Resource = self.algorithm(self)
        sid = self.servers.index(server)
        self.loads[sid] += duration
        return sid, server

    def round_robin(self):
        server = self.servers[self.current_server]
        self.current_server = (self.current_server + 1) % len(self.servers)
        return server

    def random_allocation(self):
        return random.choice(self.servers)

    def least_load(self):
        sid = self.loads.index(min(self.loads))
        return self.servers[sid]

    def least_connections(self):
        return min(self.servers, key=lambda s: s.count + len(s.queue))


def task(env: simpy.Environment, task_id: int, task_scheduler: Scheduler):
    arrival_time = env.now
    task_duration = random.uniform(sp.TASK_DURATION_MIN, sp.TASK_DURATION_MAX)
    server_id, server = task_scheduler.schedule(task_duration)
    # simulate cost of sending load and connection information
    if task_scheduler.algorithm == task_scheduler.least_load:
        yield env.timeout(sp.OVERHEAD_LEAST_LOAD)
    elif task_scheduler.algorithm == task_scheduler.least_connections:
        yield env.timeout(sp.OVERHEAD_LEAST_CONNECTIONS)

    with server.request() as req:
        yield req  # wait for server
        waited_time = env.now - arrival_time
        print(f"Task {task_id} ({task_duration:.3}) started on Server {server_id} at {env.now:.2f} (Waited {waited_time:.2f})")
        print(f"Loads: {task_scheduler.loads}")

        yield env.timeout(task_duration) # wait for task execution

        print(f"Task {task_id} finished at {env.now:.2f}")
        task_scheduler.loads[server_id] -= task_duration
        print(task_scheduler.loads)


def task_queue(env: simpy.Environment, task_scheduler: Scheduler):
    """Generate tasks according to a given random distribution"""
    task_id = 0
    while True:
        yield env.timeout(random.expovariate(sp.ARRIVAL_RATE))  # Poisson arrivals
        env.process(task(env, task_id, task_scheduler))
        task_id += 1


def main():
    env = simpy.Environment()
    scheduler = Scheduler(env, sp.N_SERVERS, sp.CAPACITY, sp.LB_ALGORITHM)
    env.process(task_queue(env, scheduler))
    env.run(until=sp.SIM_TIME)


if __name__ == "__main__":
    main()

