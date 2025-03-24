# examples/complete/full_analysis_pipeline.py

"""
Full Analysis Pipeline

This script executes the full AxAbsEnt analytical sequence:
1. Instantiates a chain of Absolute Entities
2. Composes pairwise interaction tensors
3. Constructs mediators for each pair
4. Propagates through a transfinite mediation chain
5. Computes entropy-core scalar (selection minimization)
6. Derives emergent force vector via recursive decay

Result: Emergent force projection from cross-absolute interaction dynamics.
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Generate Absolute Entities
# ----------------------------

def generate_absolutes(n=8, dim=3):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

absolutes = generate_absolutes()
print(f"✅ Created {len(absolutes)} Absolute Entities\n")

# ----------------------------
# Step 2: Compose Pairwise Interactions
# ----------------------------

def compose_interaction_tensor(a: AbsoluteEntity, b: AbsoluteEntity):
    return a.signature @ b.signature + b.signature @ a.signature

interactions = [
    compose_interaction_tensor(absolutes[i], absolutes[i + 1])
    for i in range(len(absolutes) - 1)
]

print(f"🔗 Composed {len(interactions)} interaction tensors")

# ----------------------------
# Step 3: Build Mediators & Entropy Core Traces
# ----------------------------

mediator_entropy_traces = []
state = absolutes[0].state

for idx, mediator in enumerate(interactions):
    entropy_core = mediator @ mediator.T
    decay_weight = 1 / ((idx + 1) ** 2)
    mediator_entropy_traces.append(np.trace(entropy_core) * decay_weight)
    state = mediator @ state

total_entropy_scalar = sum(mediator_entropy_traces)

print(f"\n🧠 Total Selection-Minimizing Entropy Scalar: {total_entropy_scalar:.6f}")

# ----------------------------
# Step 4: Force Emergence Proxy
# ----------------------------

def derive_emergent_force(state_vector):
    """
    Approximates emergent force vector by normalizing final projected state.
    """
    force_vector = state_vector / (np.linalg.norm(state_vector) + 1e-12)
    return force_vector

force = derive_emergent_force(state)

print(f"\n💥 Emergent Force Vector:")
print(force)

# ----------------------------
# Step 5: Summary
# ----------------------------

print("\n🧾 Pipeline Summary:")
print(f"Entities:       {len(absolutes)}")
print(f"Mediators:      {len(interactions)}")
print(f"Entropy Scalar: {total_entropy_scalar:.6f}")
print(f"Force Norm:     {np.linalg.norm(force):.4f}")
