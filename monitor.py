import matplotlib.pyplot as plt


class SimulationMonitor():
    def __init__(self, sim_time: int, n_servers: int) -> None:
        self.sim_time = sim_time
        self.n_servers = n_servers
        self.task_latencies: list[float] = []
        self.loads_over_time: list[tuple[float, list[float]]] = [(0, [0 for _ in range(n_servers)])]
        self.queue_lenghts_over_time: list[tuple[float, list[int]]] = [(0, [0 for _ in range(n_servers)])]

    def print_stats(self):
        assert len(self.task_latencies) > 0
        avg_latency = sum(self.task_latencies) / len(self.task_latencies)

        assert len(self.loads_over_time) == len(self.queue_lenghts_over_time)
        # compute average load per server
        num_samples = len(self.loads_over_time)
        avg_loads = []
        avg_queue_lengths = []
        for i in range(self.n_servers):
            avg_loads.append(sum(loads[i] for _, loads in self.loads_over_time) / num_samples)
            avg_queue_lengths.append(sum(queues[i] for _, queues in self.queue_lenghts_over_time) / num_samples)

        print(f"\nAverage Task Latency: {avg_latency:.3f}")
        for i, (avg_load, avg_queue) in enumerate(zip(avg_loads, avg_queue_lengths)):
            print(f"Server {i}: Avg Load = {avg_load:.3f}, Avg Queue Length = {avg_queue:.3f}")

        tot_avg_loads = sum(avg_loads) / len(avg_loads)
        tot_avg_queue_lengths = sum(avg_queue_lengths) / len(avg_queue_lengths)
        print(f"Total Avg Load = {tot_avg_loads:.3f}")
        print(f"Total Avg Queue Length = {tot_avg_queue_lengths:.3f}")

    def plot_load_over_time(self):
        assert self.loads_over_time

        timestamps, loads = zip(*self.loads_over_time)  # Separate timestamps and load values
        num_servers = len(loads[0])  # Number of servers

        plt.figure(figsize=(10, 5))
        for i in range(num_servers):
            server_loads = [load[i] for load in loads]
            plt.plot(timestamps, server_loads, label=f"Server {i}")

        plt.xlabel("Time")
        plt.ylabel("Load")
        plt.title("Server Load Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_queue_lengths_over_time(self):
        assert self.loads_over_time

        timestamps, lengths = zip(*self.queue_lenghts_over_time)  # Separate timestamps and load values
        num_servers = len(lengths[0])  # Number of servers

        plt.figure(figsize=(10, 5))
        for i in range(num_servers):
            server_queue_lengths = [length[i] for length in lengths]
            plt.plot(timestamps, server_queue_lengths, label=f"Server {i}")

        plt.xlabel("Time")
        plt.ylabel("Load")
        plt.title("Server Load Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

