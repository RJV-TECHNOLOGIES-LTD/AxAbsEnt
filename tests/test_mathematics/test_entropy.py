import pytest
import numpy as np
from axabsent.mathematics.entropy import (
    shannon_entropy,
    joint_entropy,
    mutual_information,
    conditional_entropy,
    normalized_entropy,
    entropy_distance
)


@pytest.mark.math
def test_shannon_entropy_of_uniform_distribution():
    """
    Shannon entropy of uniform distribution with n states should be log2(n).
    """
    probs = np.array([0.25, 0.25, 0.25, 0.25])
    H = shannon_entropy(probs)
    assert pytest.approx(H, rel=1e-6) == 2.0


@pytest.mark.math
def test_joint_entropy_for_independent_variables():
    """
    H(X, Y) = H(X) + H(Y) when X and Y are independent.
    """
    px = np.array([0.5, 0.5])
    py = np.array([0.5, 0.5])
    pxy = np.outer(px, py)  # Joint distribution for independence

    H_joint = joint_entropy(pxy)
    assert pytest.approx(H_joint, rel=1e-6) == 2.0


@pytest.mark.math
def test_mutual_information_for_independent_variables():
    """
    Mutual information should be 0 if variables are independent.
    """
    px = np.array([0.5, 0.5])
    py = np.array([0.5, 0.5])
    pxy = np.outer(px, py)

    I = mutual_information(pxy)
    assert pytest.approx(I, abs=1e-8) == 0.0


@pytest.mark.math
def test_conditional_entropy_consistency():
    """
    H(Y|X) = H(X,Y) - H(X)
    """
    pxy = np.array([[0.25, 0.25], [0.25, 0.25]])  # Uniform joint
    H_joint = joint_entropy(pxy)
    px = pxy.sum(axis=1)
    H_x = shannon_entropy(px)
    H_y_given_x = conditional_entropy(pxy)

    assert pytest.approx(H_y_given_x, rel=1e-6) == H_joint - H_x


@pytest.mark.math
def test_entropy_distance_between_distributions():
    """
    Entropy distance should be 0 between identical distributions.
    """
    p1 = np.array([0.4, 0.6])
    p2 = np.array([0.4, 0.6])
    dist = entropy_distance(p1, p2)
    assert pytest.approx(dist, abs=1e-10) == 0.0


@pytest.mark.math
def test_normalized_entropy_between_zero_and_one():
    """
    Normalized entropy must lie between 0 and 1.
    """
    matrix = np.random.rand(4, 4)
    matrix /= matrix.sum()
    h = normalized_entropy(matrix)
    assert 0.0 <= h <= 1.0
