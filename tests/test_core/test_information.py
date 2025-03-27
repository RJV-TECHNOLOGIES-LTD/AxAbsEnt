# tests/test_core/test_information.py

import numpy as np
import pytest

from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.information import InformationTransfer
from axabsent.core.mediator import MediatorSpace
from axabsent.core.interaction import CrossInteractionOperator


@pytest.fixture
def aligned_absolutes():
    """
    Two aligned absolutes in the same state direction.
    Ideal for information flow equilibrium tests.
    """
    state = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)
    a1 = AbsoluteEntity(signature=np.eye(3), state=state.copy())
    a2 = AbsoluteEntity(signature=np.eye(3), state=state.copy())
    return a1, a2


@pytest.fixture
def divergent_absolutes():
    """
    Two orthogonal absolutes with opposing directional states.
    """
    a1 = AbsoluteEntity(signature=np.eye(3), state=np.array([1.0, 0.0, 0.0]))
    a2 = AbsoluteEntity(signature=np.eye(3), state=np.array([0.0, 1.0, 0.0]))
    return a1, a2


@pytest.fixture
def identity_mediator():
    return MediatorSpace(metric=np.eye(3), label="identity_channel")


@pytest.fixture
def default_operator():
    return CrossInteractionOperator(weight_matrix=np.eye(3))


def test_information_flow_equilibrium(aligned_absolutes, identity_mediator, default_operator):
    """
    Ensure zero net information transfer when both absolutes share the same normalized state.
    """
    a1, a2 = aligned_absolutes
    engine = InformationTransfer()
    info_flux = engine.transfer(
        source=a1,
        target=a2,
        mediator=identity_mediator,
        interaction_operator=default_operator
    )

    assert isinstance(info_flux, float), "Information flux should return scalar."
    assert np.isclose(info_flux, 0.0, atol=1e-6), f"Expected near-zero transfer, got: {info_flux}"


def test_asymmetric_transfer_detected(divergent_absolutes, identity_mediator, default_operator):
    """
    Detect directional asymmetry in entropy transfer between divergent states.
    """
    a1, a2 = divergent_absolutes
    engine = InformationTransfer()

    flux_1_to_2 = engine.transfer(
        source=a1,
        target=a2,
        mediator=identity_mediator,
        interaction_operator=default_operator
    )
    flux_2_to_1 = engine.transfer(
        source=a2,
        target=a1,
        mediator=identity_mediator,
        interaction_operator=default_operator
    )

    assert flux_1_to_2 > 0, "Information flow from a1 to a2 should be non-zero."
    assert flux_2_to_1 > 0, "Information flow from a2 to a1 should be non-zero."
    assert not np.isclose(flux_1_to_2, flux_2_to_1), "Expected asymmetric transfer magnitudes."


def test_transfer_fails_without_state(identity_mediator, default_operator):
    """
    Validate that transfer raises an error if one of the absolutes lacks a state.
    """
    a1 = AbsoluteEntity(signature=np.eye(3), state=np.array([1.0, 0.0, 0.0]))
    a2 = AbsoluteEntity(signature=np.eye(3), state=None)

    engine = InformationTransfer()

    with pytest.raises(ValueError, match="Missing state vector in source or target"):
        engine.transfer(a1, a2, identity_mediator, default_operator)


def test_mediator_amplification_effect(divergent_absolutes):
    """
    Confirm that a weighted mediator metric increases the total information flux.
    """
    amp_metric = np.array([
        [2.0, 0.0, 0.0],
        [0.0, 3.0, 0.0],
        [0.0, 0.0, 4.0]
    ])
    mediator = MediatorSpace(metric=amp_metric)
    operator = CrossInteractionOperator(weight_matrix=np.eye(3))

    a1, a2 = divergent_absolutes
    engine = InformationTransfer()

    flux = engine.transfer(a1, a2, mediator, operator)
    assert flux > 1.0, f"Amplified mediator should yield large information flux. Got: {flux}"
