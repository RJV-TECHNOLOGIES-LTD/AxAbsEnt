import pytest
import numpy as np
import torch  # Assuming PyTorch or similar for device check
from cuda_bindings import force_extraction, simulation, tensor_ops

@pytest.mark.cuda
def test_cuda_available():
    """
    Check that CUDA is available and at least one device is detected.
    """
    assert torch.cuda.is_available(), "CUDA is not available on this system"
    assert torch.cuda.device_count() >= 1

@pytest.mark.cuda
def test_cuda_tensor_operation():
    """
    Tests CUDA-accelerated tensor dot product.
    Verifies shape and value constraints.
    """
    a = np.random.rand(64, 128).astype(np.float32)
    b = np.random.rand(128, 64).astype(np.float32)

    result = tensor_ops.cuda_tensor_dot(a, b)
    assert isinstance(result, np.ndarray)
    assert result.shape == (64, 64)
    assert np.all(result >= 0)  # Should not contain garbage values

@pytest.mark.cuda
def test_cuda_force_extraction_consistency():
    """
    Runs GPU-based force extraction and checks output validity.
    """
    sample_interaction_tensor = np.random.rand(256, 256).astype(np.float32)

    extracted = force_extraction.extract_cuda_forces(sample_interaction_tensor)
    assert isinstance(extracted, dict)
    assert "gravity" in extracted
    assert isinstance(extracted["gravity"], np.ndarray)
    assert extracted["gravity"].shape == (4, 4)

@pytest.mark.cuda
def test_cuda_simulation_pipeline():
    """
    End-to-end test of CUDA simulation pipeline.
    Checks for successful completion and structural validity of output.
    """
    config = {
        "mode": "quantum_field",
        "grid_size": 128,
        "timesteps": 50
    }

    output = simulation.run_cuda_simulation(config)

    assert isinstance(output, dict)
    assert "field_values" in output
    assert isinstance(output["field_values"], np.ndarray)
    assert output["field_values"].shape == (50, 128, 128)
    assert np.all(np.isfinite(output["field_values"]))

