import random
import simpy
import simulation_parameters as sp
from monitor import SimulationMonitor
from typing import Callable, Generator
import itertools
import os
import shutil


def generate_simulation_parameters(
    lb_algorithm, overhead, arrival_rate, task_duration_min, task_duration_max
):
    file_path = "simulation_parameters.py"
    with open(file_path, "r") as f:
        lines = f.readlines()
    updates = {
        "LB_ALGORITHM": f'"{lb_algorithm}"',
        "OVERHEAD_LEAST_LOAD": str(overhead[0]),
        "OVERHEAD_LEAST_CONNECTIONS": str(overhead[1]),
        "ARRIVAL_RATE": str(arrival_rate),
        "TASK_DURATION_MIN": str(task_duration_min),
        "TASK_DURATION_MAX": str(task_duration_max),
    }
    for i, line in enumerate(lines):
        for key, value in updates.items():
            if line.startswith(key):
                lines[i] = f"{key} = {value}\n"
    with open(file_path, "w") as f:
        f.writelines(lines)


def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path) 
            else:
                os.remove(file_path)  


class Scheduler:
    def __init__(self, env: simpy.Environment, num_servers: int, capacities: list[int], algorithm: Callable[['Scheduler'], simpy.Resource]) -> None:
        self.env = env
        self.servers = [simpy.Resource(env, capacity=capacities[i]) for i in range(num_servers)]
        self.loads = [0.0 for _ in range(num_servers)]
        self.current_server = 0
        self.algorithm = algorithm

    def schedule(self, duration: float) -> tuple[int, simpy.Resource]:
        server : simpy.Resource = self.algorithm(self)
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
        load_per_core = [self.loads[i] / sp.CAPACITIES[i] for i in range(len(self.loads))]
        sid = load_per_core.index(min(load_per_core))
        return self.servers[sid]

    def least_connections(self) -> simpy.Resource:
        return min(self.servers, key=lambda s: (s.count + len(s.queue)) / sp.CAPACITIES[self.servers.index(s)])


def task(env: simpy.Environment, task_id: int, task_scheduler: Scheduler, monitor: SimulationMonitor) -> Generator:
    arrival_time = env.now
    task_duration = random.uniform(sp.TASK_DURATION_MIN, sp.TASK_DURATION_MAX)
    server_id, server = task_scheduler.schedule(task_duration)
    # TODO: yield computation time

    # save load (per core) and size of queues after the task has been scheduled
    monitor.loads_over_time.append((env.now, [task_scheduler.loads[i] / sp.CAPACITIES[i] for i in range(len(task_scheduler.loads))]))
    monitor.queue_lengths_over_time.append((env.now, [len(s.queue) for s in task_scheduler.servers]))

    with server.request() as req:
        yield req  # wait for server
        waited_time = env.now - arrival_time
        monitor.task_latencies.append(waited_time)

        print(f"Task {task_id} ({task_duration:.3}) started on Server {server_id} at {env.now:.2f} (Waited {waited_time:.2f})")

        yield env.timeout(task_duration) # wait for task execution
        print(f"Task {task_id} finished at {env.now:.2f}")

        # WARNING: the load on the server is updated only at the end of a task
        # so when a long task is about to finish, the load still seems very high
        task_scheduler.loads[server_id] -= task_duration

        # simulate cost of sending load and connection information
        if task_scheduler.algorithm == task_scheduler.least_load:
            yield env.timeout(sp.OVERHEAD_LEAST_LOAD)
        elif task_scheduler.algorithm == task_scheduler.least_connections:
            yield env.timeout(sp.OVERHEAD_LEAST_CONNECTIONS)

        # save load (per core) and size of queues after the task has finished
        monitor.finished_task_counter += 1
        monitor.loads_over_time.append((env.now, [task_scheduler.loads[i] / sp.CAPACITIES[i] for i in range(len(task_scheduler.loads))]))
        monitor.queue_lengths_over_time.append((env.now, [len(s.queue) for s in task_scheduler.servers]))


def task_queue(env: simpy.Environment, task_scheduler: Scheduler, monitor: SimulationMonitor) -> Generator:
    """Generate tasks according to a given random distribution"""
    task_id = 0
    while True:
        yield env.timeout(random.expovariate(sp.ARRIVAL_RATE))  # Poisson arrivals
        env.process(task(env, task_id, task_scheduler, monitor))
        task_id += 1


def run(image_save_path):
    """Run the simulation script."""
    env = simpy.Environment()
    lb_algorithm_method = getattr(Scheduler, sp.LB_ALGORITHM)
    scheduler = Scheduler(env, sp.N_SERVERS, sp.CAPACITIES, lb_algorithm_method)
    monitor = SimulationMonitor(sp.N_SERVERS)

    env.process(task_queue(env, scheduler, monitor))
    env.run(until=sp.SIM_TIME)


    log_output = monitor.print_stats()
    monitor.plot_task_latency(image_save_path)
    monitor.plot_load_over_time(image_save_path)
    monitor.plot_queue_lengths_over_time(image_save_path)

    print(log_output) 

    return log_output  


if __name__ == "__main__":
    lb_algorithms = [
        "round_robin",
        "random_allocation",
        "least_load",
        "least_connections",
    ]
    overhead_options = [(2, 1), (1, 2)]
    arrival_rates = [0.5, 1.0, 1.5]
    task_durations = [(2, 5), (3, 6)]
    
    # delete all the logs generated before
    clear_directory("logs")
    clear_directory("plots")

    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    for lb_algorithm, overhead, arrival_rate, (task_min, task_max) in itertools.product(
        lb_algorithms, overhead_options, arrival_rates, task_durations
    ):
        image_save_path = f"plots/{lb_algorithm}_{arrival_rate}_{task_min}_{task_max}"
        os.makedirs(image_save_path, exist_ok=True)
        generate_simulation_parameters(
            lb_algorithm, overhead, arrival_rate, task_min, task_max
        )
        log_output = run(image_save_path)
        with open(
            f"logs/{lb_algorithm}_{arrival_rate}_{task_min}_{task_max}_log.txt", "w"
        ) as f:
            f.write(log_output)

        print(
            f"Simulation completed for {lb_algorithm} with ARRIVAL_RATE={arrival_rate}, "
            f"TASK_DURATION=({task_min}, {task_max})"
        )
