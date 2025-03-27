# scripts/visualization/create_interaction_diagrams.py

"""
Create Cross-Absolute Interaction Diagrams (AxAbsEnt Unified Theory)

Generates weighted interaction network diagrams between Absolute Entities.
Visual encodings include:

- Node size: state norm
- Edge thickness: entropy-core trace (SDI)
- Layout: force-directed graph from entropy tension
- Color intensity: signature scale or information propagation strength

Saves output images to /results/diagrams/.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os
from axabsent.core.absolute import AbsoluteEntity

# ----------------------------
# Configuration
# ----------------------------

NUM_ENTITIES = 12
DIM = 3
OUTPUT_PATH = "results/diagrams/interaction_graph.png"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# ----------------------------
# Initialize Absolute Entities
# ----------------------------

def create_entities(n=NUM_ENTITIES, dim=DIM):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

entities = create_entities()
print(f"🌐 Initialized {NUM_ENTITIES} Absolute Entities")


# ----------------------------
# Build Interaction Graph
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

G = nx.Graph()

for i in range(NUM_ENTITIES):
    G.add_node(i, size=np.linalg.norm(entities[i].state))

for i in range(NUM_ENTITIES):
    for j in range(i + 1, NUM_ENTITIES):
        a = entities[i]
        b = entities[j]
        mediator = compose_mediator(a.signature, b.signature)
        entropy_core = mediator @ mediator.T
        trace = np.trace(entropy_core)
        if trace > 0:
            G.add_edge(i, j, weight=trace)

# ----------------------------
# Draw Diagram
# ----------------------------

pos = nx.spring_layout(G, seed=42)
weights = [G[u][v]['weight'] for u, v in G.edges()]
sizes = [G.nodes[n]['size'] * 500 for n in G.nodes]

plt.figure(figsize=(10, 8))
plt.title("🔗 Cross-Absolute Interaction Diagram", fontsize=14)

nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color='skyblue', edgecolors='black')
nx.draw_networkx_edges(G, pos, width=[w / max(weights) * 5 for w in weights], edge_color='purple', alpha=0.7)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.axis('off')
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
plt.close()

print(f"✅ Diagram saved to: {OUTPUT_PATH}")
