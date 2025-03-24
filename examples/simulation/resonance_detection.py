# examples/simulation/resonance_detection.py

"""
Resonance Detection Simulation (AxAbsEnt Unified Theory)

Simulates the recursive evolution of a transfinite Absolute Entity chain
to detect resonance conditions based on:

- SDI growth rate
- Vector direction convergence
- Emergent field amplitude spikes

Resonance is defined by:
- Sudden increase in curvature entropy (SDI)
- Directional oscillation collapse (convergence to fixed point)
- Emergence amplitude above resonance threshold

Suitable for falsifiability testing and force resonance prediction.
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Initialize recursive transfinite chain
# ----------------------------

CHAIN_LENGTH = 30
DIM = 3
AMPLITUDE_THRESHOLD = 15.0  # Resonance spike trigger

def generate_resonant_chain(n=CHAIN_LENGTH, dim=DIM):
    return [
        AbsoluteEntity(
            signature=np.diag(np.sin(np.linspace(0, np.pi, dim)) + np.random.normal(0, 0.01, dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

absolutes = generate_resonant_chain()
print(f"🎼 Initialized {CHAIN_LENGTH}-step Absolute Chain for Resonance Detection\n")


# ----------------------------
# Step 2: Define mediator interaction
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a


# ----------------------------
# Step 3: Simulate recursive propagation and detect resonance
# ----------------------------

state = absolutes[0].state.copy()
sdi_trace = 0.0
last_direction = state.flatten() / (np.linalg.norm(state) + 1e-12)

resonance_triggered = False

for i in range(len(absolutes) - 1):
    a = absolutes[i]
    b = absolutes[i + 1]

    mediator = compose_mediator(a.signature, b.signature)
    state = mediator @ state
    entropy_core = mediator @ mediator.T
    decay = np.trace(entropy_core) / ((i + 1) ** 2)
    sdi_trace += decay

    norm = np.linalg.norm(state) + 1e-12
    current_direction = state.flatten() / norm

    alignment = np.dot(last_direction, current_direction)
    last_direction = current_direction

    # Resonance detection logic
    if norm > AMPLITUDE_THRESHOLD and alignment > 0.99:
        resonance_triggered = True
        print(f"🔔 Resonance Detected at Step {i + 1}")
        print(f"Alignment: {alignment:.6f} | Amplitude: {norm:.6f}")
        break

# ----------------------------
# Step 4: Output final result
# ----------------------------

if not resonance_triggered:
    print("❌ No Resonance Detected")
    print(f"Final Alignment: {alignment:.6f}")
    print(f"Final Amplitude: {norm:.6f}")

print(f"\n🧠 Total SDI Trace Accumulated: {sdi_trace:.6f}")
