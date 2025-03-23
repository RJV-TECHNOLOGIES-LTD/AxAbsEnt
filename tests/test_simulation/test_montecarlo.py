# tests/test_simulation/test_montecarlo.py

import numpy as np
import pytest
from axabsent.simulation.montecarlo import MonteCarloSimulation
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator

def create_entities(dim: int = 3):
    """Returns two AbsoluteEntities with identity signatures."""
    return AbsoluteEntity(signature=np.eye(dim)), AbsoluteEntity(signature=np.eye(dim))

def create_interaction(dim: int = 3) -> InteractionOperator:
    """Creates a valid interaction between two identity entities."""
    e1, e2 = create_entities(dim)
    return InteractionOperator([e1, e2], label="MonteCarloTest")

def test_initialization():
    """Test that MonteCarloSimulation initializes correctly with default parameters."""
    interaction = create_interaction()
    mc = MonteCarloSimulation([interaction], num_samples=500)
    assert mc.num_samples == 500
    assert mc.interactions[0].label == "MonteCarloTest"

def test_generate_random_state():
    """Ensure that random states generated are finite and of correct shape."""
    interaction = create_interaction()
    mc = MonteCarloSimulation([interaction])
    state = mc.generate_random_state(dim=3)
    assert state.shape == (3,)
    assert np.all(np.isfinite(state))

def test_run_returns_correct_shape():
    """Run should return a result matrix with shape (num_samples, result_dim)."""
    interaction = create_interaction()
    mc = MonteCarloSimulation([interaction], num_samples=100)
    results = mc.run()
    assert results.shape[0] == 100
    assert results.shape[1] == 3  # Assuming 3D states were used

def test_aggregate_results_returns_vector():
    """Check that the aggregated result is a finite vector of expected shape."""
    interaction = create_interaction()
    mc = MonteCarloSimulation([interaction], num_samples=100)
    mc.run()
    aggregate = mc.aggregate_results()
    assert aggregate.shape == (3,)
    assert np.all(np.isfinite(aggregate))

def test_repeatability_with_seed():
    """Verify that setting a random seed yields consistent results."""
    interaction = create_interaction()
    mc1 = MonteCarloSimulation([interaction], num_samples=10, seed=42)
    mc2 = MonteCarloSimulation([interaction], num_samples=10, seed=42)
    r1 = mc1.run()
    r2 = mc2.run()
    np.testing.assert_array_almost_equal(r1, r2)
