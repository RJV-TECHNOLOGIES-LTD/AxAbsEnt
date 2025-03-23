# tests/test_forces/test_electromagnetic.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity
from axabsent.forces.electromagnetic import ElectromagneticField
from axabsent.core.mediator import MediatorSpace

def create_identity_entity(dim: int = 2) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with an identity signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 2) -> MediatorSpace:
    """
    Helper function to create a MediatorSpace with an identity curvature tensor.
    """
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def test_em_field_initialization():
    """Test that ElectromagneticField is correctly initialized with two entities and a mediator."""
    source = create_identity_entity(2)
    target = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    em_field = ElectromagneticField(source, target, mediator)
    assert em_field.source is source
    assert em_field.target is target
    assert em_field.mediator is mediator

def test_compute_flux_matrix():
    """
    For two identity entities and an identity mediator, the flux matrix should be computed
    and be a finite 2x2 array.
    """
    source = create_identity_entity(2)
    target = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    em_field = ElectromagneticField(source, target, mediator)
    flux = em_field.compute_flux_matrix()
    assert flux.shape == (2, 2)
    assert np.all(np.isfinite(flux))

def test_compute_field_vector():
    """
    Test that the electromagnetic field vector is computed and has the correct shape.
    """
    source = create_identity_entity(2)
    target = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    em_field = ElectromagneticField(source, target, mediator)
    field_vector = em_field.compute_field_vector()
    # Expect a vector of length equal to the dimension (2)
    assert field_vector.shape == (2,)
    assert np.all(np.isfinite(field_vector))

def test_compute_potential_vector():
    """
    Test that the potential vector is computed correctly.
    """
    source = create_identity_entity(2)
    target = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    em_field = ElectromagneticField(source, target, mediator)
    potential_vector = em_field.compute_potential_vector()
    # The potential vector should be a finite array of length equal to the dimension (2)
    assert potential_vector.shape == (2,)
    assert np.all(np.isfinite(potential_vector))

def test_detect_resonance():
    """
    Checks that the resonance detection method returns a boolean.
    Since the system is based on identities, the transfer may be nearly reversible,
    so the method should return a boolean without errors.
    """
    source = create_identity_entity(2)
    target = create_identity_entity(2)
    mediator = create_identity_mediator(2)
    em_field = ElectromagneticField(source, target, mediator)
    resonance_flag = em_field.detect_resonance(tolerance=1e-6)
    assert isinstance(resonance_flag, bool)
