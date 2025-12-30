from metrics import total_delay, reliability_cost, resource_cost
from constraints import check_bandwidth

def total_cost(G, path, demand, w_delay, w_rel, w_res):
    if not check_bandwidth(G, path, demand):
        return 1e9

    return (
        w_delay * total_delay(G, path)
        + w_rel * reliability_cost(G, path)
        + w_res * resource_cost(G, path)
    )
