# tests/test_forces/__init__.py

"""
Initialization for the force emergence test suite.

This suite covers:
- Force field extraction from cross-absolute entropy gradients
- Decomposition of unified force chains into standard model counterparts
- Evaluation of force signatures and coupling constants
- Falsifiability of force emergence through entropy-field alignment

These tests are rooted in the principles of:
▶ Force Geometry as Entropic Gradient
▶ Cross-Absolute Resonance Induction
▶ Unified Signature Differentiation Framework (USDF)
"""

import os
import sys
import numpy as np

# Set up source path for test context
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Force reproducibility of gradient and field tests
np.random.seed(31415)

# Console log for test runners
print("[AxAbsEnt] Force emergence test suite initialized.")
