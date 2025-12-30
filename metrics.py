import math

def total_delay(G, path):
    d = 0
    for i in range(len(path) - 1):
        d += G[path[i]][path[i+1]]["delay"]
    for node in path[1:-1]:
        d += G.nodes[node]["processing_delay"]
    return d


def reliability_cost(G, path):
    c = 0
    for i in range(len(path) - 1):
        c += -math.log(G[path[i]][path[i+1]]["reliability"])
    for node in path:
        c += -math.log(G.nodes[node]["reliability"])
    return c


def resource_cost(G, path):
    c = 0
    for i in range(len(path) - 1):
        bw = G[path[i]][path[i+1]]["bandwidth"]
        c += 1000.0 / bw   # Mbps
    return c
