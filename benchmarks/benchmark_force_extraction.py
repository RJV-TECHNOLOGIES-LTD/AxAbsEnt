# benchmarks/benchmark_force_extraction.py

"""
Benchmark: Force Extraction Algorithms

Measures the performance of gravitational, electromagnetic, strong, and weak
force extraction computations from interaction tensors and selection entropy
across a large set of absolute entities.

This includes:

- Signature projection & entropy-core mapping
- Coupling constant synthesis
- Force vector reconstruction latency
- Optional GPU acceleration (torch)
"""

import numpy as np
import time
from benchmarks import benchmark, print_system_info

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ----------------------------
# Dummy Force Extraction Kernel
# ----------------------------

def simulate_force_extraction(interaction_tensor: np.ndarray) -> np.ndarray:
    """
    Simulates the force extraction operation over interaction space.
    This approximates coupling strength via entropy-core trace and
    reconstructs synthetic force vectors.
    """
    entropy_core = interaction_tensor @ interaction_tensor.T
    coupling_strength = np.trace(entropy_core)
    normalized = entropy_core / (np.linalg.norm(entropy_core) + 1e-10)
    return coupling_strength * normalized.mean(axis=0)


@benchmark
def benchmark_force_extraction_cpu(matrix_size=1024, iterations=10):
    results = []
    for _ in range(iterations):
        interaction_tensor = np.random.rand(matrix_size, matrix_size)
        result = simulate_force_extraction(interaction_tensor)
        results.append(result.sum())
    return sum(results)


# ----------------------------
# Optional: Torch GPU Benchmark
# ----------------------------

@benchmark
def benchmark_force_extraction_gpu(matrix_size=1024, iterations=10):
    if not TORCH_AVAILABLE:
        raise RuntimeError("Torch not installed. Run `pip install torch`.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    total_result = 0.0

    for _ in range(iterations):
        tensor = torch.rand((matrix_size, matrix_size), device=device)
        entropy_core = torch.matmul(tensor, tensor.T)
        coupling = torch.trace(entropy_core)
        normalized = entropy_core / (torch.norm(entropy_core) + 1e-10)
        total_result += (coupling * normalized.mean(dim=0)).sum().item()

    return total_result


# ----------------------------
# Benchmark Runner
# ----------------------------

def run_force_extraction_benchmarks():
    print_system_info()

    print("\n--- Running CPU Force Extraction Benchmark ---")
    cpu_result = benchmark_force_extraction_cpu()

    if TORCH_AVAILABLE and torch.cuda.is_available():
        print("\n--- Running GPU Force Extraction Benchmark ---")
        gpu_result = benchmark_force_extraction_gpu()
    else:
        gpu_result = "Torch/CUDA not available."

    print("\n--- Force Extraction Benchmark Results ---")
    print(f"CPU Aggregate Output: {cpu_result}")
    print(f"GPU Aggregate Output: {gpu_result}")


if __name__ == "__main__":
    run_force_extraction_benchmarks()
