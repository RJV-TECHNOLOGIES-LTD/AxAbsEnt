"""
AxAbsEnt | Entropy Mechanics Core

This module implements entropy-related computations grounded in the Unified Theory
of Cross-Absolute Interactions. These functions serve as the mathematical basis
for:

- Integrated information Φ({Iᵢⱼ})
- Entanglement limits between absolutes
- Absolute interaction selection principles
- Curvature-action-entropic convergence metrics

All entropy computations are conducted in base-2 (bits).
"""

from typing import Optional, Tuple
import numpy as np

# ------------------------------------------------------------------------------------
# Shannon Entropy
# ------------------------------------------------------------------------------------

def shannon_entropy(probabilities: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """
    Compute Shannon entropy H(X) = -∑ p(x) log₂ p(x)

    Parameters:
        probabilities (np.ndarray): 1D array of probability values (∑p = 1)
        epsilon (float): Threshold to avoid log(0); applied to zero masking

    Returns:
        float: Entropy in bits

    Raises:
        ValueError: If probabilities are negative or do not sum to 1
    """
    p = np.asarray(probabilities, dtype=np.float64)

    if np.any(p < 0) or not np.isclose(np.sum(p), 1.0, atol=1e-6):
        raise ValueError("Probabilities must be non-negative and sum to 1.")

    p_masked = p[p > epsilon]
    return float(-np.sum(p_masked * np.log2(p_masked)))


# ------------------------------------------------------------------------------------
# Joint Entropy
# ------------------------------------------------------------------------------------

def joint_entropy(p_xy: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """
    Compute joint entropy H(X,Y) = -∑ p(x,y) log₂ p(x,y)

    Parameters:
        p_xy (np.ndarray): 2D joint probability distribution (normalized)
        epsilon (float): Stability threshold

    Returns:
        float: Joint entropy
    """
    p = np.asarray(p_xy, dtype=np.float64)
    if not np.isclose(np.sum(p), 1.0, atol=1e-6):
        raise ValueError("Joint distribution must sum to 1.")

    p_masked = p[p > epsilon]
    return float(-np.sum(p_masked * np.log2(p_masked)))


# ------------------------------------------------------------------------------------
# Mutual Information
# ------------------------------------------------------------------------------------

def mutual_information(p_xy: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """
    Compute mutual information I(X;Y) = ∑ p(x,y) log₂(p(x,y) / p(x)p(y))

    Parameters:
        p_xy (np.ndarray): Joint probability distribution
        epsilon (float): Threshold for stability

    Returns:
        float: Mutual information in bits
    """
    p_xy = np.asarray(p_xy, dtype=np.float64)
    if not np.isclose(np.sum(p_xy), 1.0, atol=1e-6):
        raise ValueError("p(x,y) must be normalized.")

    px = np.sum(p_xy, axis=1, keepdims=True)
    py = np.sum(p_xy, axis=0, keepdims=True)
    px_py = px @ py  # Outer product

    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(
            (p_xy > epsilon) & (px_py > epsilon),
            p_xy / px_py,
            1.0  # log(1) = 0, contributes nothing
        )
        log_term = np.log2(ratio)
        result = np.sum(p_xy * log_term)

    return float(result)


# ------------------------------------------------------------------------------------
# Conditional Entropy
# ------------------------------------------------------------------------------------

def conditional_entropy(p_xy: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """
    Compute conditional entropy H(Y|X) = H(X,Y) - H(X)

    Parameters:
        p_xy (np.ndarray): Joint probability distribution
        epsilon (float): Numerical safety threshold

    Returns:
        float: Conditional entropy H(Y|X)
    """
    px = np.sum(p_xy, axis=1)
    return joint_entropy(p_xy, epsilon=epsilon) - shannon_entropy(px, epsilon=epsilon)


# ------------------------------------------------------------------------------------
# Entropy Distance (Jensen-Shannon Core)
# ------------------------------------------------------------------------------------

def entropy_distance(p1: np.ndarray, p2: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """
    Compute symmetric entropy distance:
        D_H(p1, p2) = H((p1 + p2)/2) - 0.5·H(p1) - 0.5·H(p2)

    Parameters:
        p1 (np.ndarray): First probability vector
        p2 (np.ndarray): Second probability vector
        epsilon (float): Stability threshold

    Returns:
        float: Entropy distance in bits
    """
    p1 = np.asarray(p1, dtype=np.float64)
    p2 = np.asarray(p2, dtype=np.float64)

    p1 /= np.sum(p1)
    p2 /= np.sum(p2)
    m = 0.5 * (p1 + p2)

    return shannon_entropy(m, epsilon=epsilon) - 0.5 * (
        shannon_entropy(p1, epsilon=epsilon) + shannon_entropy(p2, epsilon=epsilon)
    )


# ------------------------------------------------------------------------------------
# Normalized Entropy
# ------------------------------------------------------------------------------------

def normalized_entropy(matrix: np.ndarray, *, epsilon: float = 1e-12) -> float:
    """
    Compute normalized entropy of a matrix: H_norm = H(p) / log₂(N)

    Parameters:
        matrix (np.ndarray): Any non-negative matrix (interpreted as mass distribution)
        epsilon (float): Stability mask threshold

    Returns:
        float: Normalized entropy ∈ [0, 1]
    """
    p = np.abs(matrix.flatten())
    total = np.sum(p)
    if total == 0:
        return 0.0
    p /= total
    h = shannon_entropy(p, epsilon=epsilon)
    return float(h / np.log2(len(p)))
