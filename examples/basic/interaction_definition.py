# examples/basic/interaction_definition.py

"""
Example: Defining Interactions Between Absolute Entities

This script demonstrates the composition of an interaction tensor
between two AbsoluteEntity instances based on their properties and
signature alignment in the AxAbsEnt ontology.

Requires:
- src.axabsent.core.absolute.AbsoluteEntity
- src.axabsent.core.interaction (if extended)
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity


# ----------------------------
# Step 1: Create two absolutes
# ----------------------------

abs_a = AbsoluteEntity()
abs_b = AbsoluteEntity()

# Give each a waveform-like vector property
abs_a.set_property("waveform", np.array([0.6, 0.2, 0.2]))
abs_b.set_property("waveform", np.array([0.1, 0.7, 0.2]))

# Expand their signature matrices to match property dimensionality
abs_a.signature = np.diag(abs_a.get_property("waveform"))
abs_b.signature = np.diag(abs_b.get_property("waveform"))

print("✅ Absolute Entities Created")
print(f"Abs A Signature:\n{abs_a.signature}")
print(f"Abs B Signature:\n{abs_b.signature}")

# ----------------------------
# Step 2: Define the interaction tensor
# ----------------------------

def compose_interaction_tensor(sig_a: np.ndarray, sig_b: np.ndarray) -> np.ndarray:
    """
    Symmetric composition of two signature matrices into an interaction tensor.
    Emulates entropy-core linking before force decomposition.
    """
    return sig_a @ sig_b + sig_b @ sig_a

interaction_tensor = compose_interaction_tensor(abs_a.signature, abs_b.signature)

print("\n🔗 Interaction Tensor Constructed:")
print(interaction_tensor)

# ----------------------------
# Step 3: Compute interaction entropy core trace
# ----------------------------

entropy_core = interaction_tensor @ interaction_tensor.T
selection_trace = np.trace(entropy_core)

print("\n🧠 Selection Entropy Scalar (Trace of Interaction Core):")
print(selection_trace)
