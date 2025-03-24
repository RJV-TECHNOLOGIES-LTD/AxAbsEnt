# examples/simulation/dynamic_evolution.py

"""
Dynamic Evolution Simulation (AxAbsEnt Unified Theory)

Simulates time-resolved evolution of a system of Absolute Entities,
showing:

- Recursive mediation at each time step
- State vector update via entropy-core propagation
- Directional drift of emergent field vector
- Accumulated entropy trace (SDI dynamics)

Captures how evolving cross-absolute interactions shape force curvature over time.
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Initialize a dynamic absolute system
# ----------------------------

def initialize_entities(n=6, dim=3):
    """
    Creates an initial set of Absolute Entities with random states and signatures.
    """
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

absolutes = initialize_entities()
dim = absolutes[0].signature.shape[0]
print(f"🧩 Initialized {len(absolutes)} dynamic Absolute Entities\n")


# ----------------------------
# Step 2: Define entropy-based mediator evolution
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a


# ----------------------------
# Step 3: Run dynamic simulation across T time steps
# ----------------------------

T = 10  # Simulation steps
state = absolutes[0].state.copy()
sdi_trace_total = 0.0
direction_log = []

print("📈 Starting Dynamic Evolution:\n")

for t in range(1, T + 1):
    index_a = (t - 1) % len(absolutes)
    index_b = t % len(absolutes)

    a = absolutes[index_a]
    b = absolutes[index_b]

    mediator = compose_mediator(a.signature, b.signature)
    state = mediator @ state

    entropy_core = mediator @ mediator.T
    decay = np.trace(entropy_core) / (t ** 2)
    sdi_trace_total += decay

    direction = state.flatten() / (np.linalg.norm(state) + 1e-12)
    direction_log.append(np.round(direction, 6).tolist())

    print(f"Step {t:2d} | SDI+{decay:.6f} | Dir: {direction.tolist()}")


# ----------------------------
# Step 4: Final result
# ----------------------------

norm_final = np.linalg.norm(state)
final_vector = state.flatten() / (norm_final + 1e-12)

print(f"\n🧠 Total SDI Trace Accumulated: {sdi_trace_total:.6f}")
print(f"📡 Final Emergent Vector Direction: {np.round(final_vector, 6).tolist()}")
print(f"⚡ Final Amplitude: {norm_final:.6f}")
