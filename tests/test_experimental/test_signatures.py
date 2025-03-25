# tests/test_experimental/test_signatures.py

import numpy as np
import pytest

from axabsent.experimental.signatures import SignatureEvaluator


@pytest.fixture
def synthetic_entropy_tensor():
    """
    Create a normalized 2D entropy map centered around the interaction locus.
    """
    x = np.linspace(-1, 1, 64)
    y = np.linspace(-1, 1, 64)
    X, Y = np.meshgrid(x, y)
    field = np.exp(-(X**2 + Y**2) * 10)
    return field / np.max(field)


@pytest.fixture
def synthetic_resonance_tensor():
    """
    Create a synthetic resonance map with localized hotspots.
    """
    tensor = np.zeros((64, 64))
    tensor[20, 20] = 1.0
    tensor[40, 40] = 0.8
    tensor[32, 32] = 0.6
    return tensor


@pytest.fixture
def evaluator():
    return SignatureEvaluator()


def test_signature_hash_consistency(synthetic_entropy_tensor, synthetic_resonance_tensor, evaluator):
    """
    The signature hash must remain deterministic for the same input tensors.
    """
    sig1 = evaluator.evaluate_collision_signature(
        entropy_tensor=synthetic_entropy_tensor,
        resonance_tensor=synthetic_resonance_tensor
    )
    sig2 = evaluator.evaluate_collision_signature(
        entropy_tensor=synthetic_entropy_tensor,
        resonance_tensor=synthetic_resonance_tensor
    )

    assert sig1["signature_hash"] == sig2["signature_hash"], "Signature hash must be consistent."
    assert np.isclose(sig1["conformity_score"], sig2["conformity_score"]), "Conformity score mismatch."


def test_conformity_score_with_random_noise(evaluator):
    """
    Adding entropy noise should reduce conformity score measurably.
    """
    base_entropy = np.ones((64, 64)) * 0.5
    base_resonance = np.zeros((64, 64))
    base_resonance[32, 32] = 1.0

    baseline = evaluator.evaluate_collision_signature(base_entropy, base_resonance)

    noise = np.random.normal(0, 0.1, size=(64, 64))
    noisy_entropy = np.clip(base_entropy + noise, 0.0, 1.0)

    altered = evaluator.evaluate_collision_signature(noisy_entropy, base_resonance)

    assert altered["conformity_score"] < baseline["conformity_score"], "Noise should reduce conformity score."


def test_cosmological_signature_structure(synthetic_entropy_tensor, synthetic_resonance_tensor, evaluator):
    """
    Validate that cosmological signatures also produce valid hash and score.
    """
    sig = evaluator.evaluate_cosmological_signature(
        entropy_tensor=synthetic_entropy_tensor,
        resonance_tensor=synthetic_resonance_tensor
    )

    assert isinstance(sig, dict)
    assert "signature_hash" in sig
    assert "conformity_score" in sig
    assert 0.0 <= sig["conformity_score"] <= 1.0


def test_invalid_tensor_shape_raises():
    """
    Evaluator must reject tensors with incompatible dimensions.
    """
    bad_tensor = np.ones((32, 64, 2))  # 3D tensor instead of 2D

    evaluator = SignatureEvaluator()
    with pytest.raises(ValueError, match="2D tensor expected"):
        evaluator.evaluate_collision_signature(bad_tensor, bad_tensor)
