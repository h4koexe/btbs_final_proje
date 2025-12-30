from data_loader import load_graph
from demand_loader import load_demands
from algorithms.sa import simulated_annealing
from solver import total_cost

G = load_graph("data/NodeData.csv", "data/EdgeData.csv")
demands = load_demands("data/DemandData.csv")

W_DELAY = 0.33
W_REL = 0.33
W_RES = 0.34

d = demands.iloc[0]
source = int(d["src"])
target = int(d["dst"])
demand_bw = float(str(d["demand_mbps"]).replace(",", "."))

path = simulated_annealing(
    G, source, target, demand_bw,
    W_DELAY, W_REL, W_RES
)

cost = total_cost(G, path, demand_bw, W_DELAY, W_REL, W_RES)

print("=== SIMULATED ANNEALING RESULT ===")
print("Source:", source)
print("Target:", target)
print("Demand (Mbps):", demand_bw)
print("Path:", path)
print("Total Cost:", cost)
