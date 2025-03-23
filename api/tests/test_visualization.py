# api/tests/test_visualization.py

import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_interaction_graph_visualization():
    payload = {
        "type": "interaction_graph",
        "data": {
            "nodes": ["A", "B", "C"],
            "edges": [
                {"source": "A", "target": "B", "weight": 0.8},
                {"source": "B", "target": "C", "weight": 0.6}
            ]
        }
    }
    response = client.post("/visualization", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "image_base64" in result
    assert result["type"] == "interaction_graph"

def test_force_field_visualization():
    payload = {
        "type": "force_field",
        "tensor": [
            [0.5, 0.2, 0.1],
            [0.2, 0.8, 0.3],
            [0.1, 0.3, 0.6]
        ],
        "field_name": "Gravitational"
    }
    response = client.post("/visualization", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "image_base64" in result
    assert result["metadata"]["field_name"] == "Gravitational"

def test_entropy_map_visualization():
    payload = {
        "type": "entropy_map",
        "values": [0.1, 0.2, 0.3, 0.4, 0.5],
        "dimensions": [1, 5]
    }
    response = client.post("/visualization", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "image_base64" in result
    assert result["type"] == "entropy_map"

def test_invalid_visualization_type_returns_error():
    payload = {
        "type": "undefined_plot_type",
        "data": {}
    }
    response = client.post("/visualization", json=payload)
    assert response.status_code in [400, 422]

