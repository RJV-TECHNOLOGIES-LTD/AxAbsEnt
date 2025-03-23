# src/mathematics/tensors.py

import numpy as np
from typing import Tuple

def contract_tensor(tensor: np.ndarray, axis_pairs: Tuple[int, int]) -> float:
    """
    Contracts a tensor over a pair of axes.
    Reduces multi-rank field tensors into scalars (e.g., for action, stress).
    """
    return float(np.trace(np.tensordot(tensor, tensor, axes=(axis_pairs))))

def project_tensor(tensor: np.ndarray, projector: np.ndarray) -> np.ndarray:
    """
    Projects a tensor onto a specified subspace using a projector matrix.
    Essential for mediator-space compatible interaction projections.
    """
    return projector @ tensor @ projector.T

def decompose_tensor(tensor: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Decomposes a tensor into symmetric and antisymmetric components.
    Used to separate field resonance from topological twist.
    """
    symmetric = 0.5 * (tensor + tensor.T)
    antisymmetric = 0.5 * (tensor - tensor.T)
    return symmetric, antisymmetric

def transform_basis(tensor: np.ndarray, basis_matrix: np.ndarray) -> np.ndarray:
    """
    Changes the basis of a tensor using a given orthonormal transformation matrix.
    Required for interpreting interaction tensors in alternate mediator spaces.
    """
    return basis_matrix.T @ tensor @ basis_matrix

def tensor_norm(tensor: np.ndarray, norm: str = "fro") -> float:
    """
    Computes norm of a tensor for entropy quantification or gradient pressure.
    """
    return float(np.linalg.norm(tensor, ord=norm))

def rank_check(tensor: np.ndarray, expected_rank: int) -> bool:
    """
    Validates whether a tensor has the expected rank (number of dimensions).
    """
    return tensor.ndim == expected_rank

def is_positive_definite(tensor: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Checks if a tensor is positive definite (e.g., for valid curvature tensors).
    """
    try:
        np.linalg.cholesky(tensor + tol * np.eye(tensor.shape[0]))
        return True
    except np.linalg.LinAlgError:
        return False
