# tests/test_experimental/test_particle_physics.py

import numpy as np
import pytest

from axabsent.experimental.particle_physics import ParticleCollisionPredictor
from axabsent.experimental.signatures import SignatureEvaluator


@pytest.fixture
def mock_collision_config():
    """
    Provides mock collision parameters simulating a high-energy LHC-like event.
    """
    return {
        "energy_TeV": 13.0,
        "luminosity_fb": 150,
        "beam_profile": "gaussian",
        "entropy_seed": 42,
        "expected_channels": ["γγ", "ZZ", "tt̄", "μμ"]
    }


@pytest.fixture
def predictor():
    return ParticleCollisionPredictor()


def test_collision_entropy_signature(mock_collision_config, predictor):
    """
    Ensure that entropy topology generated from collisions is reproducible and physical.
    """
    entropy_map = predictor.generate_entropy_topology(mock_collision_config)

    assert isinstance(entropy_map, np.ndarray)
    assert entropy_map.shape == (64, 64)
    assert np.min(entropy_map) >= 0.0
    assert np.max(entropy_map) <= 1.0

    center = entropy_map[32, 32]
    edge = entropy_map[0, 0]
    assert center > edge, "Entropy must concentrate at impact center."


def test_resonance_pattern_generation(mock_collision_config, predictor):
    """
    Verify that collision outputs generate resonance traces for high-density decay signatures.
    """
    resonance_pattern = predictor.compute_resonance_traces(mock_collision_config)

    assert isinstance(resonance_pattern, np.ndarray)
    assert resonance_pattern.ndim == 2
    assert resonance_pattern.shape == (64, 64)

    max_r = np.max(resonance_pattern)
    assert 0.0 <= max_r <= 1.0, "Resonance values must be normalized."


def test_signature_from_entropy_and_resonance(mock_collision_config, predictor):
    """
    Test the full prediction signature pipeline from entropy + resonance maps.
    """
    entropy = predictor.generate_entropy_topology(mock_collision_config)
    resonance = predictor.compute_resonance_traces(mock_collision_config)

    evaluator = SignatureEvaluator()
    signature = evaluator.evaluate_collision_signature(entropy, resonance)

    assert isinstance(signature, dict)
    assert "signature_hash" in signature
    assert "conformity_score" in signature
    assert signature["conformity_score"] > 0.6, "Predicted collision signature too low in conformity."


def test_low_energy_collision_reduces_entropy():
    """
    Ensure entropy field is significantly reduced for low-energy beam configurations.
    """
    low_energy = {
        "energy_TeV": 1.0,
        "luminosity_fb": 20,
        "beam_profile": "flat",
        "entropy_seed": 7,
        "expected_channels": ["ππ"]
    }

    predictor = ParticleCollisionPredictor()
    entropy_map = predictor.generate_entropy_topology(low_energy)

    assert np.mean(entropy_map) < 0.2, "Low-energy collisions must not produce high entropy fields."
