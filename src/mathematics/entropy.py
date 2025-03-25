"""
AxAbsEnt | Entropy Mechanics Module

This module provides foundational entropy and information theory functions
used throughout the cross-absolute interaction framework. It supports:
- Shannon entropy and extensions
- Mutual information
- Conditional entropy
- Entropy distance metrics
- Normalized entropy for structure comparison

All computations assume base-2 logarithm (bits).
"""

import numpy as np


def shannon_entropy(probabilities: np.ndarray) -> float:
    """
    Compute the Shannon entropy of a probability distribution.

    Parameters:
        probabilities (np.ndarray): Probability vector (must sum to 1)

    Returns:
        float: Entropy H(p) in bits

    Raises:
        ValueError: if negative or unnormalized probabilities are detected
    """
    p = np.asarray(probabilities, dtype=np.float64)
    if np.any(p < 0) or not np.isclose(np.sum(p), 1.0):
        raise ValueError("Probabilities must be non-negative and sum to 1.")
    p = p[p > 0]  # Avoid log(0)
    return -np.sum(p * np.log2(p))


def joint_entropy(p_xy: np.ndarray) -> float:
    """
    Compute the joint entropy H(X, Y) for a joint distribution.

    Parameters:
        p_xy (np.ndarray): Joint probability matrix

    Returns:
        float: Joint entropy H(X, Y)
    """
    p = p_xy.astype(np.float64)
    p = p[p > 0]
    return -np.sum(p * np.log2(p))


def mutual_information(p_xy: np.ndarray) -> float:
    """
    Compute the mutual information I(X; Y) from a joint distribution.

    Parameters:
        p_xy (np.ndarray): Joint probability matrix

    Returns:
        float: Mutual information I(X; Y)
    """
    p_xy = p_xy.astype(np.float64)
    px = np.sum(p_xy, axis=1, keepdims=True)
    py = np.sum(p_xy, axis=0, keepdims=True)
    p_product = px @ py

    # Avoid division by zero
    mask = (p_xy > 0) & (p_product > 0)
    return np.sum(p_xy[mask] * np.log2(p_xy[mask] / p_product[mask]))


def conditional_entropy(p_xy: np.ndarray) -> float:
    """
    Compute conditional entropy H(Y|X) from joint distribution.

    Parameters:
        p_xy (np.ndarray): Joint probability matrix

    Returns:
        float: Conditional entropy H(Y|X)
    """
    H_joint = joint_entropy(p_xy)
    px = np.sum(p_xy, axis=1)
    H_x = shannon_entropy(px)
    return H_joint - H_x


def entropy_distance(p1: np.ndarray, p2: np.ndarray) -> float:
    """
    Compute symmetric entropy-based distance between two distributions.

    D_H(p1, p2) = H((p1 + p2)/2) - 0.5 * H(p1) - 0.5 * H(p2)

    Parameters:
        p1, p2 (np.ndarray): Discrete probability distributions

    Returns:
        float: Entropy distance
    """
    p1 = p1 / np.sum(p1)
    p2 = p2 / np.sum(p2)
    m = 0.5 * (p1 + p2)
    return shannon_entropy(m) - 0.5 * (shannon_entropy(p1) + shannon_entropy(p2))


def normalized_entropy(matrix: np.ndarray) -> float:
    """
    Compute the normalized entropy of a matrix as a measure of disorder.

    Parameters:
        matrix (np.ndarray): A matrix (will be normalized to sum to 1)

    Returns:
        float: Normalized entropy in [0, 1]
    """
    p = np.abs(matrix.flatten())
    p /= np.sum(p)
    return shannon_entropy(p) / np.log2(len(p))
