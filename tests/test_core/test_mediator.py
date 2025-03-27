# tests/test_core/test_mediator.py

import numpy as np
import pytest

from axabsent.core.mediator import MediatorSpace


def test_valid_mediator_initialization():
    """
    Mediator space must be a square, symmetric, non-singular matrix.
    """
    metric = np.array([
        [1.0, 0.2, 0.0],
        [0.2, 1.0, 0.1],
        [0.0, 0.1, 1.0]
    ])
    mediator = MediatorSpace(metric=metric, label="valid_metric")

    assert isinstance(mediator, MediatorSpace), "MediatorSpace should instantiate properly."
    assert mediator.metric.shape == (3, 3), "Expected 3x3 metric matrix."
    assert np.allclose(mediator.metric, mediator.metric.T), "Mediator metric must be symmetric."
    assert np.linalg.det(mediator.metric) > 0, "Mediator metric must be non-singular."


def test_invalid_mediator_raises_error():
    """
    Non-square or non-symmetric mediators should raise construction errors.
    """
    nonsquare = np.array([[1.0, 0.2]])
    asymmetric = np.array([
        [1.0, 0.5],
        [0.1, 1.0]
    ])

    with pytest.raises(ValueError, match="must be square"):
        MediatorSpace(metric=nonsquare)

    with pytest.raises(ValueError, match="must be symmetric"):
        MediatorSpace(metric=asymmetric)


def test_identity_projection_preserves_state():
    """
    An identity mediator must preserve any projected vector state.
    """
    metric = np.eye(3)
    mediator = MediatorSpace(metric=metric)
    state = np.array([0.5, -0.5, 1.0])
    projected = mediator.project_state(state)

    assert np.allclose(projected, state), "Identity mediator should not alter state."


def test_metric_projection_correctness():
    """
    Ensure mediator metric is applied as linear transformation during projection.
    """
    metric = np.array([
        [2.0, 0.0, 0.0],
        [0.0, 3.0, 0.0],
        [0.0, 0.0, 1.0]
    ])
    mediator = MediatorSpace(metric=metric)
    state = np.array([1.0, 1.0, 1.0])
    projected = mediator.project_state(state)

    expected = metric @ state
    assert np.allclose(projected, expected), "Projection mismatch with metric application."


def test_invalid_state_projection():
    """
    If a non-vector or mismatched dimension is projected, raise a clean error.
    """
    metric = np.eye(3)
    mediator = MediatorSpace(metric=metric)

    bad_state = np.array([[1.0, 0.0, 0.0]])  # 2D instead of 1D
    with pytest.raises(ValueError, match="must be a 1D vector"):
        mediator.project_state(bad_state)

    mismatched = np.array([1.0, 2.0])  # dimension mismatch
    with pytest.raises(ValueError, match="dimension mismatch"):
        mediator.project_state(mismatched)
