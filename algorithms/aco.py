import random
import math
from solver import total_cost

def ant_colony_optimization(
    G, source, target, demand,
    w_delay, w_rel, w_res,
    ants=20, iterations=40,
    alpha=1.0, beta=2.0, rho=0.5
):
    # Initial pheromone
    pheromone = {}
    for u, v in G.edges():
        pheromone[(u, v)] = 1.0
        pheromone[(v, u)] = 1.0

    best_path = None
    best_cost = float("inf")

    for _ in range(iterations):
        all_paths = []

        for _ in range(ants):
            path = [source]
            visited = set(path)

            while path[-1] != target:
                current = path[-1]
                neighbors = [
                    n for n in G.neighbors(current)
                    if n not in visited
                ]

                if not neighbors:
                    break

                probs = []
                for n in neighbors:
                    tau = pheromone[(current, n)] ** alpha
                    eta = 1.0 / (
                        G[current][n]["delay"] + 1e-6
                    )
                    probs.append(tau * (eta ** beta))

                total = sum(probs)
                probs = [p / total for p in probs]

                next_node = random.choices(neighbors, probs)[0]
                path.append(next_node)
                visited.add(next_node)

            if path[-1] == target:
                cost = total_cost(
                    G, path, demand,
                    w_delay, w_rel, w_res
                )
                all_paths.append((path, cost))

                if cost < best_cost:
                    best_cost = cost
                    best_path = path

        # Evaporation
        for k in pheromone:
            pheromone[k] *= (1 - rho)

        # Deposit pheromone
        for path, cost in all_paths:
            for i in range(len(path) - 1):
                pheromone[(path[i], path[i+1])] += 1.0 / cost
                pheromone[(path[i+1], path[i])] += 1.0 / cost

    return best_path
