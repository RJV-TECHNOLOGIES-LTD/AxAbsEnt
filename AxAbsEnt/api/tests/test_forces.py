# api/tests/test_forces.py

import numpy as np
import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_force_extraction_gravity():
    payload = {
        "type": "gravitational",
        "input_tensor": [
            [1.0, 0.1, 0.0],
            [0.1, 1.2, 0.2],
            [0.0, 0.2, 0.9]
        ],
        "parameters": {
            "mass_density": 1.0,
            "curvature_threshold": 0.01
        }
    }
    response = client.post("/forces/extract", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "force_tensor" in result
    assert isinstance(result["force_tensor"], list)

def test_force_decomposition_success():
    payload = {
        "tensor": [
            [2.1, 0.3, 0.0],
            [0.3, 1.8, 0.4],
            [0.0, 0.4, 1.1]
        ]
    }
    response = client.post("/forces/decompose", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "gravitational_component" in result
    assert "electromagnetic_component" in result
    assert isinstance(result["electromagnetic_component"], list)

def test_force_unification_consistency():
    payload = {
        "components": {
            "gravitational": [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]],
            "electromagnetic": [[0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5]],
            "strong": [[0.2, 0, 0], [0, 0.2, 0], [0, 0, 0.2]],
            "weak": [[0.1, 0, 0], [0, 0.1, 0], [0, 0, 0.1]]
        }
    }
    response = client.post("/forces/unify", json=payload)
    assert response.status_code == 200
    unified = response.json().get("unified_tensor")
    assert unified is not None
    assert isinstance(unified, list)
    assert len(unified) == 3
