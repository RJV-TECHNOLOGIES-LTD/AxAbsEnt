"""
AxAbsEnt Mathematics Test Suite Initialization

This module sets up the testing environment for all mathematical subcomponents
of the AxAbsEnt system, including:
- Tensor algebra
- Entropy and information theory
- Category theory and functors
- Differential geometry
- Transfinite and ordinal logic
- Topological and Lie algebraic constructs

These tests ensure mathematical consistency and theoretical traceability.
"""

import pytest
import numpy as np
import random
import os

# Set global numerical tolerance
NUMERICAL_PRECISION = 1e-10

# Ensure deterministic testing
def pytest_configure(config):
    np.random.seed(42)
    random.seed(42)
    os.environ["PYTHONHASHSEED"] = "42"

    config.addinivalue_line(
        "markers", "math: mark test as part of the AxAbsEnt mathematical engine suite"
    )
