# examples/visualization/multidimensional_visualization.py

"""
Multidimensional Visualization (AxAbsEnt Unified Theory)

Projects high-dimensional emergent behavior from cross-absolute interactions
into 2D/3D space for:

- Visual falsifiability of force emergence
- SDI-based clustering
- Entropy-coherence pattern detection

Uses PCA for dimensionality reduction.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Create high-dimensional absolute chain
# ----------------------------

NUM_ENTITIES = 40
DIM = 6  # Multidimensional interaction space

def create_highdim_entities(n=NUM_ENTITIES, dim=DIM):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

entities = create_highdim_entities()
print(f"🔢 Created {NUM_ENTITIES} Absolute Entities in {DIM}D\n")


# ----------------------------
# Step 2: Simulate cumulative SDI projection across system
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

state_vectors = []
entropy_magnitudes = []

state = entities[0].state.copy()
sdi_total = 0.0

for i in range(NUM_ENTITIES - 1):
    a = entities[i]
    b = entities[i + 1]
    mediator = compose_mediator(a.signature, b.signature)
    state = mediator @ state
    entropy_core = mediator @ mediator.T
    decay = np.trace(entropy_core)
    sdi_total += decay

    state_vectors.append(state.flatten())
    entropy_magnitudes.append(decay)

state_matrix = np.array(state_vectors)
print(f"🧠 Total SDI Trace Across Chain: {sdi_total:.6f}")


# ----------------------------
# Step 3: Reduce dimensions using PCA
# ----------------------------

pca = PCA(n_components=2)
projected = pca.fit_transform(state_matrix)

x = projected[:, 0]
y = projected[:, 1]
colors = np.array(entropy_magnitudes)


# ----------------------------
# Step 4: Plot projection with SDI shading
# ----------------------------

plt.figure(figsize=(8, 6))
plt.title("🌌 Multidimensional Force Emergence Projection", fontsize=14)

scatter = plt.scatter(x, y, c=colors, cmap='plasma', s=60, edgecolors='black')
plt.xlabel("PCA Axis 1")
plt.ylabel("PCA Axis 2")
plt.colorbar(scatter, label="Entropy-Core Magnitude (SDI)")
plt.grid(True, linestyle='--', linewidth=0.3)
plt.tight_layout()
plt.show()
