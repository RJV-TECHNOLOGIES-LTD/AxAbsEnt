# tests/test_core/test_transfinite.py

import numpy as np
import pytest

from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.transfinite import TransfiniteInteractionChain
from axabsent.core.mediator import MediatorSpace
from axabsent.core.interaction import CrossInteractionOperator


@pytest.fixture
def three_node_chain():
    """
    Returns 3 absolute entities in linearly progressive state vectors.
    """
    a0 = AbsoluteEntity(signature=np.eye(3), state=np.array([1.0, 0.0, 0.0]))
    a1 = AbsoluteEntity(signature=np.eye(3), state=np.array([0.5, 0.5, 0.0]))
    a2 = AbsoluteEntity(signature=np.eye(3), state=np.array([0.0, 1.0, 0.0]))
    return [a0, a1, a2]


@pytest.fixture
def identity_mediator():
    return MediatorSpace(metric=np.eye(3), label="identity_mediator")


@pytest.fixture
def identity_operator():
    return CrossInteractionOperator(weight_matrix=np.eye(3))


def test_chain_initialization(three_node_chain):
    """
    TransfiniteInteractionChain must initialize with ≥2 absolutes.
    """
    chain = TransfiniteInteractionChain(absolutes=three_node_chain)
    assert isinstance(chain, TransfiniteInteractionChain)
    assert len(chain.absolutes) == 3
    assert chain.length == 2  # edges between 3 nodes


def test_chain_fails_with_single_absolute():
    """
    A transfinite chain must have at least 2 absolutes to form a valid link.
    """
    a0 = AbsoluteEntity(signature=np.eye(3), state=np.array([1.0, 0.0, 0.0]))
    with pytest.raises(ValueError, match="at least two absolutes"):
        TransfiniteInteractionChain(absolutes=[a0])


def test_causal_propagation_magnitude(three_node_chain, identity_mediator, identity_operator):
    """
    Ensure the chain computes cumulative entropy-based propagation magnitude correctly.
    """
    chain = TransfiniteInteractionChain(absolutes=three_node_chain)
    mag = chain.compute_propagation_magnitude(
        mediator=identity_mediator,
        interaction_operator=identity_operator
    )

    assert isinstance(mag, float), "Propagation magnitude must be a scalar."
    assert mag > 0, "Expected nonzero causal propagation across chain."
    assert np.isclose(mag, 1.0), f"Expected magnitude ≈ 1.0, got {mag}"


def test_projection_along_chain(three_node_chain, identity_mediator, identity_operator):
    """
    Verify that each link correctly projects entropy flow along transfinite steps.
    """
    chain = TransfiniteInteractionChain(absolutes=three_node_chain)
    flow = chain.project_entropic_flow(
        mediator=identity_mediator,
        interaction_operator=identity_operator
    )

    assert isinstance(flow, list), "Projected flow must return a list."
    assert len(flow) == chain.length
    for step in flow:
        assert isinstance(step, float)
        assert step >= 0


def test_chain_respects_null_state_handling():
    """
    A chain link must raise error if any state is undefined.
    """
    a0 = AbsoluteEntity(signature=np.eye(3), state=np.array([1.0, 0.0, 0.0]))
    a1 = AbsoluteEntity(signature=np.eye(3), state=None)
    with pytest.raises(ValueError, match="Undefined state in transfinite chain"):
        TransfiniteInteractionChain(absolutes=[a0, a1])
