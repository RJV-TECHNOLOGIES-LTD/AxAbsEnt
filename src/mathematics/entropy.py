# src/mathematics/entropy.py

import numpy as np
from typing import Union, List

def von_neumann_entropy(density_matrix: np.ndarray, tol: float = 1e-12) -> float:
    """
    Computes Von Neumann entropy: S = -Tr(ρ log ρ)
    Used when AbsoluteEntity states are expressed via quantum-like density matrices.
    """
    if not np.allclose(density_matrix, density_matrix.T.conj(), atol=tol):
        raise ValueError("Density matrix must be Hermitian.")

    eigvals = np.linalg.eigvalsh(density_matrix)
    eigvals = eigvals[eigvals > tol]  # remove near-zero eigenvalues to avoid log(0)
    entropy = -np.sum(eigvals * np.log(eigvals))
    return float(entropy)

def frobenius_entropy(tensor: np.ndarray) -> float:
    """
    Uses the Frobenius norm squared as a surrogate entropy measure for force fields.
    Suitable for symmetric projection tensors and mediator curvature fields.
    """
    return float(np.linalg.norm(tensor, ord='fro')**2)

def entropy_gradient(field: np.ndarray) -> np.ndarray:
    """
    Computes the entropy gradient over a scalar or tensor field.
    Used to derive topological force vectors (CEFT/FDT).
    """
    return np.gradient(field)

def relative_entropy(p: Union[np.ndarray, List[float]], q: Union[np.ndarray, List[float]], base: float = np.e) -> float:
    """
    Computes Kullback-Leibler divergence (relative entropy) between two probability distributions.
    Used for comparing entropic states in transfinite interaction chains.
    """
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    p = np.clip(p, 1e-12, 1.0)
    q = np.clip(q, 1e-12, 1.0)
    return float(np.sum(p * (np.log(p / q) / np.log(base))))

def entropy_flux(field_t: np.ndarray, field_prev: np.ndarray, dt: float) -> float:
    """
    Computes the temporal entropy flux (∂S/∂t) across consecutive tensor states.
    Used to determine resonance onset or force emergence from entropy acceleration.
    """
    diff = field_t - field_prev
    return float(np.linalg.norm(diff, ord='fro') / dt)

def entropy_pressure(curvature_tensor: np.ndarray, entropy_tensor: np.ndarray) -> np.ndarray:
    """
    Calculates entropic pressure induced by curvature deformation, essential to strong and gravitational fields.
    """
    return curvature_tensor @ entropy_tensor @ curvature_tensor.T
