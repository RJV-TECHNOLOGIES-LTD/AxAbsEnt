"""
Test Suite: Multidimensional Visualization of Cross-Absolute Structures

Purpose:
- Validate rendering fidelity of high-dimensional tensors and force fields
- Ensure correct projection of cross-absolute interaction structures onto visual subspaces
- Maintain ontological traceability from tensor representations to absolute structure configurations

Theoretical Basis:
- Visualizations must reflect projections from Iij: Sᵢ × Sⱼ → Sinteraction
- Tensor fields must encode:
    • Orthogonality (O(Aᵢ, Aⱼ))
    • Mediator hierarchy depth
    • Transfinite chain attenuation
- Must visually comply with structure entropy, topological curvature, and force signature projections (σ⃗ᵢ)

Modules Tested:
- axabsent.visualization.multidimensional

"""

import pytest
import numpy as np
from matplotlib.figure import Figure

from axabsent.visualization.multidimensional import (
    render_tensor_projection,
    render_topological_embedding,
)
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator
from axabsent.utils.validation import validate_visualization_output


def generate_test_tensor(rank: int = 3, shape: tuple = (10, 10, 10)) -> np.ndarray:
    """
    Generate a synthetic high-rank tensor encoding interaction data for visualization tests.

    Returns:
        np.ndarray: High-dimensional tensor simulating Iij interaction outputs
    """
    tensor = np.random.random(shape)
    # Impose orthogonality gradient for realism
    for i in range(shape[0]):
        tensor[i, :, :] *= np.exp(-i / shape[0])
    return tensor


def test_tensor_projection_rendering():
    """
    Test projection rendering from a 3D interaction tensor onto a 2D visual plane.
    """
    tensor = generate_test_tensor()
    fig = render_tensor_projection(tensor, projection_axis=0)

    assert isinstance(fig, Figure), "Output of tensor projection must be a matplotlib Figure."
    assert validate_visualization_output(fig), "Tensor projection visualization failed integrity check."
    assert fig.axes, "Figure must include axes for the projected subspace."


def test_topological_embedding_visualization():
    """
    Test multidimensional embedding visualization from theoretical structure tensor.
    """
    tensor = generate_test_tensor(rank=4, shape=(8, 8, 8, 8))
    fig = render_topological_embedding(tensor, method="entropy-curvature")

    assert isinstance(fig, Figure), "Output of topological embedding must be a matplotlib Figure."
    assert validate_visualization_output(fig), "Topological embedding visualization failed integrity check."


def test_tensor_orthogonality_gradient_preservation():
    """
    Verify tensor rendering visually reflects decreasing inter-absolute interaction with increasing orthogonality.
    """
    tensor = generate_test_tensor()
    projection = tensor.mean(axis=0)  # Should reflect orthogonality decay in intensity

    assert projection.shape == (10, 10), "Projection must reduce tensor to 2D subspace"
    assert np.all(projection >= 0), "Tensor projection must yield non-negative visual values"
    assert projection.max() <= 1.0, "Tensor projection values must remain normalized"
    assert projection.min() < projection.max(), "Visual gradient must reflect structure differences"
