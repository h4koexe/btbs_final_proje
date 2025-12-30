import random
import math
import networkx as nx
from solver import total_cost

def neighbor_path(G, path):
    if len(path) < 4:
        return path

    i = random.randint(1, len(path) - 2)
    node = path[i]

    neighbors = list(G.neighbors(node))
    if not neighbors:
        return path

    new_node = random.choice(neighbors)
    new_path = path[:i] + [new_node] + path[i+1:]
    return new_path


def simulated_annealing(
    G, source, target, demand,
    w_delay, w_rel, w_res,
    T0=100.0, Tmin=1e-3, alpha=0.95, steps=100
):
    try:
        current_path = nx.shortest_path(G, source, target)
    except:
        return None

    current_cost = total_cost(
        G, current_path, demand,
        w_delay, w_rel, w_res
    )

    best_path = current_path
    best_cost = current_cost

    T = T0

    while T > Tmin:
        for _ in range(steps):
            new_path = neighbor_path(G, current_path)
            new_cost = total_cost(
                G, new_path, demand,
                w_delay, w_rel, w_res
            )

            delta = new_cost - current_cost

            if delta < 0 or random.random() < math.exp(-delta / T):
                current_path = new_path
                current_cost = new_cost

                if current_cost < best_cost:
                    best_cost = current_cost
                    best_path = current_path

        T *= alpha

    return best_path
