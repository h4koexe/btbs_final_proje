def check_bandwidth(G, path, demand):
    for i in range(len(path) - 1):
        if G[path[i]][path[i+1]]["bandwidth"] < demand:
            return False
    return True
