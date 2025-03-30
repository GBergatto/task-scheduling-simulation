import matplotlib.pyplot as plt


class SimulationMonitor():
    def __init__(self, n_servers: int) -> None:
        self.n_servers = n_servers
        self.finished_task_counter = 0
        self.task_latencies: list[float] = []
        self.loads_over_time: list[tuple[float, list[float]]] = [(0, [0 for _ in range(n_servers)])]
        self.queue_lengths_over_time: list[tuple[float, list[int]]] = [(0, [0 for _ in range(n_servers)])]

    def print_stats(self):
        assert len(self.task_latencies) > 0
        avg_latency = sum(self.task_latencies) / len(self.task_latencies)

        assert len(self.loads_over_time) == len(self.queue_lengths_over_time)
        num_samples = len(self.loads_over_time)
        assert num_samples > 1

        avg_loads: list[float] = [0.0] * self.n_servers
        avg_qlens: list[float] = [0.0] * self.n_servers
        var_loads: list[float] = [0.0] * self.n_servers
        var_qlens: list[float] = [0.0] * self.n_servers

        # compute time-weighted average load for each server
        for i in range(1, num_samples):
            t1, _ = self.loads_over_time[i - 1]
            t2, load = self.loads_over_time[i]
            for j in range(self.n_servers):
                avg_loads[j] += load[j] * (t2 - t1)

        total_time_load = self.loads_over_time[-1][0] - self.loads_over_time[0][0]
        avg_loads = [load / total_time_load for load in avg_loads]

        # compute time-weighted variance of load for each server
        for i in range(1, num_samples):
            t1, _ = self.loads_over_time[i - 1]
            t2, load = self.loads_over_time[i]
            dt = t2 - t1
            for j in range(self.n_servers):
                var_loads[j] += ((load[j] - avg_loads[j]) ** 2) * dt

        var_loads = [var / total_time_load for var in var_loads]

        # compute time-weighted average queue length for each server
        for i in range(1, num_samples):
            t1, _ = self.loads_over_time[i - 1]
            t2, qlen = self.loads_over_time[i]
            for j in range(self.n_servers):
                avg_loads[j] += qlen[j] * (t2 - t1)

        total_time_qlen = self.queue_lengths_over_time[-1][0] - self.queue_lengths_over_time[0][0]
        avg_qlens = [ql / total_time_qlen for ql in avg_qlens]

        # compute time-weighted variance of queue length for each server
        for i in range(1, num_samples):
            t1, _ = self.queue_lengths_over_time[i - 1]
            t2, qlen = self.queue_lengths_over_time[i]
            dt = t2 - t1
            for j in range(self.n_servers):
                var_qlens[j] += ((qlen[j] - avg_qlens[j]) ** 2) * dt

        var_qlens = [var / total_time_qlen for var in var_qlens]

        print(f"\nTotal number of tasks executed {self.finished_task_counter}")
        print(f"Average Task Latency: {avg_latency:.3f}")
        for s in range(self.n_servers):
            print(f"Server {s}:")
            print(f"   Avg Load = {avg_loads[s]:.3f}, Avg Queue Length = {avg_qlens[s]:.3f}")
            print(f"   Var Load = {var_loads[s]:.3f}, Var Queue Length = {var_qlens[s]:.3f}")
        print()

        # compute averages of load and queue length across all servers
        tot_avg_loads = sum(avg_loads) / len(avg_loads)
        tot_avg_qlens = sum(avg_qlens) / len(avg_qlens)
        print(f"Total Avg Load = {tot_avg_loads:.3f}")
        print(f"Total Avg Queue Length = {tot_avg_qlens:.3f}")

        if self.n_servers > 1:
            # compute variances of average load and queue length across servers
            tot_var_loads = sum((avg_loads[s]-tot_avg_loads)**2 for s in range(self.n_servers)) / (self.n_servers-1)
            tot_var_qlens = sum((avg_qlens[s]-tot_avg_qlens)**2 for s in range(self.n_servers)) / (self.n_servers-1)
            print(f"Total Var Load = {tot_var_loads:.3f}")
            print(f"Total Var Queue Length = {tot_var_qlens:.3f}")

    def plot_load_over_time(self):
        assert self.loads_over_time

        timestamps, loads = zip(*self.loads_over_time)
        num_servers = len(loads[0])

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

        timestamps, lengths = zip(*self.queue_lengths_over_time)
        num_servers = len(lengths[0])

        plt.figure(figsize=(10, 5))
        for i in range(num_servers):
            server_queue_lengths = [length[i] for length in lengths]
            plt.plot(timestamps, server_queue_lengths, label=f"Server {i}")

        plt.xlabel("Time")
        plt.ylabel("Queue length")
        plt.title("Server Queue Length Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()

