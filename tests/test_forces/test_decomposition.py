# tests/test_forces/test_decomposition.py

import pytest
import numpy as np
from axabsent.forces.decomposition import ForceDecomposer
from axabsent.core.absolute import AbsoluteEntity

@pytest.fixture
def synthetic_absolute():
    """Creates a synthetic AbsoluteEntity with embedded properties and state."""
    abs_entity = AbsoluteEntity(
        signature=np.array([[1.0, 0.0], [0.0, 1.0]]),
        state=np.array([0.6, -0.8]),
    )
    abs_entity.set_property("charge_density", 1.5)
    abs_entity.set_property("mass_density", 9.81)
    return abs_entity

@pytest.fixture
def interaction_tensor():
    """Simulates an interaction tensor emerging from a mediator space."""
    return np.array([
        [0.2, 0.5],
        [-0.3, 0.7]
    ])

@pytest.fixture
def ceft_tensor():
    """Provides a synthetic curvature-entropy flux tensor."""
    return np.array([
        [1.2, 0.4],
        [0.4, 0.9]
    ])

def test_decompose_force_vector_components(synthetic_absolute, interaction_tensor, ceft_tensor):
    decomposer = ForceDecomposer()
    result = decomposer.decompose(
        absolute=synthetic_absolute,
        interaction_tensor=interaction_tensor,
        ceft_tensor=ceft_tensor
    )

    assert isinstance(result, dict), "Decomposition output should be a dictionary."
    assert all(k in result for k in ["gravity", "electromagnetic", "strong", "weak"]), "Missing force components."
    assert all(isinstance(v, np.ndarray) for v in result.values()), "Each force component must be a NumPy array."
    assert all(v.shape == (2,) for v in result.values()), "Each force component must match the entity's vector shape."

def test_zero_tensor_decomposition(synthetic_absolute):
    interaction_tensor = np.zeros((2, 2))
    ceft_tensor = np.zeros((2, 2))
    decomposer = ForceDecomposer()
    result = decomposer.decompose(
        absolute=synthetic_absolute,
        interaction_tensor=interaction_tensor,
        ceft_tensor=ceft_tensor
    )

    for component in result.values():
        assert np.allclose(component, np.zeros(2)), "All components should be zero when tensors are null."

def test_force_projection_consistency(synthetic_absolute, interaction_tensor, ceft_tensor):
    decomposer = ForceDecomposer()
    result = decomposer.decompose(
        absolute=synthetic_absolute,
        interaction_tensor=interaction_tensor,
        ceft_tensor=ceft_tensor
    )

    total_force = sum(result.values())
    projected = synthetic_absolute.project_state(interaction_tensor)
    assert total_force.shape == projected.shape, "Projected state and total force should be dimensionally consistent."

