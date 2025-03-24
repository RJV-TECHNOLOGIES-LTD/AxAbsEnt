# examples/forces/force_extraction.py

"""
Force Extraction (AxAbsEnt Unified Theory)

This script simulates the full extraction of a unified force
from an interaction chain of Absolute Entities using the
entropy-core symmetry decay projection (SDI-based extraction).

Result:
- Normalized emergent force vector
- Scalar energy measure (trace)
- Ready for force decomposition or experiment mapping
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Generate a transfinite chain of Absolute Entities
# ----------------------------

def create_force_chain(n=8, dim=4):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

absolutes = create_force_chain()
dim = absolutes[0].signature.shape[0]

print(f"🧱 Created {len(absolutes)} Absolute Entities for Force Extraction\n")


# ----------------------------
# Step 2: Define mediator composition and entropy-core propagation
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

state = absolutes[0].state
sdi_trace_total = 0.0

for i in range(len(absolutes) - 1):
    a = absolutes[i]
    b = absolutes[i + 1]
    mediator = compose_mediator(a.signature, b.signature)

    state = mediator @ state

    entropy_core = mediator @ mediator.T
    decay_weight = 1 / ((i + 1) ** 2)
    sdi_trace_total += np.trace(entropy_core) * decay_weight

print(f"🧠 SDI Trace Accumulated: {sdi_trace_total:.6f}")


# ----------------------------
# Step 3: Extract unified force vector
# ----------------------------

def extract_force_vector(projected_state):
    """
    Normalizes and returns the emergent force vector.
    """
    norm = np.linalg.norm(projected_state) + 1e-12
    return (projected_state / norm).flatten().tolist(), float(norm)

force_vector, force_magnitude = extract_force_vector(state)

# ----------------------------
# Step 4: Output Result
# ----------------------------

print("\n💥 Unified Force Extracted:")
print(f"Direction Vector: {np.round(force_vector, 6).tolist()}")
print(f"Total Amplitude:  {force_magnitude:.6f}")
