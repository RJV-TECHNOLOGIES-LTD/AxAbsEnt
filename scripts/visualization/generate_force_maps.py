# scripts/visualization/generate_force_maps.py

"""
Generate Force Maps (AxAbsEnt Unified Theory)

Generates 2D visual maps of emergent force fields across a spatial grid
of Absolute Entities. Each vector is computed from mediator interactions
and plotted with:

- Arrow direction = emergent field vector
- Arrow length / color = entropy-core amplitude
- Background shading = force magnitude field

Outputs plots to results/diagrams/force_map.png
"""

import numpy as np
import matplotlib.pyplot as plt
from axabsent.core.absolute import AbsoluteEntity
import os

# ----------------------------
# Configuration
# ----------------------------

GRID_SIZE = 10
DIM = 2  # For 2D vector field rendering
OUTPUT_PATH = "results/diagrams/force_map.png"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)


# ----------------------------
# Create Entity Grid
# ----------------------------

def generate_grid_entities(size=GRID_SIZE, dim=DIM):
    return np.array([
        [AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        ) for _ in range(size)]
        for _ in range(size)
    ])

entities = generate_grid_entities()
print(f"🌐 Generated {GRID_SIZE}x{GRID_SIZE} Absolute Entity Grid")


# ----------------------------
# Force Computation via Mediators
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

X, Y = np.meshgrid(np.arange(GRID_SIZE), np.arange(GRID_SIZE))
U = np.zeros_like(X, dtype=float)
V = np.zeros_like(Y, dtype=float)
AMP = np.zeros_like(X, dtype=float)

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        current = entities[i][j]
        neighbors = []

        if i > 0: neighbors.append(entities[i - 1][j])
        if i < GRID_SIZE - 1: neighbors.append(entities[i + 1][j])
        if j > 0: neighbors.append(entities[i][j - 1])
        if j < GRID_SIZE - 1: neighbors.append(entities[i][j + 1])

        vector = np.zeros((DIM, 1))

        for neighbor in neighbors:
            mediator = compose_mediator(current.signature, neighbor.signature)
            vector += mediator @ (current.state + neighbor.state)

        norm = np.linalg.norm(vector) + 1e-12
        unit_vector = (vector / norm).flatten()
        U[i, j] = unit_vector[0]
        V[i, j] = unit_vector[1]
        AMP[i, j] = norm


# ----------------------------
# Plot Force Map
# ----------------------------

plt.figure(figsize=(9, 8))
plt.title("🧲 Emergent Force Map (AxAbsEnt Unified Theory)", fontsize=14)

# Background = force amplitude field
plt.imshow(AMP, origin="lower", cmap="magma", extent=[0, GRID_SIZE, 0, GRID_SIZE], alpha=0.7)

# Arrows = force vectors
plt.quiver(X, Y, U, V, color='white', scale=25, width=0.003)

plt.xlabel("X (Grid Index)")
plt.ylabel("Y (Grid Index)")
plt.colorbar(label="Force Amplitude")
plt.grid(True, linestyle='--', linewidth=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
plt.close()

print(f"✅ Force map saved to {OUTPUT_PATH}")
