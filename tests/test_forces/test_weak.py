# tests/test_forces/test_weak.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity
from axabsent.forces.weak import WeakForceField
from axabsent.core.mediator import MediatorSpace

def create_identity_entity(dim: int = 2) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with an identity signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 2) -> MediatorSpace:
    """
    Helper function to create a MediatorSpace with an identity curvature tensor.
    """
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def test_weak_force_field_initialization():
    """Test that WeakForceField is correctly initialized with two entities and a mediator."""
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    wf = WeakForceField([entity1, entity2], mediator)
    assert wf.entities is not None
    assert wf.mediator is mediator

def test_compute_stress_index():
    """Verify that the stress index is computed as a finite float."""
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    wf = WeakForceField([entity1, entity2], mediator)
    stress = wf.compute_stress_index()
    assert isinstance(stress, float)
    assert np.isfinite(stress)

def test_compute_parity_break_tensor():
    """Check that the parity break tensor is a finite 2x2 array."""
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    wf = WeakForceField([entity1, entity2], mediator)
    tensor = wf.compute_parity_break_tensor()
    assert tensor.shape == (2, 2)
    assert np.all(np.isfinite(tensor))

def test_compute_transition_probability():
    """
    Ensure that the computed transition probability is within the expected range,
    given the tanh function's output is between -1 and 1.
    """
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    wf = WeakForceField([entity1, entity2], mediator)
    prob = wf.compute_transition_probability()
    assert -1 <= prob <= 1
