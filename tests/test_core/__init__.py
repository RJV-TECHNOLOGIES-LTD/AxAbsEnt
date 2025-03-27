# tests/test_core/__init__.py

"""
Initialization file for core module tests in AxAbsEnt.

This suite validates the foundational ontology components:
- Absolute entity construction and invariants
- Cross-absolute interaction operators
- Mediator space composition
- Transfinite interaction chains
- Information transfer mechanisms
- Cross-absolute action formulation

All core logic must comply with the Enhanced Mathematical Ontology of Absolute Nothingness.
"""

import os
import sys
import numpy as np

# Ensure src is importable
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Optional: Set global test seed for reproducibility
np.random.seed(42)

# Log test suite startup
print("[AxAbsEnt] Core module test suite initialized.")
