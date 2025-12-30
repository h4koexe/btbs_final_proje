import random
import networkx as nx
from solver import total_cost

def random_path(G, source, target, max_tries=100):
    for _ in range(max_tries):
        try:
            return nx.shortest_path(
                G, source, target,
                method="dijkstra"
            )
        except:
            pass
    return None


def crossover(p1, p2):
    common = set(p1[1:-1]) & set(p2[1:-1])
    if not common:
        return p1[:]

    cut = random.choice(list(common))
    i1 = p1.index(cut)
    i2 = p2.index(cut)

    child = p1[:i1] + p2[i2:]
    return child


def mutate(G, path, mutation_rate=0.2):
    if random.random() > mutation_rate:
        return path

    if len(path) < 4:
        return path

    i = random.randint(1, len(path) - 2)
    node = path[i]

    neighbors = list(G.neighbors(node))
    if not neighbors:
        return path

    new_node = random.choice(neighbors)
    return path[:i] + [new_node] + path[i+1:]


def genetic_algorithm(
    G, source, target, demand,
    w_delay, w_rel, w_res,
    pop_size=30, generations=40
):
    population = []

    for _ in range(pop_size):
        p = random_path(G, source, target)
        if p:
            population.append(p)

    best_path = None
    best_cost = float("inf")

    for _ in range(generations):
        scored = []
        for p in population:
            c = total_cost(G, p, demand, w_delay, w_rel, w_res)
            scored.append((c, p))

            if c < best_cost:
                best_cost = c
                best_path = p

        scored.sort(key=lambda x: x[0])
        population = [p for _, p in scored[:pop_size // 2]]

        new_pop = population[:]
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population, 2)
            child = crossover(p1, p2)
            child = mutate(G, child)
            new_pop.append(child)

        population = new_pop

    return best_path
