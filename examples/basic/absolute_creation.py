# examples/basic/absolute_creation.py

"""
Example: Creating and Inspecting Absolute Entities

This script demonstrates how to instantiate AbsoluteEntity objects,
assign internal properties, and compute selection-related metrics
in accordance with the AxAbsEnt Unified Theory.

Requires:
- src.axabsent.core.absolute.AbsoluteEntity
"""

import numpy as np
from axabsent.core.absolute import AbsoluteEntity

# ----------------------------
# Step 1: Create a basic absolute entity
# ----------------------------

abs1 = AbsoluteEntity()

print("✅ Absolute Created")
print(f"ID: {abs1.identifier}")
print(f"Signature Matrix:\n{abs1.signature}")
print(f"Initial Properties: {abs1.properties}")

# ----------------------------
# Step 2: Assign internal properties
# ----------------------------

abs1.set_property("charge", 1.0)
abs1.set_property("mass", 9.11e-31)  # in kg
abs1.set_property("dimension", 3)
abs1.set_property("waveform", np.array([0.7, 0.2, 0.1]))

print("\n🔧 Properties Assigned:")
for k, v in abs1.properties.items():
    print(f"{k}: {v}")

# ----------------------------
# Step 3: Assign a state vector for projection
# ----------------------------

state_vector = np.array([[0.5]])
abs1.state = state_vector

# Define projection matrix (identity for trivial test)
projection_matrix = np.eye(1)

projected = abs1.project_state(projection_matrix)

print("\n🌀 State Projection:")
print(f"Original State: {abs1.state}")
print(f"Projected State: {projected}")

# ----------------------------
# Step 4: Compute Selection Entropy Scalar
# ----------------------------

entropy_scalar = abs1.encode_selection()

print("\n🧠 Selection Principle Scalar:")
print(f"Entropy Core Trace: {entropy_scalar}")
