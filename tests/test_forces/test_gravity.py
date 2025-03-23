# tests/test_forces/test_gravity.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity
from axabsent.forces.gravity import GravitationalField
from axabsent.core.mediator import MediatorSpace

def create_identity_entity(dim: int = 2) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with an identity signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 2) -> MediatorSpace:
    """
    Helper function to create a MediatorSpace with a given dimension.
    Uses an identity matrix as the curvature tensor.
    """
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def test_gravitational_field_initialization():
    """Test that a GravitationalField can be correctly initialized with two entities and a mediator."""
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    gf = GravitationalField([entity1, entity2], mediator)
    assert gf.entities is not None
    assert gf.mediator is mediator

def test_compute_curvature_flux():
    """
    For a mediator with an identity curvature tensor, the connection form becomes:
        curvature_tensor.T @ curvature_tensor = I,
    so the trace is equal to the dimension (2 for a 2x2 identity).
    """
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    gf = GravitationalField([entity1, entity2], mediator)
    flux = gf.compute_curvature_flux()
    np.testing.assert_almost_equal(flux, 2.0, decimal=6)

def test_compute_field_tensor():
    """
    Checks that the computed field tensor is a finite 2x2 array.
    """
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    gf = GravitationalField([entity1, entity2], mediator)
    tensor = gf.compute_field_tensor()
    assert tensor.shape == (2, 2)
    assert np.all(np.isfinite(tensor))

def test_compute_potential_energy():
    """
    Verifies that the gravitational potential energy is computed and returns a positive float.
    """
    entity1 = create_identity_entity(2)
    entity2 = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    gf = GravitationalField([entity1, entity2], mediator)
    potential = gf.compute_potential_energy()
    assert potential > 0
