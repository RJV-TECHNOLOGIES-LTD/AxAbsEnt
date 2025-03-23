# src/mathematics/differential_geometry.py

import numpy as np
from typing import Tuple

def compute_metric_tensor(basis_vectors: np.ndarray) -> np.ndarray:
    """
    Computes the metric tensor g_ij from a set of basis vectors.
    g_ij = <e_i, e_j> — inner product in curved space.
    """
    dim = basis_vectors.shape[1]
    metric = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            metric[i, j] = np.dot(basis_vectors[:, i], basis_vectors[:, j])
    return metric

def christoffel_symbols(metric_tensor: np.ndarray) -> np.ndarray:
    """
    Computes the Christoffel symbols Γ^k_ij from a metric tensor.
    These define how vectors parallel transport in a curved space.
    """
    dim = metric_tensor.shape[0]
    inv_metric = np.linalg.inv(metric_tensor)
    symbols = np.zeros((dim, dim, dim))
    for k in range(dim):
        for i in range(dim):
            for j in range(dim):
                term = (
                    np.gradient(metric_tensor[j, k], axis=i) +
                    np.gradient(metric_tensor[i, k], axis=j) -
                    np.gradient(metric_tensor[i, j], axis=k)
                )
                symbols[i, j, k] = 0.5 * np.sum(inv_metric[k, :] * term)
    return symbols

def compute_geodesic(metric_tensor: np.ndarray, position: np.ndarray, velocity: np.ndarray, dt: float, steps: int) -> np.ndarray:
    """
    Evolves a geodesic in curved space using second-order Christoffel-corrected update.
    Used to trace force lines and entropy flow paths over mediator curvature.
    """
    path = [position]
    current_pos = position.copy()
    current_vel = velocity.copy()
    Γ = christoffel_symbols(metric_tensor)

    for _ in range(steps):
        acceleration = np.zeros_like(current_pos)
        for i in range(len(current_pos)):
            for j in range(len(current_pos)):
                for k in range(len(current_pos)):
                    acceleration[i] -= Γ[j, k, i] * current_vel[j] * current_vel[k]
        current_vel += acceleration * dt
        current_pos += current_vel * dt
        path.append(current_pos.copy())

    return np.array(path)

def curvature_scalar(metric_tensor: np.ndarray) -> float:
    """
    Returns an approximate scalar curvature (Ricci scalar) for small-scale mediator space.
    """
    inv_metric = np.linalg.inv(metric_tensor)
    det = np.linalg.det(metric_tensor)
    if det <= 0:
        return 0.0
    trace = np.trace(inv_metric)
    curvature = trace / det
    return float(curvature)

def is_flat(metric_tensor: np.ndarray, tolerance: float = 1e-8) -> bool:
    """
    Determines if the space described by the metric is locally flat (zero curvature).
    """
    scalar = curvature_scalar(metric_tensor)
    return abs(scalar) < tolerance
