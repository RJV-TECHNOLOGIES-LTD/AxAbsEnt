# examples/complete/theory_to_experiment.py

"""
Theory to Experiment: Cross-Absolute Interaction Simulation

Simulates a full cross-absolute interaction pipeline using the AxAbsEnt framework
and produces measurable experimental signatures:

- Total entropy-core trace
- Emergent force vector
- Predicted observable parameters (e.g., amplitude, direction)

This file bridges theoretical constructs with experimental expectations,
demonstrating falsifiability of the Enhanced Mathematical Ontology of Absolute Nothingness.
"""

import numpy as np
import json
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Create absolute entities
# ----------------------------

def create_entity_chain(count=6, dim=3):
    return [
        AbsoluteEntity(
            signature=np.diag(np.random.rand(dim)),
            state=np.random.rand(dim, 1)
        )
        for _ in range(count)
    ]

absolutes = create_entity_chain()
print(f"🔬 Created {len(absolutes)} absolute entities\n")


# ----------------------------
# Step 2: Construct mediators and simulate interaction
# ----------------------------

def compose_mediator(sig_a, sig_b):
    return sig_a @ sig_b + sig_b @ sig_a

entropy_trace_sum = 0
state = absolutes[0].state

for i in range(len(absolutes) - 1):
    a, b = absolutes[i], absolutes[i + 1]
    mediator = compose_mediator(a.signature, b.signature)

    # Apply mediation to current state
    state = mediator @ state

    # Compute entropy-core trace (selection pressure)
    entropy_core = mediator @ mediator.T
    decay_weight = 1 / ((i + 1) ** 2)  # ordinal decay
    entropy_trace_sum += np.trace(entropy_core) * decay_weight


# ----------------------------
# Step 3: Derive experimental signature
# ----------------------------

def derive_experimental_signature(state_vector):
    norm = np.linalg.norm(state_vector) + 1e-10
    direction = state_vector.flatten() / norm
    amplitude = norm
    return {
        "force_direction": direction.tolist(),
        "force_amplitude": float(amplitude),
        "force_vector": state_vector.flatten().tolist()
    }

signature = derive_experimental_signature(state)


# ----------------------------
# Step 4: Create experimental output JSON
# ----------------------------

experiment_result = {
    "absolutes_count": len(absolutes),
    "signature_dimension": absolutes[0].signature.shape[0],
    "selection_entropy_scalar": float(entropy_trace_sum),
    "emergent_signature": signature,
    "theoretical_model": "Enhanced Mathematical Ontology of Absolute Nothingness",
    "experimental_version": "v1.0",
    "validation_ready": True
}

# Optionally export to file
output_path = "data/experimental/cross_absolute_test_result.json"
with open(output_path, "w") as f:
    json.dump(experiment_result, f, indent=4)

# ----------------------------
# Step 5: Output summary
# ----------------------------

print("📡 Theory-to-Experiment Signature Generated:")
print(f"Entropy Scalar:  {experiment_result['selection_entropy_scalar']:.6f}")
print(f"Force Amplitude: {signature['force_amplitude']:.6f}")
print(f"Force Direction: {signature['force_direction']}")
print(f"\n🧪 Output Saved: {output_path}")
