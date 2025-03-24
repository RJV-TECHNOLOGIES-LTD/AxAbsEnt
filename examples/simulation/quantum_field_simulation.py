# examples/simulation/quantum_field_simulation.py

"""
Quantum Field Simulation (AxAbsEnt Unified Theory)

Simulates emergent quantum fields across a spatial lattice of Absolute Entities.

Models:
- Grid of absolutes (quantum vacuum substrate)
- Cross-absolute interaction through lattice coherence
- Entropy-core propagation at node intersections
- Emergent field vector as quantum field excitation

Output:
- Field amplitude
- Coherence direction vector
- Total SDI trace across the field

Forms the foundation of emergent quantum vacuum modeling.
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Create lattice grid of Absolute Entities
# ----------------------------

GRID_SIZE = 4  # 4x4 quantum substrate
DIM = 3

def generate_field_grid(size=GRID_SIZE, dim=DIM):
    return np.array([
        [AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        ) for _ in range(size)]
        for _ in range(size)
    ])

field_grid = generate_field_grid()
print(f"🧩 Initialized {GRID_SIZE}x{GRID_SIZE} Absolute Entity Quantum Grid\n")


# ----------------------------
# Step 2: Define mediator and entropy-core operations
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a


# ----------------------------
# Step 3: Propagate entropy across the lattice
# ----------------------------

sdi_trace_total = 0.0
field_state = np.zeros((DIM, 1))

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        entity = field_grid[i][j]
        neighbors = []

        if i > 0: neighbors.append(field_grid[i - 1][j])
        if i < GRID_SIZE - 1: neighbors.append(field_grid[i + 1][j])
        if j > 0: neighbors.append(field_grid[i][j - 1])
        if j < GRID_SIZE - 1: neighbors.append(field_grid[i][j + 1])

        for neighbor in neighbors:
            mediator = compose_mediator(entity.signature, neighbor.signature)
            field_state += mediator @ (entity.state + neighbor.state)
            entropy_core = mediator @ mediator.T
            sdi_trace_total += np.trace(entropy_core) / (1 + len(neighbors))

print(f"🧠 Total SDI Trace Across Quantum Field: {sdi_trace_total:.6f}")


# ----------------------------
# Step 4: Normalize emergent quantum field vector
# ----------------------------

norm = np.linalg.norm(field_state) + 1e-12
field_vector = field_state.flatten() / norm

# ----------------------------
# Step 5: Output result
# ----------------------------

print(f"\n🌀 Emergent Quantum Field Vector:")
print(f"Direction: {np.round(field_vector, 6).tolist()}")
print(f"Amplitude: {norm:.6f}")
