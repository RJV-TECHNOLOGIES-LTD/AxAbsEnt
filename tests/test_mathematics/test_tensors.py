"""
Test Suite: Tensor Algebra and Absolute Interaction Structures

Purpose:
- Validate the correctness of tensor construction, manipulation, and projection
  within the AxAbsEnt mathematical layer.
- Ensure theoretical consistency with:
    • Cross-absolute interaction tensors (I_ij)
    • Force projection matrices (σ⃗i, EF_k)
    • Orthogonality-decomposed tensor fields
    • Transfinite tensor contraction and decay chains

Modules Tested:
- axabsent.mathematics.tensors

Theoretical Foundations:
- Tensor constructions must encode interactions over Si × Sj → Sinteraction
- Contractions must obey chain-damped norms and preserve entropy
- Tensor projections must reflect accurate force decompositions
"""

import pytest
import numpy as np

from axabsent.mathematics.tensors import (
    create_interaction_tensor,
    contract_tensor_along_axis,
    project_tensor_to_force_signature,
    normalize_tensor,
    damp_tensor_transfinite_chain,
)


def test_create_interaction_tensor_shape_and_type():
    """
    Validates shape and numerical properties of an Iij tensor from two absolutes.
    """
    tensor = create_interaction_tensor(dim_i=4, dim_j=5)

    assert isinstance(tensor, np.ndarray), "Interaction tensor must be a NumPy ndarray."
    assert tensor.shape == (4, 5), "Tensor shape must match (dim_i, dim_j)."
    assert np.issubdtype(tensor.dtype, np.floating), "Tensor values must be float type."


def test_tensor_contraction_preserves_rank():
    """
    Ensure contraction along specified axis reduces tensor rank correctly.
    """
    tensor = np.random.rand(3, 4, 5)
    contracted = contract_tensor_along_axis(tensor, axis=1)

    assert contracted.shape == (3, 5), "Tensor rank after contraction should reduce by one."


def test_tensor_projection_to_force_signature():
    """
    Test force signature projection from interaction tensor.
    """
    interaction_tensor = np.random.rand(6, 6)
    signature_vector = np.array([0.9, 0.1, 0.0, 0.0, 0.0, 0.0])  # Dominant force signature from A1

    projected = project_tensor_to_force_signature(interaction_tensor, signature_vector)

    assert projected.shape == interaction_tensor.shape, "Projected tensor must retain original shape."
    assert np.all(projected <= 1.0), "Projection must remain normalized."


def test_tensor_normalization_output_bounds():
    """
    Normalization must produce values in [0,1] for visualization or entropy encoding.
    """
    tensor = np.random.normal(0, 3, size=(10, 10))
    normalized = normalize_tensor(tensor)

    assert normalized.shape == (10, 10), "Normalization must preserve shape."
    assert np.all((normalized >= 0) & (normalized <= 1)), "Normalized values must be in [0,1]."


def test_transfinite_chain_tensor_damping():
    """
    Simulate damping of multi-hop transfinite tensor composition.
    """
    base_tensor = np.ones((3, 3))
    chain_order = 4
    damping_lambda = 0.5

    damped = damp_tensor_transfinite_chain(base_tensor, chain_order=chain_order, damping_factor=damping_lambda)

    expected_decay = np.exp(-damping_lambda * chain_order)
    assert np.allclose(damped, base_tensor * expected_decay, rtol=1e-6), "Damped tensor must decay exponentially."
