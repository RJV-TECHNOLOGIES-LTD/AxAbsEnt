# tests/test_experimental/test_cosmological.py

import numpy as np
import pytest

from axabsent.experimental.cosmological import CosmologicalPredictor
from axabsent.experimental.signatures import SignatureEvaluator


@pytest.fixture
def mock_cosmic_parameters():
    """
    Provides a mock configuration of cosmological constants aligned with Λ-CDM limits.
    """
    return {
        "H0": 67.4,                         # Hubble parameter in km/s/Mpc
        "Ωm": 0.315,                        # Matter density
        "ΩΛ": 0.685,                        # Dark energy density
        "σ8": 0.811,                        # Matter fluctuation amplitude
        "ns": 0.965,                        # Spectral index
        "curvature": 0.0                   # Flat universe
    }


@pytest.fixture
def predictor():
    return CosmologicalPredictor()


def test_entropy_field_structure(mock_cosmic_parameters, predictor):
    """
    Validate that the entropy curvature field has the expected dimensional shape
    and smooth decay characteristics.
    """
    entropy_field = predictor.generate_entropy_tensor(mock_cosmic_parameters)

    assert isinstance(entropy_field, np.ndarray)
    assert entropy_field.ndim == 2
    assert entropy_field.shape[0] == entropy_field.shape[1], "Entropy field must be square."

    # Check that entropy decays radially from center
    center_value = entropy_field[entropy_field.shape[0] // 2, entropy_field.shape[1] // 2]
    edge_value = entropy_field[0, 0]
    assert center_value > edge_value, "Entropy must decay outward from curvature origin."


def test_resonance_distribution(mock_cosmic_parameters, predictor):
    """
    Ensure that cosmic resonances (entropy spikes) are within statistically valid bounds.
    """
    resonance_map = predictor.compute_resonance_distribution(mock_cosmic_parameters)
    assert isinstance(resonance_map, np.ndarray)
    assert resonance_map.shape == (128, 128)

    mean_resonance = np.mean(resonance_map)
    assert mean_resonance < 0.5, "Mean resonance amplitude too high for physical cosmology."
    assert np.max(resonance_map) <= 1.0, "Resonance values must be normalized to [0,1]."


def test_prediction_signature_verification(mock_cosmic_parameters, predictor):
    """
    Confirm that the resulting entropy and resonance tensors match the expected falsifiable signature.
    """
    entropy = predictor.generate_entropy_tensor(mock_cosmic_parameters)
    resonance = predictor.compute_resonance_distribution(mock_cosmic_parameters)

    evaluator = SignatureEvaluator()
    signature = evaluator.evaluate_cosmological_signature(entropy_tensor=entropy, resonance_tensor=resonance)

    assert isinstance(signature, dict)
    assert "signature_hash" in signature
    assert "conformity_score" in signature

    assert 0.0 <= signature["conformity_score"] <= 1.0, "Conformity score must be normalized."
    assert signature["conformity_score"] > 0.75, "Prediction does not meet falsifiability threshold."


def test_prediction_instability_warning():
    """
    Ensure model raises a warning or returns low score when curvature is extreme.
    """
    extreme_params = {
        "H0": 90.0,
        "Ωm": 0.99,
        "ΩΛ": 0.01,
        "σ8": 1.4,
        "ns": 1.2,
        "curvature": 0.25  # Positive curvature inflation
    }

    predictor = CosmologicalPredictor()
    entropy = predictor.generate_entropy_tensor(extreme_params)
    resonance = predictor.compute_resonance_distribution(extreme_params)

    evaluator = SignatureEvaluator()
    signature = evaluator.evaluate_cosmological_signature(entropy, resonance)

    assert signature["conformity_score"] < 0.4, "Extreme model must fail conformity."
