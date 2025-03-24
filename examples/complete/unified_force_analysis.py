# examples/complete/unified_force_analysis.py

"""
Unified Force Analysis: From Interaction Chains to Force Differentiation

This script simulates cross-absolute interaction recursion and
decomposes the resulting emergent force into four observable force components:

1. Gravity
2. Electromagnetic
3. Strong
4. Weak

Force decomposition follows the theoretical prescription of:
- Tensor projection of entropy-core via predefined coupling selectors
- Scalar normalization using the symmetry decay trace (SDI)
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Create absolutes for transfinite interaction chain
# ----------------------------

def generate_chain(n=10, dim=4):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

absolutes = generate_chain()
print(f"✅ Created {len(absolutes)} Absolute Entities\n")

# ----------------------------
# Step 2: Compose mediators and project through chain
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

state = absolutes[0].state
sdi_trace_total = 0.0

for i in range(len(absolutes) - 1):
    a, b = absolutes[i], absolutes[i + 1]
    mediator = compose_mediator(a.signature, b.signature)
    state = mediator @ state

    entropy_core = mediator @ mediator.T
    weight = 1 / ((i + 1) ** 2)
    sdi_trace_total += np.trace(entropy_core) * weight

print(f"🧠 Total SDI Trace: {sdi_trace_total:.6f}")

# ----------------------------
# Step 3: Force Differentiation via Coupling Selectors
# ----------------------------

def force_decomposition(force_vector, selector_matrix):
    """
    Projects the emergent force onto a given coupling selector matrix.
    """
    return selector_matrix @ force_vector

dim = state.shape[0]
norm_force = state / (np.linalg.norm(state) + 1e-12)

# Define idealized coupling selectors
gravity_selector         = np.eye(dim) * 0.01
electromagnetic_selector = np.eye(dim) * 0.3
strong_selector          = np.eye(dim) * 0.6
weak_selector            = np.eye(dim) * 0.09

# Project emergent force
gravity_force         = force_decomposition(norm_force, gravity_selector)
electromagnetic_force = force_decomposition(norm_force, electromagnetic_selector)
strong_force          = force_decomposition(norm_force, strong_selector)
weak_force            = force_decomposition(norm_force, weak_selector)

# ----------------------------
# Step 4: Report Final Result
# ----------------------------

def report(name, vec):
    print(f"\n💥 {name} Force:")
    print(f"Vector:  {vec.flatten().tolist()}")
    print(f"Norm:    {np.linalg.norm(vec):.6f}")

report("Gravitational", gravity_force)
report("Electromagnetic", electromagnetic_force)
report("Strong", strong_force)
report("Weak", weak_force)
