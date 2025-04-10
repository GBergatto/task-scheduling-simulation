from monitor import SimulationMonitor
from config import SimulationConfig
from simulation import Scheduler, task_queue
import random
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
    random.seed(11)
    env = simpy.Environment()
    scheduler = Scheduler(config, env)
    monitor = SimulationMonitor(config)

    env.process(task_queue(config, env, scheduler, monitor))
    env.run(until=sn.SIM_TIME)

    log_output = monitor.print_stats()
    monitor.plot_task_latency(image_save_path)
    monitor.plot_load_over_time(image_save_path)
    monitor.plot_queue_lengths_over_time(image_save_path)

    print(log_output) 

    return log_output


if __name__ == "__main__":
    clear_directory("output")
    os.makedirs("output", exist_ok=True)

    assert len(sn.N_SERVERS) == len(sn.CAPACITIES) == len(sn.ARRIVAL_RATES) == \
       len(sn.TASK_DURATIONS) == len(sn.STATIC_COMPUTATIONS) == \
       len(sn.STATE_AWARE_COMPUTATIONS) == len(sn.STATE_OVERHEADS), "Mismatched lengths in scenarios config"

    for i, (n, cap, rate, (dmin, dmax), static_co, state_aware_co, (so_min, so_max)) in enumerate(
            zip(sn.N_SERVERS, sn.CAPACITIES, sn.ARRIVAL_RATES, sn.TASK_DURATIONS,
                sn.STATIC_COMPUTATIONS, sn.STATE_AWARE_COMPUTATIONS, sn.STATE_OVERHEADS)):

        for state_overhead in range(so_min, so_max+1):
            for algo in sn.ALGORITHMS:
                image_save_path = f"output/scenario_{i+1:02d}/{state_overhead}_{algo}"
                os.makedirs(image_save_path, exist_ok=True)

                computation_overhead = static_co
                if "least" in algo:
                    computation_overhead = state_aware_co

                config = SimulationConfig(
                    n_servers=n,
                    capacities=cap,
                    lb_algorithm=algo,
                    computation_overhead=computation_overhead,
                    state_overhead=state_overhead/10 if "least" in algo else 0,
                    arrival_rate=rate,
                    task_duration_min=dmin,
                    task_duration_max=dmax
                )

                log_output = run(config, image_save_path)
                with open(f"{image_save_path}/log.txt", "w") as f:
                    f.write(log_output)

                print(f"Simulation completed for {algo} with ARRIVAL_RATE={rate}, TASK_DURATION=({dmin}, {dmax})\n")

