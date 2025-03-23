# api/tests/test_simulation.py

import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_simulate_cosmology_success():
    payload = {
        "type": "cosmological",
        "parameters": {
            "initial_scale": 1.0,
            "steps": 20,
            "dimension": 3
        }
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "expansion_tensor" in data
    assert "structure_map" in data
    assert isinstance(data["structure_map"], list)

def test_simulate_vacuum_energy_edge_case():
    payload = {
        "type": "vacuum",
        "parameters": {
            "fluctuation_range": [0.0, 0.0],  # edge: zero fluctuations
            "samples": 50
        }
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    assert "energy_density_tensor" in response.json()

def test_simulate_invalid_type_returns_422():
    payload = {
        "type": "nonsense",
        "parameters": {}
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code in [400, 422]
