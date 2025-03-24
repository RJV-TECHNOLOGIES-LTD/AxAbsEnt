# examples/visualization/interaction_graph_plotting.py

"""
Interaction Graph Plotting (AxAbsEnt Unified Theory)

Visualizes the network of cross-absolute interactions between a collection of
Absolute Entities using entropy-core weighted edges.

Graph encodes:
- Nodes: Absolute Entities
- Edges: Interaction connections
- Edge weights: Entropy-core trace magnitude (strength of interaction)
- Layout: Force-directed spatial layout based on interaction tension
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Initialize interaction group
# ----------------------------

NUM_ENTITIES = 8
DIM = 3

def create_entities(n=NUM_ENTITIES, dim=DIM):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

entities = create_entities()
print(f"🌐 Initialized {NUM_ENTITIES} Absolute Entities for Interaction Mapping\n")


# ----------------------------
# Step 2: Build weighted interaction graph
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

G = nx.Graph()

for i in range(NUM_ENTITIES):
    G.add_node(i)

for i in range(NUM_ENTITIES):
    for j in range(i + 1, NUM_ENTITIES):
        a = entities[i]
        b = entities[j]
        mediator = compose_mediator(a.signature, b.signature)
        entropy_core = mediator @ mediator.T
        weight = np.trace(entropy_core)

        G.add_edge(i, j, weight=weight)

weights = [G[u][v]['weight'] for u, v in G.edges()]
scaled_weights = [w / max(weights) * 5 for w in weights]


# ----------------------------
# Step 3: Plot graph using force-directed layout
# ----------------------------

pos = nx.spring_layout(G, seed=42)  # Force-directed based on weights

plt.figure(figsize=(9, 7))
plt.title("🕸️ Cross-Absolute Interaction Graph", fontsize=14)

nx.draw_networkx_nodes(G, pos, node_size=800, node_color='skyblue', edgecolors='black')
nx.draw_networkx_edges(G, pos, width=scaled_weights, edge_color='purple', alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.axis('off')
plt.tight_layout()
plt.show()
