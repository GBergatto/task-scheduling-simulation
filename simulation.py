import random
import simpy
import simulation_parameters as sp


class Scheduler:
    def __init__(self, env, num_servers, algorithm):
        self.env = env
        self.servers = [simpy.Resource(env, capacity=1) for _ in range(num_servers)]
        self.current_server = 0
        
        if not callable(algorithm):
            raise ValueError("Algorithm must be a callable method.")
        
        # reference to the algorithm to use for scheduling
        self.algorithm = algorithm

    def schedule(self):
        return self.algorithm(self)

    def round_robin(self):
        server = self.servers[self.current_server]
        self.current_server = (self.current_server + 1) % len(self.servers)
        return server

    def random_allocation(self):
        return random.choice(self.servers)

    def least_load(self):
        return min(self.servers, key=lambda s: len(s.queue))

    def least_connections(self):
        return min(self.servers, key=lambda s: s.count)


def task(env, task_id, task_scheduler):
    arrival_time = env.now
    task_duration = random.uniform(sp.TASK_DURATION_MIN, sp.TASK_DURATION_MAX)
    server = task_scheduler.schedule()

    with server.request() as req:
        yield req  # wait for server
        waited_time = env.now - arrival_time
        # TODO: find a way to identify the server assigned to each task
        print(f"Task {task_id} started on Server {server} at {env.now:.2f} (Waited {waited_time:.2f})")
        yield env.timeout(task_duration) # wait for task execution
        print(f"Task {task_id} finished at {env.now:.2f}")


def task_queue(env, task_scheduler):
    """Generate tasks according to a given random distribution"""
    task_id = 0
    while True:
        yield env.timeout(random.expovariate(sp.ARRIVAL_RATE))  # Poisson arrivals
        env.process(task(env, task_id, task_scheduler))
        task_id += 1


def main():
    env = simpy.Environment()
    scheduler = Scheduler(env, sp.N_SERVERS, Scheduler.least_load)
    env.process(task_queue(env, scheduler))
    env.run(until=sp.SIM_TIME)


if __name__ == "__main__":
    main()

