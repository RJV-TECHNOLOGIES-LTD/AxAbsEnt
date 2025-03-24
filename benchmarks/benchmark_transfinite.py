# benchmarks/benchmark_transfinite.py

"""
Benchmark: Transfinite Interaction Chains & Symmetry Decay

Evaluates recursive ordinal projections, Symmetry Decay Index (SDI)
evolution, and tensor propagation across layered transfinite chains.

Includes:

- Ordinal projection complexity
- Symmetry Decay Index stabilization steps
- Entropy-core trace decay across recursion depth
"""

import numpy as np
from benchmarks import benchmark, print_system_info


# ----------------------------
# Transfinite Chain Simulation
# ----------------------------

def simulate_transfinite_chain(depth=64, dim=128):
    """
    Constructs a transfinite chain of tensors, projecting ordinal states
    and aggregating entropy-core decay as per the SDI model.
    """
    sdi_tensor = np.eye(dim)
    decay_trace = []

    for i in range(1, depth + 1):
        ordinal_factor = i / (i + 1)
        projection = ordinal_factor * np.random.rand(dim, dim)
        sdi_tensor = sdi_tensor @ projection
        trace = np.trace(sdi_tensor @ sdi_tensor.T)
        decay_trace.append(trace)

    return decay_trace[-1]


@benchmark
def benchmark_transfinite_chain(iterations=32):
    return np.mean([simulate_transfinite_chain() for _ in range(iterations)])


# ----------------------------
# SDI Evolution Stability
# ----------------------------

def simulate_sdi_stabilization(depth=100, dim=64, threshold=1e-3):
    """
    Simulates SDI stabilization by computing the point at which the trace
    variation falls below threshold. This reflects topological stabilization
    of cross-absolute recursion.
    """
    sdi = np.eye(dim)
    prev_trace = None
    stabilization_step = depth

    for i in range(1, depth + 1):
        decay = (1 / i) * np.random.rand(dim, dim)
        sdi = sdi @ decay
        current_trace = np.trace(sdi @ sdi.T)
        if prev_trace is not None:
            if abs(current_trace - prev_trace) < threshold:
                stabilization_step = i
                break
        prev_trace = current_trace

    return stabilization_step


@benchmark
def benchmark_sdi_stabilization(trials=50):
    return np.mean([simulate_sdi_stabilization() for _ in range(trials)])


# ----------------------------
# Ordinal Collapse Projection
# ----------------------------

def simulate_ordinal_projection(depth=50, dim=32):
    """
    Propagates ordinal-indexed projections downward, mimicking topological
    collapse in curvature-tensor recursion.
    """
    accumulator = np.eye(dim)
    for i in range(1, depth + 1):
        rank = np.random.rand(dim, dim)
        decay = 1 / (i**2)
        accumulator += decay * rank
    return np.linalg.norm(accumulator)


@benchmark
def benchmark_ordinal_projection(repeats=40):
    return np.mean([simulate_ordinal_projection() for _ in range(repeats)])
    

# ----------------------------
# Benchmark Runner
# ----------------------------

def run_transfinite_benchmarks():
    print_system_info()

    print("\n--- Running Transfinite Chain Benchmark ---")
    transfinite_result = benchmark_transfinite_chain()

    print("\n--- Running SDI Stabilization Benchmark ---")
    sdi_result = benchmark_sdi_stabilization()

    print("\n--- Running Ordinal Collapse Projection Benchmark ---")
    ordinal_result = benchmark_ordinal_projection()

    print("\n--- Transfinite Benchmark Results ---")
    print(f"Final SDI Trace (Depth Limit): {transfinite_result:.4f}")
    print(f"SDI Stabilization Step: {sdi_result:.2f}")
    print(f"Ordinal Collapse Tensor Norm: {ordinal_result:.4f}")


if __name__ == "__main__":
    run_transfinite_benchmarks()
