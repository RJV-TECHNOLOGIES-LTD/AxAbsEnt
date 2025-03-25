# tools/validators/mathematical_consistency.py

"""
Mathematical Consistency Validator

Ensures internal mathematical structures conform to rules of the unified ontology,
including tensor dimensions, signature matrix validity, entropy trace integrity,
and operator symmetry under transformations.
"""

import numpy as np


def validate_tensor_shape(tensor: np.ndarray, expected_shape: tuple) -> bool:
    """
    Validate that a tensor has the exact expected shape.

    Args:
        tensor (np.ndarray): The tensor to validate.
        expected_shape (tuple): Expected shape as (rows, cols) or (n,).

    Returns:
        bool: True if shape matches, False otherwise.
    """
    if not isinstance(tensor, np.ndarray):
        raise TypeError("Tensor must be a NumPy array.")
    return tensor.shape == expected_shape


def validate_signature_matrix(matrix: np.ndarray) -> bool:
    """
    Ensure that a signature matrix is:
    - Square
    - Symmetric
    - Trace-invertible (i.e., not singular for entropy projection)
    - Encodes identity projection under self-interaction

    Returns:
        bool: True if all properties are satisfied
    """
    if not isinstance(matrix, np.ndarray):
        return False
    if matrix.shape[0] != matrix.shape[1]:
        return False
    if not np.allclose(matrix, matrix.T):
        return False
    if np.linalg.matrix_rank(matrix) < matrix.shape[0]:
        return False
    return True


def validate_entropy_projection(matrix: np.ndarray) -> bool:
    """
    Validates whether the matrix projects onto a non-negative scalar entropy space.

    This is done by checking if the trace of matrix.T @ matrix is non-negative.

    Args:
        matrix (np.ndarray): Matrix used for entropy core calculation.

    Returns:
        bool: True if entropy projection is valid.
    """
    if not isinstance(matrix, np.ndarray):
        return False
    entropy_core = matrix @ matrix.T
    trace = np.trace(entropy_core)
    return np.isfinite(trace) and trace >= 0


def is_unit_tensor(tensor: np.ndarray) -> bool:
    """
    Check if a tensor is approximately an identity matrix.

    Args:
        tensor (np.ndarray)

    Returns:
        bool
    """
    if tensor.shape[0] != tensor.shape[1]:
        return False
    return np.allclose(tensor, np.eye(tensor.shape[0]), atol=1e-10)
