import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

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
# ---------------------------------------


class RoutingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QoS Routing Simulator")

        # Load data
        self.G = load_graph("data/NodeData.csv", "data/EdgeData.csv")
        self.demands = load_demands("data/DemandData.csv")

        # Main layout
        self.left = tk.Frame(root, width=200)
        self.left.pack(side=tk.LEFT, fill=tk.Y)

        self.right = tk.Frame(root)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Demand selector
        tk.Label(self.left, text="Demand seç:").pack(pady=5)
        self.demand_box = ttk.Combobox(
            self.left,
            values=[f"{i}: {int(r.src)} → {int(r.dst)}"
                    for i, r in self.demands.iterrows()]
        )
        self.demand_box.current(0)
        self.demand_box.pack(pady=5)

        # Buttons
        tk.Button(self.left, text="Dijkstra",
                  command=lambda: self.run_algo("Dijkstra")).pack(fill=tk.X, pady=2)

        tk.Button(self.left, text="Genetic Algorithm",
                  command=lambda: self.run_algo("GA")).pack(fill=tk.X, pady=2)

        tk.Button(self.left, text="Ant Colony",
                  command=lambda: self.run_algo("ACO")).pack(fill=tk.X, pady=2)

        tk.Button(self.left, text="Simulated Annealing",
                  command=lambda: self.run_algo("SA")).pack(fill=tk.X, pady=2)

        # Result label
        self.result_label = tk.Label(self.left, text="", wraplength=180)
        self.result_label.pack(pady=10)

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.pos = nx.spring_layout(self.G, seed=42)
        self.draw_graph()

    def get_selected_demand(self):
        idx = self.demand_box.current()
        d = self.demands.iloc[idx]
        return (
            int(d["src"]),
            int(d["dst"]),
            float(str(d["demand_mbps"]).replace(",", "."))
        )

    def run_algo(self, algo):
        source, target, demand = self.get_selected_demand()

        if algo == "Dijkstra":
            path = dijkstra_path(
                self.G, source, target, demand,
                W_DELAY, W_REL, W_RES
            )
        elif algo == "GA":
            path = genetic_algorithm(
                self.G, source, target, demand,
                W_DELAY, W_REL, W_RES
            )
        elif algo == "ACO":
            path = ant_colony_optimization(
                self.G, source, target, demand,
                W_DELAY, W_REL, W_RES
            )
        elif algo == "SA":
            path = simulated_annealing(
                self.G, source, target, demand,
                W_DELAY, W_REL, W_RES
            )
        else:
            return

        cost = total_cost(self.G, path, demand, W_DELAY, W_REL, W_RES)

        self.result_label.config(
            text=f"{algo}\nCost: {cost:.3f}\nPath length: {len(path)}"
        )

        self.draw_graph(path)

    def draw_graph(self, path=None):
        self.ax.clear()

        nx.draw(
            self.G,
            self.pos,
            ax=self.ax,
            node_size=10,
            edge_color="lightgray",
            node_color="black",
            alpha=0.6
        )

        if path:
            edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_nodes(
                self.G, self.pos,
                nodelist=path,
                node_color="red",
                node_size=40,
                ax=self.ax
            )
            nx.draw_networkx_edges(
                self.G, self.pos,
                edgelist=edges,
                edge_color="red",
                width=2,
                ax=self.ax
            )

        self.ax.set_title("Network Graph")
        self.ax.axis("off")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = RoutingUI(root)
    root.mainloop()
