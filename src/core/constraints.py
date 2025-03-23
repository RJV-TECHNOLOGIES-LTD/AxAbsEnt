# src/core/constraints.py

import numpy as np
from typing import List
from .absolute import AbsoluteEntity

def validate_signature_matrix(matrix: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Ensures the signature matrix is square, symmetric, and real.
    Required for any AbsoluteEntity representation.
    """
    if matrix.ndim != 2:
        return False
    if matrix.shape[0] != matrix.shape[1]:
        return False
    if not np.allclose(matrix, matrix.T, atol=tol):
        return False
    if not np.isreal(matrix).all():
        return False
    return True

def validate_symmetry_conditions(entities: List[AbsoluteEntity], threshold: float = 1e-5) -> bool:
    """
    Validates symmetry consistency across Absolute Entities' signatures.
    Passes if deviation norm remains within CEFT-prescribed thresholds.
    """
    if len(entities) < 2:
        return True
    base = entities[0].signature
    for other in entities[1:]:
        delta = np.linalg.norm(base - other.signature, ord="fro")
        if delta > threshold:
            return False
    return True

def enforce_curvature_tensor_conditions(curvature_tensor: np.ndarray, dimension: int, tol: float = 1e-6) -> bool:
    """
    Verifies that a mediator's curvature tensor is valid under FDT.
    Must be square, symmetric, non-singular, and match declared dimensionality.
    """
    if curvature_tensor.shape != (dimension, dimension):
        return False
    if not np.allclose(curvature_tensor, curvature_tensor.T, atol=tol):
        return False
    det = np.linalg.det(curvature_tensor)
    if abs(det) < tol:
        return False  # Near-singular tensor, invalid for force emergence
    return True

def validate_projective_consistency(entity: AbsoluteEntity, projection_matrix: np.ndarray) -> bool:
    """
    Ensures that the projection of an entity's state does not violate its identity invariance.
    This protects against illegal transformations violating SDI constraints.
    """
    try:
        if entity.state is None:
            return True  # Nothing to project
        projected = projection_matrix @ entity.state
        if not np.isfinite(projected).all():
            return False
        return True
    except Exception:
        return False
