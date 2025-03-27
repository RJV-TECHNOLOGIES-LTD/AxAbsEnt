# tests/test_forces/test_strong.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator
from axabsent.core.interaction_composition import InteractionComposition
from axabsent.forces.strong import StrongForceField
from axabsent.core.mediator import MediatorSpace

def create_identity_entity(dim: int = 2) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with an identity signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 2) -> MediatorSpace:
    """
    Helper function to create a MediatorSpace with an identity curvature tensor.
    """
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def create_interaction_composition(dim: int = 2) -> InteractionComposition:
    """
    Helper function to create an InteractionComposition from two identity entities.
    """
    entity1 = create_identity_entity(dim)
    entity2 = create_identity_entity(dim)
    interaction = InteractionOperator([entity1, entity2], label="TestInteraction")
    mediator = create_identity_mediator(dim)
    # Create a composition with one interaction operator and its corresponding mediator.
    comp = InteractionComposition([interaction], [mediator])
    return comp

def test_strong_force_field_initialization():
    """Verify that StrongForceField is correctly initialized."""
    comp = create_interaction_composition(2)
    mediator = create_identity_mediator(2)
    sff = StrongForceField([comp], mediator, steps=3)
    assert sff.compositions is not None
    assert sff.mediator is mediator

def test_build_entanglement_matrix():
    """Test that the entanglement matrix is built with correct dimensions."""
    comp = create_interaction_composition(2)
    mediator = create_identity_mediator(2)
    sff = StrongForceField([comp], mediator, steps=3)
    ent_matrix = sff.build_entanglement_matrix()
    # Expect a square matrix with dimensions equal to mediator dimension.
    assert ent_matrix.shape[0] == ent_matrix.shape[1] == 2

def test_compute_binding_energy():
    """Ensure that the computed binding energy is a positive value."""
    comp = create_interaction_composition(2)
    mediator = create_identity_mediator(2)
    sff = StrongForceField([comp], mediator, steps=3)
    energy = sff.compute_binding_energy()
    assert energy > 0

def test_generate_confinement_tensor():
    """Check that the confinement tensor is a finite 2x2 array."""
    comp = create_interaction_composition(2)
    mediator = create_identity_mediator(2)
    sff = StrongForceField([comp], mediator, steps=3)
    tensor = sff.generate_confinement_tensor()
    assert tensor.shape == (2, 2)
    assert np.all(np.isfinite(tensor))
