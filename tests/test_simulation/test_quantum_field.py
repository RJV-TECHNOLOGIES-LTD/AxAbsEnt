# tests/test_simulation/test_quantum_field.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.mediator import MediatorSpace
from axabsent.simulation.quantum_field import QuantumFieldSimulation

def create_identity_entity(dim: int = 3) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with an identity signature of given dimension."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 3) -> MediatorSpace:
    """Helper function to create a MediatorSpace with an identity curvature tensor."""
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def test_quantum_field_initialization():
    """
    Test that the quantum field is initialized as a normalized composite state.
    The initialized field should be a square matrix of the correct dimension and normalized.
    """
    entity = create_identity_entity(3)
    mediator = create_identity_mediator(3)
    sim = QuantumFieldSimulation([entity], mediator, time_step=0.01, total_time=0.05)
    field = sim.initialize_field()
    assert field.shape == (3, 3)
    # The field is normalized: Frobenius norm should be 1
    norm = np.linalg.norm(field, ord='fro')
    assert np.isclose(norm, 1.0)

def test_quantum_field_evolution():
    """
    Test that the quantum field evolves over the simulation time.
    After running the simulation, the current time should be at least equal to the total time,
    and the final field state should maintain the correct dimensions.
    """
    entity = create_identity_entity(3)
    mediator = create_identity_mediator(3)
    sim = QuantumFieldSimulation([entity], mediator, time_step=0.01, total_time=0.05)
    sim.initialize_field()
    final_state = sim.run()
    assert sim.current_time >= sim.total_time
    assert final_state.shape == (3, 3)

def test_field_entropy():
    """
    Test that the entropy of the quantum field state can be computed.
    The computed entropy should be a non-negative float.
    """
    entity = create_identity_entity(3)
    mediator = create_identity_mediator(3)
    sim = QuantumFieldSimulation([entity], mediator, time_step=0.01, total_time=0.05)
    sim.initialize_field()
    sim.run()
    entropy = sim.compute_field_entropy()
    assert isinstance(entropy, float)
    assert entropy >= 0.0
