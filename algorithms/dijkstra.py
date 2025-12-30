import heapq
from solver import total_cost

def dijkstra_path(G, source, target, demand, w_delay, w_rel, w_res):
    """
    Dijkstra using total_cost as path cost.
    Returns best path found.
    """

    pq = []
    heapq.heappush(pq, (0, [source]))

    visited = set()

    while pq:
        cost, path = heapq.heappop(pq)
        current = path[-1]

        if current == target:
            return path

        if current in visited:
            continue
        visited.add(current)

        for neighbor in G.neighbors(current):
            if neighbor in path:
                continue

            new_path = path + [neighbor]
            new_cost = total_cost(
                G, new_path, demand, w_delay, w_rel, w_res
            )

            heapq.heappush(pq, (new_cost, new_path))

    return None
