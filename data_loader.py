import pandas as pd
import networkx as nx

def load_graph(node_csv, edge_csv):
    from utils import resource_path

    nodes = pd.read_csv(resource_path(node_csv), sep=";")
    edges = pd.read_csv(resource_path(edge_csv), sep=";")


    G = nx.Graph()

    for _, n in nodes.iterrows():
        G.add_node(
            int(n["node_id"]),
            processing_delay=float(str(n["s_ms"]).replace(",", ".")),
            reliability=float(str(n["r_node"]).replace(",", "."))
        )

    for _, e in edges.iterrows():
        G.add_edge(
            int(e["src"]),
            int(e["dst"]),
            delay=float(str(e["delay_ms"]).replace(",", ".")),
            bandwidth=float(str(e["capacity_mbps"]).replace(",", ".")),
            reliability=float(str(e["r_link"]).replace(",", "."))
        )

    return G
