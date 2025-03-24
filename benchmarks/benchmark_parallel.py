# benchmarks/benchmark_parallel.py

"""
Benchmark: Threaded Parallelism (Local Multi-Core Scaling)

Measures the effect of multi-threaded local execution on AxAbsEnt tensor operations:

- Parallel construction of interaction tensors
- Concurrent force extraction
- Entropy-core trace propagation

Focuses on optimizing local scalability before distributed expansion.
"""

import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from benchmarks import benchmark, print_system_info


# ----------------------------
# Simulated Parallel Tasks
# ----------------------------

def interaction_task(pair_id: int, dim: int) -> float:
    """
    Simulated tensor composition task for interaction between two Absolutes.
    Returns trace of the resulting tensor to simulate selection metric.
    """
    A = np.random.rand(dim)
    B = np.random.rand(dim)
    tensor = np.outer(A, B) + np.outer(B, A)
    return np.trace(tensor)


def force_task(force_id: int, dim: int) -> float:
    """
    Simulated force extraction operation using entropy-core computation.
    """
    sig = np.random.rand(dim, dim)
    entropy_core = sig @ sig.T
    selection_trace = np.trace(entropy_core) / (np.linalg.norm(entropy_core) + 1e-10)
    return selection_trace


# ----------------------------
# Benchmark 1: Parallel Interaction Threads
# ----------------------------

@benchmark
def benchmark_parallel_interactions(n_tasks=64, dim=256, max_workers=8):
    futures = []
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(n_tasks):
            futures.append(executor.submit(interaction_task, i, dim))

        for future in as_completed(futures):
            results.append(future.result())

    return sum(results)


# ----------------------------
# Benchmark 2: Parallel Force Threads
# ----------------------------

@benchmark
def benchmark_parallel_force_extraction(n_tasks=64, dim=256, max_workers=8):
    futures = []
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(n_tasks):
            futures.append(executor.submit(force_task, i, dim))

        for future in as_completed(futures):
            results.append(future.result())

    return np.mean(results)


# ----------------------------
# Benchmark Runner
# ----------------------------

def run_parallel_benchmarks():
    print_system_info()

    print("\n--- Running Parallel Interaction Composition ---")
    interaction_sum = benchmark_parallel_interactions()

    print("\n--- Running Parallel Force Extraction ---")
    force_mean = benchmark_parallel_force_extraction()

    print("\n--- Parallel Benchmark Results ---")
    print(f"Total Parallel Interaction Trace Sum: {interaction_sum}")
    print(f"Mean Parallel Force Trace: {force_mean}")


if __name__ == "__main__":
    run_parallel_benchmarks()
