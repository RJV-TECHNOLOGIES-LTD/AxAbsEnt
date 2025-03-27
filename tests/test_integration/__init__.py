# tests/test_integration/__init__.py

"""
AxAbsEnt Integration Test Suite Initialization

This module initializes the integration testing environment for validating the complete
execution flow across core ontological structures, mediator spaces, force emergence,
entropy propagation, and simulation-rendering feedback loops.

Integration tests simulate full-scale scientific scenarios combining:
  - Absolute Entity instantiation
  - Interaction tensor application via mediator composition
  - Force emergence through CEFT, SDI, FDT
  - Simulation of transfinite chains and resonance propagation
  - Visualization and entropy signature verification
"""

import logging
import warnings
import numpy as np

# Suppress irrelevant numerical warnings in controlled tensor algebra operations
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Configure test-level logging
logging.basicConfig(
    level=logging.INFO,
    format="🔥 [AxAbsEnt Integration] %(asctime)s — %(levelname)s — %(message)s"
)

# Global precision for numerical tests
np.set_printoptions(precision=6, suppress=True)

# Log suite boot
logging.info("AxAbsEnt Integration Test Suite initialized.")
