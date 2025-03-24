# examples/basic/transfinite_chain_analysis.py

"""
Example: Transfinite Chain Analysis Across Absolutes

This script simulates the formation of a transfinite chain of
Absolute Entities, linked via recursive mediator tensors, and computes
the overall entropy decay trace across all mediator layers.

It mimics:
- Ordinal-indexed mediation layering
- Symmetry Decay Index (SDI) projection behavior
- Transfinite topology collapse effects

Requires:
- src.axabsent.core.absolute.AbsoluteEntity
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Generate a transfinite list of absolutes
# ----------------------------

def generate_absolutes_chain(length=10, dimension=3):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dimension)),
            state=np.random.rand(dimension, 1)
        )
        for _ in range(length)
    ]

absolutes = generate_absolutes_chain()

print(f"🔗 Created {len(absolutes)} Absolute Entities for Transfinite Chain")

# ----------------------------
# Step 2: Define mediator constructor
# ----------------------------

def compose_mediator(sig_a: np.ndarray, sig_b: np.ndarray) -> np.ndarray:
    return sig_a @ sig_b + sig_b @ sig_a

# ----------------------------
# Step 3: Recursive chain propagation
# ----------------------------

def propagate_transfinite_chain(absolutes):
    entropy_trace_total = 0.0
    state_propagation = absolutes[0].state

    for i in range(len(absolutes) - 1):
        a = absolutes[i]
        b = absolutes[i + 1]

        mediator = compose_mediator(a.signature, b.signature)
        state_propagation = mediator @ state_propagation

        entropy_core = mediator @ mediator.T
        trace_contribution = np.trace(entropy_core)
        entropy_trace_total += trace_contribution / ((i + 1) ** 2)  # ordinal decay

        print(f"Step {i+1}: Trace = {trace_contribution:.4f} | Ordinal decay applied")

    return entropy_trace_total, state_propagation

# ----------------------------
# Step 4: Execute propagation
# ----------------------------

final_trace, final_state = propagate_transfinite_chain(absolutes)

print("\n🧠 Transfinite Entropy Scalar (Total Decayed Trace):")
print(final_trace)

print("\n📡 Final Propagated State:")
print(final_state)
