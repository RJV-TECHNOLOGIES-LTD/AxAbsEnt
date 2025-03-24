# examples/simulation/cosmological_simulation.py

"""
Cosmological Simulation (AxAbsEnt Unified Theory)

Simulates the evolution of the early universe under cross-absolute interaction propagation.
Models the emergence of a large-scale cosmological field from transfinite recursive mediation.

Captures:
- Entropy propagation through a transfinite interaction chain
- Emergent vector simulating cosmic-scale force direction
- Scalar magnitude of universe-scale entropy decay
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Generate large cosmological chain of absolutes
# ----------------------------

def generate_cosmological_chain(n=32, dim=4):
    """
    Models a cosmological-scale entropy chain where each absolute represents
    a discrete early-universe mediation node in curvature collapse.
    """
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim) + 0.01),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

absolutes = generate_cosmological_chain()
print(f"🌌 Generated {len(absolutes)} cosmological Absolutes\n")


# ----------------------------
# Step 2: Recursive entropy propagation via mediator tensors
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

state = absolutes[0].state
sdi_trace = 0.0
decay_profile = []

for i in range(len(absolutes) - 1):
    a = absolutes[i]
    b = absolutes[i + 1]
    mediator = compose_mediator(a.signature, b.signature)
    state = mediator @ state
    entropy_core = mediator @ mediator.T
    decay = np.trace(entropy_core) / ((i + 1) ** 2)
    sdi_trace += decay
    decay_profile.append(decay)

print(f"🧠 Accumulated SDI Trace: {sdi_trace:.6f}")


# ----------------------------
# Step 3: Extract emergent cosmological vector
# ----------------------------

def extract_cosmological_vector(state_vector):
    norm = np.linalg.norm(state_vector) + 1e-12
    return state_vector.flatten() / norm, float(norm)

direction_vector, expansion_amplitude = extract_cosmological_vector(state)


# ----------------------------
# Step 4: Output simulation results
# ----------------------------

print("\n🌠 Emergent Cosmological Vector:")
print(f"Direction: {np.round(direction_vector, 6).tolist()}")
print(f"Amplitude: {expansion_amplitude:.6f}")
print(f"Entropy Gradient (initial → final): {np.round(decay_profile[0], 6)} → {np.round(decay_profile[-1], 6)}")
