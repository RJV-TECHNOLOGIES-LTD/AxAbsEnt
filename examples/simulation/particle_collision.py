# examples/simulation/particle_collision.py

"""
Particle Collision Simulation (AxAbsEnt Unified Model)

Simulates a single particle collision event based on cross-absolute
interaction collapse:

- Pre-collision symmetry profile (two Absolute Entities)
- Mediator composition and entropy-core tracing
- Post-collision emergent force direction and scalar amplitude
- Suitable for falsifiability against collider data

This forms the simulation core for the experimental predictions pipeline.
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Define colliding absolute entities
# ----------------------------

def create_collision_pair(dim=4):
    """
    Constructs two Absolute Entities to simulate particle impact dynamics.
    """
    a = AbsoluteEntity(signature=np.diag(np.random.rand(dim)))
    b = AbsoluteEntity(signature=np.diag(np.random.rand(dim)))
    a.state = np.random.rand(dim, 1)
    b.state = np.random.rand(dim, 1)
    return a, b

entity_A, entity_B = create_collision_pair()
print("💥 Initialized Pre-Collision Entities\n")


# ----------------------------
# Step 2: Construct mediator tensor and compute entropy-core
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

mediator = compose_mediator(entity_A.signature, entity_B.signature)
entropy_core = mediator @ mediator.T
entropy_scalar = float(np.trace(entropy_core))
print(f"🧠 Entropy-Core Trace: {entropy_scalar:.6f}")


# ----------------------------
# Step 3: Simulate post-collision emergent field
# ----------------------------

def simulate_recoil_force(mediator_tensor, a_state, b_state):
    combined = a_state + b_state
    impulse = mediator_tensor @ combined
    norm = np.linalg.norm(impulse) + 1e-12
    return impulse.flatten() / norm, float(norm)

recoil_vector, amplitude = simulate_recoil_force(mediator, entity_A.state, entity_B.state)


# ----------------------------
# Step 4: Output result
# ----------------------------

print(f"\n🎯 Post-Collision Emergent Force:")
print(f"Direction Vector: {np.round(recoil_vector, 6).tolist()}")
print(f"Scalar Amplitude: {amplitude:.6f}")
