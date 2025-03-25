# tests/test_experimental/__init__.py

"""
Initialization for experimental prediction test suite.

This suite verifies the prediction engine's ability to:
- Detect vacuum fluctuation signatures
- Match theoretical projections to particle physics observations
- Validate cosmological parameters under the unified model
- Evaluate resonance maps and entropy flux measurements

Each test directly evaluates falsifiable outputs as defined by:
▶ Enhanced Mathematical Ontology of Absolute Nothingness
▶ AxAbsEnt Experimental Signature Framework (AESF)
"""

import os
import sys
import numpy as np

# Ensure access to main AxAbsEnt modules
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Seed random number generator for reproducibility of Monte Carlo and synthetic resonance validation
np.random.seed(777)

# Signal test context initialization
print("[AxAbsEnt] Experimental prediction test suite initialized.")
