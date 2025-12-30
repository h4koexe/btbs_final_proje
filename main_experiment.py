import time
import numpy as np
import pandas as pd

from data_loader import load_graph
from demand_loader import load_demands
from solver import total_cost

from algorithms.dijkstra import dijkstra_path
from algorithms.ga import genetic_algorithm
from algorithms.aco import ant_colony_optimization
from algorithms.sa import simulated_annealing


# ---------------- CONFIG ----------------
W_DELAY = 0.33
W_REL = 0.33
W_RES = 0.34

REPEATS = 5          # her demand için tekrar
MAX_DEMANDS = 20     # PDF şartı
# ---------------------------------------


def run_algorithm(algo_name, G, source, target, demand):
    start = time.time()

    if algo_name == "Dijkstra":
        path = dijkstra_path(G, source, target, demand, W_DELAY, W_REL, W_RES)
    elif algo_name == "GA":
        path = genetic_algorithm(G, source, target, demand, W_DELAY, W_REL, W_RES)
    elif algo_name == "ACO":
        path = ant_colony_optimization(G, source, target, demand, W_DELAY, W_REL, W_RES)
    elif algo_name == "SA":
        path = simulated_annealing(G, source, target, demand, W_DELAY, W_REL, W_RES)
    else:
        raise ValueError("Unknown algorithm")

    cost = total_cost(G, path, demand, W_DELAY, W_REL, W_RES)
    runtime = time.time() - start

    return cost, runtime


def main():
    print("Loading graph and demands...")
    G = load_graph("data/NodeData.csv", "data/EdgeData.csv")
    demands = load_demands("data/DemandData.csv").head(MAX_DEMANDS)

    algorithms = ["Dijkstra", "GA", "ACO", "SA"]
    results = []

    for idx, d in demands.iterrows():
        source = int(d["src"])
        target = int(d["dst"])
        demand_bw = float(str(d["demand_mbps"]).replace(",", "."))

        print(f"\nDemand {idx} | S={source}, D={target}, B={demand_bw}")

        for algo in algorithms:
            costs = []
            times = []

            for r in range(REPEATS):
                cost, runtime = run_algorithm(
                    algo, G, source, target, demand_bw
                )
                costs.append(cost)
                times.append(runtime)

            results.append({
                "Demand": idx,
                "Algorithm": algo,
                "AvgCost": np.mean(costs),
                "StdCost": np.std(costs),
                "MinCost": np.min(costs),
                "MaxCost": np.max(costs),
                "AvgTime": np.mean(times)
            })

            print(
                f"{algo:10s} | "
                f"AvgCost={np.mean(costs):.3f} | "
                f"Time={np.mean(times):.3f}s"
            )

    df = pd.DataFrame(results)
    df.to_csv("experiment_results.csv", index=False)

    print("\n=== EXPERIMENT FINISHED ===")
    print("Results saved to experiment_results.csv")


if __name__ == "__main__":
    main()
