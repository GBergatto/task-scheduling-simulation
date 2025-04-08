import matplotlib.pyplot as plt
from config import SimulationConfig


class SimulationMonitor:
    def __init__(self, config: SimulationConfig) -> None:
        self.algorith = config.lb_algorithm
        self.n_servers = config.n_servers
        self.finished_task_counter = 0
        self.task_latencies: list[float] = []
        self.loads_over_time: list[tuple[float, list[float]]] = [
            (0, [0 for _ in range(self.n_servers)])
        ]
        self.queue_lengths_over_time: list[tuple[float, list[int]]] = [
            (0, [0 for _ in range(self.n_servers)])
        ]

    def print_stats(self):
        assert len(self.task_latencies) > 0
        avg_latency = sum(self.task_latencies) / len(self.task_latencies)
        var_latency = sum((lat - avg_latency) ** 2 for lat in self.task_latencies) / len(self.task_latencies)

        assert len(self.loads_over_time) == len(self.queue_lengths_over_time)
        num_samples = len(self.loads_over_time)
        assert num_samples > 1

        avg_loads: list[float] = [0.0] * self.n_servers
        avg_qlens: list[float] = [0.0] * self.n_servers
        var_loads: list[float] = [0.0] * self.n_servers
        var_qlens: list[float] = [0.0] * self.n_servers

        for i in range(1, num_samples):
            t1, _ = self.loads_over_time[i - 1]
            t2, load = self.loads_over_time[i]
            for j in range(self.n_servers):
                avg_loads[j] += load[j] * (t2 - t1)

        total_time_load = self.loads_over_time[-1][0] - self.loads_over_time[0][0]
        avg_loads = [load / total_time_load for load in avg_loads]

        for i in range(1, num_samples):
            t1, _ = self.loads_over_time[i - 1]
            t2, load = self.loads_over_time[i]
            dt = t2 - t1
            for j in range(self.n_servers):
                var_loads[j] += ((load[j] - avg_loads[j]) ** 2) * dt

        var_loads = [var / total_time_load for var in var_loads]
        for i in range(1, num_samples):
            t1, _ = self.loads_over_time[i - 1]
            t2, qlen = self.loads_over_time[i]
            for j in range(self.n_servers):
                avg_qlens[j] += qlen[j] * (t2 - t1)

        total_time_qlen = (
            self.queue_lengths_over_time[-1][0] - self.queue_lengths_over_time[0][0]
        )
        avg_qlens = [ql / total_time_qlen for ql in avg_qlens]

        for i in range(1, num_samples):
            t1, _ = self.queue_lengths_over_time[i - 1]
            t2, qlen = self.queue_lengths_over_time[i]
            dt = t2 - t1
            for j in range(self.n_servers):
                var_qlens[j] += ((qlen[j] - avg_qlens[j]) ** 2) * dt

        var_qlens = [var / total_time_qlen for var in var_qlens]

        result = f"\nTotal number of tasks executed = {self.finished_task_counter}\n"
        result += f"Average Task Latency = {avg_latency:.3f}\n"
        result += f"Variance Task Latency = {var_latency:.3f}\n"
        for s in range(self.n_servers):
            result += f"Server {s}:\n"
            result += f"   Avg Load = {avg_loads[s]:.3f}, Avg Queue Length = {avg_qlens[s]:.3f}\n"
            result += f"   Var Load = {var_loads[s]:.3f}, Var Queue Length = {var_qlens[s]:.3f}\n"
        result += "\n"

        tot_avg_loads = sum(avg_loads) / len(avg_loads)
        tot_avg_qlens = sum(avg_qlens) / len(avg_qlens)
        result += f"Total Avg Load = {tot_avg_loads:.3f}\n"
        result += f"Total Avg Queue Length = {tot_avg_qlens:.3f}\n"

        if self.n_servers > 1:
            tot_var_loads = sum(
                (avg_loads[s] - tot_avg_loads) ** 2 for s in range(self.n_servers)
            ) / (self.n_servers - 1)
            tot_var_qlens = sum(
                (avg_qlens[s] - tot_avg_qlens) ** 2 for s in range(self.n_servers)
            ) / (self.n_servers - 1)
            result += f"Total Var Load = {tot_var_loads:.3f}\n"
            result += f"Total Var Queue Length = {tot_var_qlens:.3f}\n"

        return result

    def plot_task_latency(self, save_path=None):
        plt.figure(figsize=(10, 5))
        plt.plot(range(len(self.task_latencies)), self.task_latencies, label="Latency", linewidth=0.7)

        avg_latency = sum(self.task_latencies) / len(self.task_latencies)
        plt.axhline(avg_latency, color='red', linestyle='--', label=f"Avg Latency: {avg_latency:.2f}")

        plt.xlabel("Task ID")
        plt.ylabel("Latency")
        plt.title(f"Task Latency Over Time ({self.algorith})")
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(f"{save_path}/task_latency.png")  # Save the plot
        plt.close()

    def plot_load_over_time(self, save_path=None):
        assert self.loads_over_time

        timestamps, loads = zip(*self.loads_over_time)
        num_servers = len(loads[0])

        plt.figure(figsize=(10, 5))
        for i in range(num_servers):
            server_loads = [load[i] for load in loads]
            plt.plot(timestamps, server_loads, label=f"Server {i}", linewidth=0.7)

        plt.xlabel("Time")
        plt.ylabel("Load")
        plt.title(f"Server Load Over Time ({self.algorith})")
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(f"{save_path}/load.png")  # Save the plot
        plt.close()

    def plot_queue_lengths_over_time(self, save_path=None):
        assert self.loads_over_time

        timestamps, lengths = zip(*self.queue_lengths_over_time)
        num_servers = len(lengths[0])

        plt.figure(figsize=(10, 5))
        for i in range(num_servers):
            server_queue_lengths = [length[i] for length in lengths]
            plt.plot(timestamps, server_queue_lengths, label=f"Server {i}", linewidth=0.7)

        plt.xlabel("Time")
        plt.ylabel("Queue length")
        plt.title(f"Server Queue Length Over Time ({self.algorith})")
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(f"{save_path}/queue.png")  # Save the plot
        plt.close()

