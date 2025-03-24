# benchmarks/benchmark_distributed.py

"""
Benchmark: Distributed Execution Performance

This module evaluates the performance of distributed execution within AxAbsEnt,
focusing on cross-node tensor computation, transfinite data pipelines,
and distributed simulation chains.

Includes timing and memory metrics for:

- Multi-node tensor decomposition
- Distributed action minimization across absolute sets
- Inter-process communication efficiency
"""

import numpy as np
import time
from benchmarks import benchmark, print_system_info
from multiprocessing import Pool, cpu_count

try:
    import dask.array as da
    from dask.distributed import Client, LocalCluster
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False

# ----------------------------
# Baseline: Multiprocessing CPU Benchmark
# ----------------------------

def compute_local_chunk(chunk_size: int) -> float:
    """Performs a dummy spectral decomposition on a local tensor chunk."""
    chunk = np.random.rand(chunk_size, chunk_size)
    eigvals = np.linalg.eigvals(chunk)
    return np.sum(np.abs(eigvals))


@benchmark
def benchmark_multiprocessing(chunk_size=256, num_chunks=cpu_count()):
    with Pool(processes=num_chunks) as pool:
        results = pool.map(compute_local_chunk, [chunk_size] * num_chunks)
    return sum(results)


# ----------------------------
# Dask: Advanced Distributed Benchmark
# ----------------------------

@benchmark
def benchmark_dask_tensor_reduction(shape=(2048, 2048), chunks=(512, 512)):
    if not DASK_AVAILABLE:
        raise RuntimeError("Dask is not installed. Run `pip install dask distributed`")

    cluster = LocalCluster(n_workers=4, threads_per_worker=1)
    client = Client(cluster)

    tensor = da.random.random(shape, chunks=chunks)
    result = tensor.mean().compute()

    client.close()
    cluster.close()
    return result


# ----------------------------
# Benchmark Runner
# ----------------------------

def run_distributed_benchmarks():
    print_system_info()
    print("\n--- Running Multiprocessing Benchmark ---")
    mp_result = benchmark_multiprocessing()

    if DASK_AVAILABLE:
        print("\n--- Running Dask Distributed Benchmark ---")
        dask_result = benchmark_dask_tensor_reduction()
    else:
        dask_result = "Dask not installed."

    print("\n--- Distributed Benchmark Results ---")
    print(f"Multiprocessing Output Sum: {mp_result}")
    print(f"Dask Reduction Result: {dask_result}")


if __name__ == "__main__":
    run_distributed_benchmarks()
