from monitor import SimulationMonitor
from config import SimulationConfig
from simulation import Scheduler, task_queue
import simpy
import scenarios as sn
import os
import shutil


def clear_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path) 
            else:
                os.remove(file_path)  


def run(config: SimulationConfig, image_save_path):
    """Run a simulation with the given set of parameters"""
    env = simpy.Environment()
    scheduler = Scheduler(config, env)
    monitor = SimulationMonitor(config.n_servers)

    env.process(task_queue(config, env, scheduler, monitor))
    env.run(until=sn.SIM_TIME)

    log_output = monitor.print_stats()
    monitor.plot_task_latency(image_save_path)
    monitor.plot_load_over_time(image_save_path)
    monitor.plot_queue_lengths_over_time(image_save_path)

    print(log_output) 

    return log_output


if __name__ == "__main__":
    
    clear_directory("logs")
    clear_directory("plots")
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    for n, cap, rate, (dmin, dmax) in zip(sn.N_SERVERS, sn.CAPACITIES, sn.ARRIVAL_RATES, sn.TASK_DURATIONS):
        for algo in sn.ALGORITHMS:
            image_save_path = f"plots/{algo}_{rate}_{dmin}_{dmax}"
            os.makedirs(image_save_path, exist_ok=True)

            config = SimulationConfig(
                n_servers=n,
                capacities=cap,
                lb_algorithm=algo,
                overhead_least_load=sn.OVERHEADS[0],
                overhead_least_connections=sn.OVERHEADS[1],
                arrival_rate=rate,
                task_duration_min=dmin,
                task_duration_max=dmax
            )

            log_output = run(config, image_save_path)
            with open(f"logs/{algo}_{rate}_{dmin}_{dmax}_log.txt", "w") as f:
                f.write(log_output)

            print(f"Simulation completed for {algo} with ARRIVAL_RATE={rate}, TASK_DURATION=({dmin}, {dmax})\n")

