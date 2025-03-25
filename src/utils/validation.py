"""
Validation Utilities for AxAbsEnt

Purpose:
- Validate the structural, numerical, ontological, and epistemological consistency of:
    • AbsoluteEntity definitions
    • Interaction operators (Iij)
    • Tensor fields (force projections, entanglement matrices, entropy maps)
    • Visualization outputs (graphical renderings from mathematical constructs)

All validation functions are designed to enforce alignment with the Unified Theory
and prevent epistemologically invalid constructs from entering the computation pipeline.
"""

from typing import Any, Union
import numpy as np
from matplotlib.figure import Figure
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator


def validate_absolute_structure(entity: AbsoluteEntity) -> bool:
    """
    Validates that an absolute entity contains valid structure and property spaces.

    Args:
        entity (AbsoluteEntity): The entity to validate

    Returns:
        bool: True if valid, raises ValueError otherwise
    """
    if not entity.name or not isinstance(entity.name, str):
        raise ValueError("AbsoluteEntity must have a valid name string.")
    if not entity.structure_space or not isinstance(entity.structure_space, str):
        raise ValueError(f"{entity.name} lacks valid structure_space.")
    if not entity.property_space or not isinstance(entity.property_space, str):
        raise ValueError(f"{entity.name} lacks valid property_space.")
    return True


def validate_interaction_operator(operator: InteractionOperator) -> bool:
    """
    Validates that an interaction operator is well-formed and ontologically coherent.

    Args:
        operator (InteractionOperator): The Iij to validate

    Returns:
        bool: True if valid, raises ValueError otherwise
    """
    if not operator.absolute_i or not operator.absolute_j:
        raise ValueError("InteractionOperator must bind two absolutes.")
    if operator.absolute_i == operator.absolute_j:
        if not operator.symmetric:
            raise ValueError("Self-interaction must be symmetric or explicitly defined.")
    if not hasattr(operator, "interaction_tensor") or operator.interaction_tensor is None:
        raise ValueError("InteractionOperator must contain a valid tensor.")
    if not isinstance(operator.interaction_tensor, np.ndarray):
        raise TypeError("Interaction tensor must be a NumPy array.")
    return True


def validate_tensor_entropy_consistency(tensor: np.ndarray) -> bool:
    """
    Ensure entropy-relevant tensors are numerically valid (non-negative, bounded).

    Args:
        tensor (np.ndarray): The tensor to validate

    Returns:
        bool: True if valid, raises ValueError otherwise
    """
    if not isinstance(tensor, np.ndarray):
        raise TypeError("Expected tensor input as NumPy ndarray.")
    if np.any(np.isnan(tensor)) or np.any(np.isinf(tensor)):
        raise ValueError("Tensor contains NaN or infinite values.")
    if np.min(tensor) < 0:
        raise ValueError("Entropy tensors must be non-negative.")
    return True


def validate_visualization_output(fig: Any) -> bool:
    """
    Validates that a matplotlib figure meets basic visual integrity criteria.

    Args:
        fig (Any): Figure object (usually matplotlib.figure.Figure)

    Returns:
        bool: True if valid, raises ValueError otherwise
    """
    if not isinstance(fig, Figure):
        raise TypeError("Expected matplotlib Figure.")
    if not fig.axes:
        raise ValueError("Visualization figure contains no axes.")
    return True


def validate_force_signature_vector(vector: np.ndarray, tolerance: float = 1e-6) -> bool:
    """
    Ensures a force signature vector (σ⃗ᵢ) is normalized and non-negative.

    Args:
        vector (np.ndarray): Force contribution vector for an absolute
        tolerance (float): Allowed deviation from unit norm

    Returns:
        bool: True if valid
    """
    if not isinstance(vector, np.ndarray):
        raise TypeError("Force signature must be a NumPy vector.")
    if np.any(vector < 0):
        raise ValueError("Force signature components must be non-negative.")
    norm = np.sum(vector)
    if not np.isclose(norm, 1.0, atol=tolerance):
        raise ValueError(f"Force signature must sum to 1. Got {norm}")
    return True
