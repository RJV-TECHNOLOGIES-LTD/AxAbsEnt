import pytest
import numpy as np
from axabsent.mathematics.differential_geometry import (
    Manifold,
    MetricTensor,
    compute_connection,
    compute_riemann_tensor,
    compute_ricci_tensor,
    compute_scalar_curvature
)


@pytest.mark.math
def test_metric_tensor_definition():
    """
    Ensure the metric tensor is symmetric and has proper dimensionality.
    """
    m = Manifold(name="2D Minkowski", dim=2)
    g = MetricTensor(m, components=np.array([[1.0, 0.0], [0.0, -1.0]]))

    assert g.shape == (2, 2)
    assert np.allclose(g.components, g.components.T)  # Symmetric
    assert g.signature == (1, -1)


@pytest.mark.math
def test_connection_computation():
    """
    Check if Christoffel symbols are correctly computed from the metric.
    """
    m = Manifold("2D Euclidean", dim=2)
    g = MetricTensor(m, components=np.eye(2))

    Γ = compute_connection(g)
    assert isinstance(Γ, np.ndarray)
    assert Γ.shape == (2, 2, 2)
    assert np.allclose(Γ, np.zeros((2, 2, 2)))  # Flat space


@pytest.mark.math
def test_riemann_tensor_for_flat_space():
    """
    Riemann tensor should vanish in flat Euclidean space.
    """
    m = Manifold("2D Euclidean", dim=2)
    g = MetricTensor(m, components=np.eye(2))

    Riemann = compute_riemann_tensor(g)
    assert Riemann.shape == (2, 2, 2, 2)
    assert np.allclose(Riemann, 0)


@pytest.mark.math
def test_ricci_tensor_and_scalar_curvature():
    """
    Validate Ricci tensor and scalar curvature for a known curved manifold.
    """
    # Sphere with radius R = 1, known Ricci tensor: R_ij = g_ij, scalar curvature = 2
    m = Manifold("2-Sphere", dim=2)
    g = MetricTensor(m, components=np.array([[1.0, 0.0], [0.0, np.sin(np.pi / 4)**2]]))

    riemann = compute_riemann_tensor(g)
    ricci = compute_ricci_tensor(riemann)
    scalar = compute_scalar_curvature(ricci, g)

    assert ricci.shape == (2, 2)
    assert isinstance(scalar, float)
    assert scalar > 0  # Positive curvature for sphere


@pytest.mark.math
def test_metric_signature_classification():
    """
    Check automatic classification of signature for Lorentzian metric.
    """
    m = Manifold("2D Lorentzian", dim=2)
    g = MetricTensor(m, components=np.array([[-1.0, 0.0], [0.0, 1.0]]))

    assert g.signature == (-1, 1)
    assert g.is_lorentzian()
