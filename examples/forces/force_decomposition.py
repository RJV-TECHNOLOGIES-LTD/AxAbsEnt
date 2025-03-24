# examples/forces/force_decomposition.py

"""
Force Decomposition (AxAbsEnt Unified Model)

This script decomposes a given unified force vector into:
1. Gravitational Component
2. Electromagnetic Component
3. Strong Force Component
4. Weak Force Component

Each component is obtained via coupling selector matrices, which project
the force vector into the respective force subspaces.

All selectors are normalized for unitary projection under symmetry collapse.
"""

import numpy as np

# ----------------------------
# Step 1: Generate a sample unified force vector
# ----------------------------

def generate_unified_force(dim=4):
    """
    Simulates an emergent unified force vector.
    """
    vec = np.random.rand(dim, 1)
    return vec / (np.linalg.norm(vec) + 1e-12)

unified_force = generate_unified_force()
dim = unified_force.shape[0]

print("🧲 Unified Force Vector:")
print(unified_force.flatten().tolist())


# ----------------------------
# Step 2: Define coupling selector matrices
# ----------------------------

def get_selector_matrix(force_type: str, dim: int):
    """
    Returns an approximate coupling selector matrix for the given force type.
    """
    selectors = {
        "gravity":         np.eye(dim) * 0.01,
        "electromagnetic": np.eye(dim) * 0.3,
        "strong":          np.eye(dim) * 0.6,
        "weak":            np.eye(dim) * 0.09,
    }
    return selectors[force_type]

selector_gravity         = get_selector_matrix("gravity", dim)
selector_em              = get_selector_matrix("electromagnetic", dim)
selector_strong          = get_selector_matrix("strong", dim)
selector_weak            = get_selector_matrix("weak", dim)


# ----------------------------
# Step 3: Decompose force components
# ----------------------------

def project_force(selector, force_vector):
    """
    Projects force vector using the selector matrix and returns component + norm.
    """
    projected = selector @ force_vector
    norm = np.linalg.norm(projected)
    return projected.flatten(), norm

gravity_vector, gravity_amp         = project_force(selector_gravity, unified_force)
em_vector, em_amp                   = project_force(selector_em, unified_force)
strong_vector, strong_amp           = project_force(selector_strong, unified_force)
weak_vector, weak_amp               = project_force(selector_weak, unified_force)

total_amp = gravity_amp + em_amp + strong_amp + weak_amp


# ----------------------------
# Step 4: Report component-wise contributions
# ----------------------------

def report_component(name, vector, amp, total):
    pct = (amp / total) * 100 if total > 0 else 0
    print(f"\n🔹 {name} Force Component:")
    print(f"Vector: {np.round(vector, 6).tolist()}")
    print(f"Amplitude: {amp:.6f}")
    print(f"Contribution: {pct:.2f}%")

report_component("Gravitational", gravity_vector, gravity_amp, total_amp)
report_component("Electromagnetic", em_vector, em_amp, total_amp)
report_component("Strong", strong_vector, strong_amp, total_amp)
report_component("Weak", weak_vector, weak_amp, total_amp)

print(f"\n🧠 Total Unified Amplitude: {total_amp:.6f}")
