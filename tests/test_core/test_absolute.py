# tests/test_core/test_absolute.py

import numpy as np
import pytest
from axabsent.core.absolute import AbsoluteEntity, AbsoluteInvariantError

def test_valid_signature():
    # Valid signature: symmetric and square matrix.
    signature = np.array([[1, 0], [0, 1]])
    entity = AbsoluteEntity(signature=signature)
    assert entity.signature.shape == (2, 2)

def test_invalid_signature_not_square():
    # Non-square matrix should raise a ValueError.
    sig = np.array([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError):
        AbsoluteEntity(signature=sig)

def test_invalid_signature_not_symmetric():
    # Non-symmetric matrix should raise a ValueError.
    sig = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        AbsoluteEntity(signature=sig)

def test_set_and_get_property():
    # Verify that properties can be set and retrieved.
    signature = np.array([[1, 0], [0, 1]])
    entity = AbsoluteEntity(signature=signature)
    entity.set_property("mass", 1.23)
    assert entity.get_property("mass") == 1.23

def test_project_state_without_state():
    # Attempting to project a state when none is defined should raise an AbsoluteInvariantError.
    signature = np.array([[1, 0], [0, 1]])
    entity = AbsoluteEntity(signature=signature)
    with pytest.raises(AbsoluteInvariantError):
        entity.project_state(np.eye(2))
