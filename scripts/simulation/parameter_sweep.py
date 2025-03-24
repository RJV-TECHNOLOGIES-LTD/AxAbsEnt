# scripts/simulation/parameter_sweep.py

"""
Parameter Sweep Simulation (AxAbsEnt Unified Theory)

Performs a systematic parameter sweep across:
- Absolute Entity signature scale
- Dimensionality of interaction space
- Number of chain steps

Records:
- Emergent field amplitude
- SDI entropy trace
- Alignment vector

Outputs structured data suitable for falsifiability, visualization, and optimization.
"""

import numpy as np
import pandas as pd
from axabsent.core.absolute import AbsoluteEntity

# ----------------------------
# Sweep Configuration
# ----------------------------

SIGNATURE_SCALES = [0.1, 0.5, 1.0]
DIMENSIONS = [2, 3, 4]
CHAIN_LENGTHS = [5, 10, 20]

SWEEP_RESULTS = []

np.random.seed(42)  # Reproducibility

# ----------------------------
# Mediator Composition Logic
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

# ----------------------------
# Simulation Execution
# ----------------------------

def run_simulation(dim, scale, steps):
    entities = [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim) * scale),
            state=np.random.rand(dim, 1)
        ) for _ in range(steps)
    ]

    state = entities[0].state.copy()
    sdi_trace = 0.0

    for i in range(len(entities) - 1):
        a = entities[i]
        b = entities[i + 1]
        mediator = compose_mediator(a.signature, b.signature)
        state = mediator @ state
        entropy_core = mediator @ mediator.T
        sdi_trace += np.trace(entropy_core) / ((i + 1) ** 2)

    amplitude = np.linalg.norm(state)
    direction = (state.flatten() / (amplitude + 1e-12)).tolist()

    return sdi_trace, amplitude, direction

# ----------------------------
# Run Sweep Across All Configurations
# ----------------------------

print(f"🔄 Running AxAbsEnt Parameter Sweep...\n")

for dim in DIMENSIONS:
    for scale in SIGNATURE_SCALES:
        for steps in CHAIN_LENGTHS:
            sdi, amp, vec = run_simulation(dim, scale, steps)
            SWEEP_RESULTS.append({
                "dimension": dim,
                "signature_scale": scale,
                "chain_length": steps,
                "sdi_trace": sdi,
                "amplitude": amp,
                "direction_vector": vec
            })
            print(f"✅ dim={dim}, scale={scale}, steps={steps} → amplitude={amp:.4f}, SDI={sdi:.4f}")

# ----------------------------
# Export Results
# ----------------------------

df = pd.DataFrame(SWEEP_RESULTS)
df.to_csv("results/parameter_sweep_results.csv", index=False)

print(f"\n📁 Results exported to results/parameter_sweep_results.csv")
