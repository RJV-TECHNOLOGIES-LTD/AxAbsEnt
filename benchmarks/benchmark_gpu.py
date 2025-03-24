# benchmarks/benchmark_gpu.py

"""
Benchmark: GPU Tensor Acceleration

This module evaluates GPU performance for critical AxAbsEnt tensor operations:

- Matrix-matrix multiplications for entropy-core projection
- Tensor decomposition and normalizations
- Cross-absolute coupling trace evaluations

Benchmarks are compared across CPU (NumPy), GPU (Torch CUDA), and
optionally native CUDA kernel backends (to be linked with CUDA module).
"""

import time
import numpy as np
from benchmarks import benchmark, print_system_info

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# ----------------------------
# CPU BASELINE
# ----------------------------

@benchmark
def benchmark_entropy_core_cpu(size=2048):
    A = np.random.rand(size, size)
    core = A @ A.T
    trace = np.trace(core)
    return trace


# ----------------------------
# GPU ACCELERATION (TORCH)
# ----------------------------

@benchmark
def benchmark_entropy_core_gpu(size=2048):
    if not TORCH_AVAILABLE:
        raise RuntimeError("PyTorch not installed. Run `pip install torch`")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    A = torch.rand((size, size), device=device)
    core = torch.matmul(A, A.T)
    trace = torch.trace(core)
    return trace.item()


# ----------------------------
# GPU MEMORY BANDWIDTH TEST
# ----------------------------

@benchmark
def benchmark_gpu_memory_transfer(size=4096):
    if not TORCH_AVAILABLE:
        raise RuntimeError("Torch not available.")

    cpu_data = torch.rand((size, size))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    t0 = time.perf_counter()
    gpu_data = cpu_data.to(device)
    t1 = time.perf_counter()
    duration = t1 - t0
    return gpu_data.numel(), duration


# ----------------------------
# Benchmark Runner
# ----------------------------

def run_gpu_benchmarks():
    print_system_info()

    print("\n--- Running CPU Entropy-Core Benchmark ---")
    cpu_trace = benchmark_entropy_core_cpu()

    if TORCH_AVAILABLE and torch.cuda.is_available():
        print("\n--- Running GPU Entropy-Core Benchmark ---")
        gpu_trace = benchmark_entropy_core_gpu()

        print("\n--- Running GPU Memory Transfer Benchmark ---")
        mem_transfer, mem_time = benchmark_gpu_memory_transfer()
    else:
        gpu_trace = "Unavailable"
        mem_transfer = mem_time = "N/A"

    print("\n--- GPU Benchmark Results ---")
    print(f"CPU Trace Result: {cpu_trace}")
    print(f"GPU Trace Result: {gpu_trace}")
    print(f"GPU Memory Transfer: {mem_transfer} elements in {mem_time} seconds")


if __name__ == "__main__":
    run_gpu_benchmarks()
