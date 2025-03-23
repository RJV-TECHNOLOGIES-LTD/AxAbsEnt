# tests/test_core/test_interaction.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator

def create_identity_entity(dim: int = 2) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with an identity signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def test_interaction_requires_multiple_entities():
    """Verify that an interaction requires at least two Absolute Entities."""
    entity = create_identity_entity(2)
    with pytest.raises(ValueError):
        InteractionOperator([entity], label="SingleEntityInteraction")

def test_compose_tensor_field():
    """Test that composing tensor fields from two identity entities produces 2*I."""
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    interaction = InteractionOperator([entity1, entity2], label="TestInteraction")
    tensor_field = interaction.compose_tensor_field()
    expected = 2 * np.eye(2)
    np.testing.assert_array_almost_equal(tensor_field, expected)

def test_compute_selection_scalar():
    """
    Verify that the selection scalar is computed correctly.
    Each identity matrix has a trace of 2, so the average over two entities should be 2.
    """
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    interaction = InteractionOperator([entity1, entity2], label="TestInteraction")
    scalar = interaction.compute_selection_scalar()
    assert np.isclose(scalar, 2.0)

def test_calculate_interaction_entropy():
    """
    Test that the interaction entropy is calculated correctly.
    For two identity matrices, the composed tensor field is 2I,
    whose Frobenius norm is 2*sqrt(2) for a 2x2 identity matrix.
    """
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    interaction = InteractionOperator([entity1, entity2], label="TestInteraction")
    tensor_field = interaction.compose_tensor_field()  # Expected to be 2*I
    entropy = interaction.calculate_interaction_entropy()
    expected_entropy = 2 * np.sqrt(2)
    np.testing.assert_almost_equal(entropy, expected_entropy, decimal=6)
