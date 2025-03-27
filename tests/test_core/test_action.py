# tests/test_core/test_action.py

import numpy as np
import pytest

from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.action import CrossAbsoluteAction
from axabsent.core.mediator import MediatorSpace
from axabsent.core.interaction import CrossInteractionOperator


@pytest.fixture
def mock_absolutes():
    """
    Create a mock set of absolute entities with pre-defined signatures and states.
    """
    a1 = AbsoluteEntity(signature=np.eye(3), state=np.array([1.0, 0.0, 0.0]))
    a2 = AbsoluteEntity(signature=np.eye(3), state=np.array([0.0, 1.0, 0.0]))
    a3 = AbsoluteEntity(signature=np.eye(3), state=np.array([0.0, 0.0, 1.0]))
    return [a1, a2, a3]


@pytest.fixture
def identity_mediator():
    """
    Create an identity mediator space for pure-state propagation.
    """
    return MediatorSpace(metric=np.eye(3), label="identity_mediator")


@pytest.fixture
def default_operator():
    """
    Default linear cross-interaction operator with unit weights.
    """
    return CrossInteractionOperator(weight_matrix=np.eye(3))


def test_action_trace_conservation(mock_absolutes, identity_mediator, default_operator):
    """
    Validate that the total action trace is symmetric and conserved under reversible states.
    """
    action = CrossAbsoluteAction()
    result = action.compute_action(
        absolutes=mock_absolutes,
        mediator=identity_mediator,
        interaction_operator=default_operator
    )

    assert isinstance(result, float), "Action output should be a scalar float."
    assert result > 0, "Action should be positive definite under identity mediator."
    assert np.isclose(result, 3.0), f"Unexpected action value: {result}"


def test_action_minimization_with_projection(mock_absolutes):
    """
    Ensure that projecting states along aligned directions reduces the action scalar.
    """
    # Manually align all absolutes
    shared_state = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)
    for abs in mock_absolutes:
        abs.state = shared_state.copy()

    mediator = MediatorSpace(metric=np.eye(3))
    operator = CrossInteractionOperator(weight_matrix=np.eye(3))

    action = CrossAbsoluteAction()
    result = action.compute_action(
        absolutes=mock_absolutes,
        mediator=mediator,
        interaction_operator=operator
    )

    assert np.isclose(result, 0.0, atol=1e-6), f"Expected near-zero action for aligned states, got: {result}"


def test_action_fails_without_states(mock_absolutes, identity_mediator, default_operator):
    """
    Confirm that the action raises an error if any absolute is missing its state.
    """
    mock_absolutes[1].state = None
    action = CrossAbsoluteAction()

    with pytest.raises(ValueError, match="State undefined in one or more absolutes"):
        action.compute_action(
            absolutes=mock_absolutes,
            mediator=identity_mediator,
            interaction_operator=default_operator
        )


def test_asymmetric_mediator_increases_action(mock_absolutes):
    """
    Verify that introducing an asymmetric mediator increases total action scalar.
    """
    asymmetric_metric = np.array([
        [1.0, 0.2, 0.1],
        [0.0, 1.0, 0.3],
        [0.0, 0.0, 1.0]
    ])
    mediator = MediatorSpace(metric=asymmetric_metric)
    operator = CrossInteractionOperator(weight_matrix=np.eye(3))

    action = CrossAbsoluteAction()
    result = action.compute_action(
        absolutes=mock_absolutes,
        mediator=mediator,
        interaction_operator=operator
    )

    assert result > 3.0, f"Action should exceed symmetric baseline. Got: {result}"
