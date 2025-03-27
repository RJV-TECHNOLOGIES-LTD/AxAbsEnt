# tests/test_simulation/test_cosmological.py

import numpy as np
import pytest
from axabsent.simulation.cosmological import CosmologicalSimulation
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.mediator import MediatorSpace

def create_identity_entity(dim: int = 3) -> AbsoluteEntity:
    """Creates an AbsoluteEntity with an identity matrix signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 3) -> MediatorSpace:
    """Creates a MediatorSpace with identity curvature tensor."""
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def test_cosmological_simulation_initialization():
    """Test correct initialization of the simulation."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = CosmologicalSimulation([entity], mediator, initial_scale=1.0)
    assert sim.scale_factor == 1.0
    assert sim.mediator.dimension == 3

def test_compute_expansion_tensor_returns_correct_shape():
    """Check that expansion tensor is computed and correctly shaped."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = CosmologicalSimulation([entity], mediator, initial_scale=1.0)
    tensor = sim.compute_expansion_tensor()
    assert tensor.shape == (3, 3)
    assert np.all(np.isfinite(tensor))

def test_evolve_scale_factor_updates_correctly():
    """
    Run multiple steps and verify that the scale factor increases,
    assuming positive expansion rate.
    """
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = CosmologicalSimulation([entity], mediator, initial_scale=1.0)
    sim.evolve(dynamics_steps=10)
    assert sim.scale_factor > 1.0

def test_generate_structure_map_output():
    """Ensure the structure map is a finite square matrix."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = CosmologicalSimulation([entity], mediator, initial_scale=1.0)
    structure = sim.generate_structure_map()
    assert structure.shape == (3, 3)
    assert np.all(np.isfinite(structure))
