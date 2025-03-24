# examples/basic/mediator_space_creation.py

"""
Example: Creating a Mediator Space for Absolute Interaction

This script shows how to build a Mediator Space from two Absolute Entities,
compose the interaction tensor, and simulate propagation through the
mediator using basic projection techniques.

Requires:
- src.axabsent.core.absolute.AbsoluteEntity
- src.axabsent.core.mediator (future: MediatorSpace class)
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity

# ----------------------------
# Step 1: Define Absolute Entities
# ----------------------------

abs_a = AbsoluteEntity()
abs_b = AbsoluteEntity()

# Define internal waveform signatures
abs_a.set_property("waveform", np.array([0.9, 0.3]))
abs_b.set_property("waveform", np.array([0.4, 0.6]))

abs_a.signature = np.diag(abs_a.get_property("waveform"))
abs_b.signature = np.diag(abs_b.get_property("waveform"))

print("✅ Absolutes Created:")
print("Signature A:\n", abs_a.signature)
print("Signature B:\n", abs_b.signature)

# ----------------------------
# Step 2: Create Mediator Tensor
# ----------------------------

def create_mediator_tensor(sig_a: np.ndarray, sig_b: np.ndarray) -> np.ndarray:
    """
    Composes the mediator tensor as a symmetric bridge between two signatures.
    Represents the transient interaction frame across mediation space.
    """
    return sig_a @ sig_b + sig_b @ sig_a

mediator_tensor = create_mediator_tensor(abs_a.signature, abs_b.signature)

print("\n🧭 Mediator Tensor Constructed:")
print(mediator_tensor)

# ----------------------------
# Step 3: Apply Projection in Mediator
# ----------------------------

def apply_mediator_projection(entity: AbsoluteEntity, mediator: np.ndarray) -> np.ndarray:
    """
    Applies the mediator tensor as a projection operator to the absolute's internal state.
    Simulates propagation of information through mediation.
    """
    if entity.state is None:
        entity.state = np.array([[0.5], [0.5]])  # default state if undefined
    return mediator @ entity.state

projected_state = apply_mediator_projection(abs_a, mediator_tensor)

print("\n📡 Projected State via Mediator:")
print(projected_state)

# ----------------------------
# Step 4: Compute Information Transfer Scalar
# ----------------------------

entropy_core = mediator_tensor @ mediator_tensor.T
information_scalar = np.trace(entropy_core)

print("\n🧠 Information Scalar (Trace of Mediator Core):")
print(information_scalar)
