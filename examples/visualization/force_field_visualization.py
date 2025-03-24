# examples/visualization/force_field_visualization.py

"""
Force Field Visualization (AxAbsEnt Unified Model)

This script visualizes emergent force vectors across a 2D grid
of Absolute Entities using AxAbsEnt's entropy-core collapse model.

Outputs:
- Quiver plot of directional force field
- Background color map indicating amplitude of force at each point
"""

import numpy as np
import matplotlib.pyplot as plt
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Generate a 2D spatial grid of Absolute Entities
# ----------------------------

GRID_SIZE = 10
DIM = 2  # 2D vector field for plotting

def generate_grid_entities(size=GRID_SIZE, dim=DIM):
    return np.array([
        [AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        ) for _ in range(size)]
        for _ in range(size)
    ])

grid = generate_grid_entities()
print(f"🌐 Generated {GRID_SIZE}x{GRID_SIZE} Absolute Entity grid\n")


# ----------------------------
# Step 2: Define mediator logic and field vector computation
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

X, Y = np.meshgrid(np.arange(GRID_SIZE), np.arange(GRID_SIZE))
U = np.zeros_like(X, dtype=float)
V = np.zeros_like(Y, dtype=float)
AMP = np.zeros_like(X, dtype=float)

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        current = grid[i][j]
        neighbors = []

        if i > 0: neighbors.append(grid[i - 1][j])
        if i < GRID_SIZE - 1: neighbors.append(grid[i + 1][j])
        if j > 0: neighbors.append(grid[i][j - 1])
        if j < GRID_SIZE - 1: neighbors.append(grid[i][j + 1])

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
# Step 3: Plot quiver force field
# ----------------------------

plt.figure(figsize=(8, 8))
plt.title("🧲 Emergent Force Field (AxAbsEnt)", fontsize=14)

# Background magnitude field
plt.imshow(AMP, origin="lower", cmap="viridis", extent=[0, GRID_SIZE, 0, GRID_SIZE], alpha=0.6)

# Force vector field (quiver)
plt.quiver(X, Y, U, V, color='white', scale=25, width=0.003)

plt.xlabel("X (Entity Index)")
plt.ylabel("Y (Entity Index)")
plt.colorbar(label="Force Amplitude")
plt.grid(True, linestyle='--', linewidth=0.3)
plt.tight_layout()
plt.show()
