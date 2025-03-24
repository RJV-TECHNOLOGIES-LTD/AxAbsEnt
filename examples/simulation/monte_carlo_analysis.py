# examples/simulation/monte_carlo_analysis.py

"""
Monte Carlo Analysis of Emergent Forces (AxAbsEnt Unified Theory)

This script runs a Monte Carlo simulation of multiple randomized Absolute Entity chains
to statistically characterize:

- SDI entropy trace distribution
- Emergent force amplitude variation
- Vector alignment patterns (e.g. directional clustering)

Provides statistical insights into the stochastic structure of force emergence
in the unified cross-absolute interaction model.
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Monte Carlo configuration
# ----------------------------

NUM_TRIALS = 1000
CHAIN_LENGTH = 6
DIM = 3

sdi_traces = []
amplitudes = []
vector_log = []


# ----------------------------
# Step 2: Core sampling logic
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

def generate_random_chain(n=CHAIN_LENGTH, dim=DIM):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(n)
    ]

def run_single_trial():
    entities = generate_random_chain()
    state = entities[0].state.copy()
    sdi_trace = 0.0

    for i in range(len(entities) - 1):
        a = entities[i]
        b = entities[i + 1]
        mediator = compose_mediator(a.signature, b.signature)
        state = mediator @ state
        entropy_core = mediator @ mediator.T
        sdi_trace += np.trace(entropy_core) / ((i + 1) ** 2)

    norm = np.linalg.norm(state) + 1e-12
    direction = (state / norm).flatten()

    return sdi_trace, norm, direction.tolist()


# ----------------------------
# Step 3: Run simulation
# ----------------------------

print(f"🎲 Running Monte Carlo Simulation: {NUM_TRIALS} trials\n")

for _ in range(NUM_TRIALS):
    sdi, amp, vec = run_single_trial()
    sdi_traces.append(sdi)
    amplitudes.append(amp)
    vector_log.append(vec)

sdi_traces = np.array(sdi_traces)
amplitudes = np.array(amplitudes)
vector_log = np.array(vector_log)


# ----------------------------
# Step 4: Statistical summaries
# ----------------------------

def summarize_distribution(name, array):
    print(f"📊 {name} Distribution:")
    print(f"  Mean:   {np.mean(array):.6f}")
    print(f"  Std:    {np.std(array):.6f}")
    print(f"  Min:    {np.min(array):.6f}")
    print(f"  Max:    {np.max(array):.6f}\n")

summarize_distribution("SDI Trace", sdi_traces)
summarize_distribution("Force Amplitude", amplitudes)


# ----------------------------
# Step 5: Vector field center (directional clustering)
# ----------------------------

average_vector = np.mean(vector_log, axis=0)
average_vector /= np.linalg.norm(average_vector) + 1e-12

print(f"🧭 Average Emergent Vector Direction:")
print(f"  {np.round(average_vector, 6).tolist()}")
