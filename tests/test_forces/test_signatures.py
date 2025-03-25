# tests/test_forces/test_signatures.py

import pytest
import numpy as np
from axabsent.forces.signatures import ForceSignatureAnalyzer
from axabsent.core.absolute import AbsoluteEntity

@pytest.fixture
def synthetic_force_fields():
    """Returns a dictionary of synthetic force vectors."""
    return {
        "gravity": np.array([0.0, -9.81]),
        "electromagnetic": np.array([1.2, 0.8]),
        "strong": np.array([5.5, -3.1]),
        "weak": np.array([0.01, 0.03])
    }

@pytest.fixture
def absolute_origin():
    """Returns an AbsoluteEntity representing the origin of the force field."""
    abs_entity = AbsoluteEntity(
        signature=np.array([[1.0, 0.0], [0.0, 1.0]]),
        state=np.array([0.5, 0.5])
    )
    abs_entity.set_property("entropy_density", 1.0)
    return abs_entity

def test_force_signature_generation(synthetic_force_fields, absolute_origin):
    analyzer = ForceSignatureAnalyzer()
    signature_result = analyzer.generate_signatures(
        absolute=absolute_origin,
        forces=synthetic_force_fields
    )

    assert isinstance(signature_result, dict), "Signature result must be a dictionary."
    assert all(k in signature_result for k in ["gravity", "electromagnetic", "strong", "weak"]), "Missing force keys."

    for key, signature in signature_result.items():
        assert isinstance(signature, np.ndarray), f"{key} signature is not a NumPy array."
        assert signature.shape == (2, 2), f"{key} signature must be 2x2 matrix."
        assert np.allclose(signature, signature.T), f"{key} signature must be symmetric."

def test_entropy_consistency(synthetic_force_fields, absolute_origin):
    analyzer = ForceSignatureAnalyzer()
    signatures = analyzer.generate_signatures(
        absolute=absolute_origin,
        forces=synthetic_force_fields
    )

    for key, matrix in signatures.items():
        entropy_trace = np.trace(matrix)
        assert entropy_trace > 0, f"{key} entropy trace must be positive."
