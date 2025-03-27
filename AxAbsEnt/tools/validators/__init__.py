# tools/validators/__init__.py

"""
AxAbsEnt Validators Package

This module provides centralized access to validation tools for:
- Theoretical consistency enforcement
- Mathematical structure coherence
- Simulation configuration validation
- Experimental prediction alignment
- Tensor shape enforcement and unit validation

Each validator is aligned with the Enhanced Mathematical Ontology of Absolute Nothingness.
"""

from .theory_consistency import validate_cross_absolute_theory
from .simulation_validator import validate_simulation_config
from .experimental_prediction import validate_prediction_consistency
from .mathematical_consistency import (
    validate_tensor_shape,
    validate_signature_matrix,
    validate_entropy_projection
)

__all__ = [
    "validate_cross_absolute_theory",
    "validate_simulation_config",
    "validate_prediction_consistency",
    "validate_tensor_shape",
    "validate_signature_matrix",
    "validate_entropy_projection"
]
