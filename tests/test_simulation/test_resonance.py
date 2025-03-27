# tests/test_simulation/test_resonance.py

import numpy as np
import pytest
from axabsent.simulation.resonance import ResonanceSimulation
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator

def create_identity_entity(dim: int = 3) -> AbsoluteEntity:
    """Helper function to create an AbsoluteEntity with identity signature."""
    return AbsoluteEntity(signature=np.eye(dim))

def create_basic_interaction(dim: int = 3) -> InteractionOperator:
    """Creates a basic valid interaction between two AbsoluteEntities."""
    entity1 = create_identity_entity(dim)
    entity2 = create_identity_entity(dim)
    return InteractionOperator([entity1, entity2], label="ResonanceTest")

def test_resonance_simulation_initialization():
    """Test that ResonanceSimulation is correctly initialized."""
    interaction = create_basic_interaction()
    sim = ResonanceSimulation([interaction], detection_threshold=0.01)
    assert sim.interactions is not None
    assert sim.detection_threshold == 0.01

def test_detect_resonance_signatures():
    """
    Ensure that the resonance detection method returns a list of booleans.
    Given identity interactions and low threshold, expect True or False per interaction.
    """
    interaction = create_basic_interaction()
    sim = ResonanceSimulation([interaction], detection_threshold=1e-6)
    results = sim.detect_resonance_signatures()
    assert isinstance(results, list)
    assert all(isinstance(val, bool) for val in results)

def test_analyze_dynamics_returns_matrix():
    """Check that dynamics analysis returns a finite square matrix."""
    interaction = create_basic_interaction()
    sim = ResonanceSimulation([interaction], detection_threshold=0.01)
    dyn = sim.analyze_dynamics()
    assert dyn.shape[0] == dyn.shape[1]
    assert np.all(np.isfinite(dyn))

def test_signal_amplification_returns_nonzero_matrix():
    """
    Signal amplification should return a matrix where values are scaled up.
    """
    interaction = create_basic_interaction()
    sim = ResonanceSimulation([interaction], detection_threshold=0.01)
    amplified = sim.signal_amplification()
    assert amplified.shape[0] == amplified.shape[1]
    assert np.any(np.abs(amplified) > 0)
