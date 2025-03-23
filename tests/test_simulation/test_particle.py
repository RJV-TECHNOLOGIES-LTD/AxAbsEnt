# tests/test_simulation/test_particle.py

import numpy as np
import pytest
from axabsent.simulation.particle import ParticleCollisionSimulation
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator

def create_entities(dim: int = 3):
    """Helper to generate two AbsoluteEntities with identity signatures."""
    return AbsoluteEntity(signature=np.eye(dim)), AbsoluteEntity(signature=np.eye(dim))

def create_interaction_operator(dim: int = 3):
    """Create a basic interaction operator from two absolute entities."""
    e1, e2 = create_entities(dim)
    return InteractionOperator([e1, e2], label="CollisionTest")

def test_particle_simulation_initialization():
    """Ensure the simulation initializes correctly with interactions and default energy scale."""
    interaction = create_interaction_operator()
    sim = ParticleCollisionSimulation([interaction], energy_scale=10.0)
    assert sim.energy_scale == 10.0
    assert isinstance(sim.interactions[0], InteractionOperator)

def test_generate_collision_state_shape():
    """Collision state should be a square matrix of the correct dimension (3x3)."""
    interaction = create_interaction_operator()
    sim = ParticleCollisionSimulation([interaction], energy_scale=10.0)
    state = sim.generate_collision_state()
    assert state.shape == (3, 3)
    assert np.all(np.isfinite(state))

def test_compute_energy_deposition_tensor_values():
    """The tensor should be a 3x3 finite matrix representing energy deposition across dimensions."""
    interaction = create_interaction_operator()
    sim = ParticleCollisionSimulation([interaction], energy_scale=10.0)
    tensor = sim.compute_energy_deposition_tensor()
    assert tensor.shape == (3, 3)
    assert np.all(np.isfinite(tensor))

def test_predict_trajectory_vector_properties():
    """Trajectory vector should be finite and match dimensionality."""
    interaction = create_interaction_operator()
    sim = ParticleCollisionSimulation([interaction], energy_scale=10.0)
    trajectory = sim.predict_trajectory_vector()
    assert trajectory.shape == (3,)
    assert np.all(np.isfinite(trajectory))

def test_collision_cross_section_is_nonnegative():
    """Cross-section calculation should yield a non-negative scalar value."""
    interaction = create_interaction_operator()
    sim = ParticleCollisionSimulation([interaction], energy_scale=10.0)
    cross_section = sim.compute_collision_cross_section()
    assert isinstance(cross_section, float)
    assert cross_section >= 0.0
