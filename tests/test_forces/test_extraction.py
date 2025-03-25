# tests/test_forces/test_extraction.py

import pytest
import numpy as np
from axabsent.forces.extraction import ForceExtractor
from axabsent.core.absolute import AbsoluteEntity

@pytest.fixture
def absolute_sample():
    """Creates an AbsoluteEntity with internal entropy and spatial state."""
    abs_entity = AbsoluteEntity(
        signature=np.identity(3),
        state=np.array([0.0, 1.0, -1.0])
    )
    abs_entity.set_property("entropy_density", 2.4)
    abs_entity.set_property("gradient_field", np.array([0.1, -0.3, 0.2]))
    return abs_entity

@pytest.fixture
def symmetry_decay_tensor():
    """Returns a synthetic Symmetry Decay Tensor (SDI-driven)."""
    return np.array([
        [0.95, -0.01, 0.00],
        [-0.01, 0.90, 0.02],
        [0.00, 0.02, 0.85]
    ])

@pytest.fixture
def information_gradient():
    """Returns a synthetic information gradient field vector."""
    return np.array([0.4, -0.5, 0.6])

def test_extract_force_vector(absolute_sample, symmetry_decay_tensor, information_gradient):
    extractor = ForceExtractor()

    force_vector = extractor.extract(
        absolute=absolute_sample,
        symmetry_tensor=symmetry_decay_tensor,
        info_gradient=information_gradient
    )

    assert isinstance(force_vector, np.ndarray), "Force output must be a NumPy array."
    assert force_vector.shape == (3,), "Force vector must match Absolute state dimension."
    assert not np.any(np.isnan(force_vector)), "Force vector contains invalid numerical values."

def test_zero_gradient_behavior(absolute_sample, symmetry_decay_tensor):
    extractor = ForceExtractor()
    zero_gradient = np.zeros(3)

    force_vector = extractor.extract(
        absolute=absolute_sample,
        symmetry_tensor=symmetry_decay_tensor,
        info_gradient=zero_gradient
    )

    assert np.allclose(force_vector, np.zeros(3)), "Zero gradient should yield zero force."
