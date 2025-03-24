# examples/visualization/information_flow_diagram.py

"""
Information Flow Diagram (AxAbsEnt Unified Theory)

Visualizes directional information propagation between a set of Absolute Entities.

Features:
- Directed graph representation
- Edge width = entropy flow magnitude
- Edge direction = net informational displacement
- Node size = local state amplitude

Foundation for modeling entangled information networks and curvature-mediated information transfer.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Define a small network of Absolute Entities
# ----------------------------

NUM_ENTITIES = 6
DIM = 3

def create_entities(n=NUM_ENTITIES, dim=DIM):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        ) for _ in range(n)
    ]

entities = create_entities()
print(f"🧠 Created {NUM_ENTITIES} Absolute Entities for Information Flow Analysis\n")


# ----------------------------
# Step 2: Compute directional entropy propagation (information flow)
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

G = nx.DiGraph()

for i in range(NUM_ENTITIES):
    G.add_node(i)

for i in range(NUM_ENTITIES):
    for j in range(NUM_ENTITIES):
        if i == j:
            continue
        a = entities[i]
        b = entities[j]

        mediator = compose_mediator(a.signature, b.signature)
        entropy_tensor = mediator @ mediator.T
        information_flow_strength = float(np.trace(entropy_tensor))

        # Use dot product to determine net displacement direction
        flow_direction = np.dot((b.state - a.state).flatten(), (mediator @ a.state).flatten())
        if flow_direction > 0:
            G.add_edge(i, j, weight=information_flow_strength)


# ----------------------------
# Step 3: Visualize the graph
# ----------------------------

pos = nx.circular_layout(G)
weights = [G[u][v]['weight'] for u, v in G.edges()]
node_sizes = [np.linalg.norm(e.state) * 1000 for e in entities]

plt.figure(figsize=(8, 8))
plt.title("🔄 Information Flow Between Absolute Entities", fontsize=14)

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', edgecolors='black')
nx.draw_networkx_edges(G, pos, width=[w / 5 for w in weights], arrows=True, arrowstyle='-|>', edge_color='gray')
nx.draw_networkx_labels(G, pos, font_size=10)

plt.axis('off')
plt.tight_layout()
plt.show()
