# benchmarks/benchmark_simulation.py

"""
Benchmark: AxAbsEnt Simulation Engines

Measures simulation performance for:

1. Dynamic evolution of absolute entity systems (ODE-based propagation).
2. Quantum field simulation over grid spaces (probabilistic amplitudes).
3. Monte Carlo sampling across force emergence topologies.

Includes latency, convergence, and entropy minimization statistics.
"""

import numpy as np
from benchmarks import benchmark, print_system_info


# ----------------------------
# Simulation 1: Dynamic System (ODE-like)
# ----------------------------

def simulate_dynamics(step_count=1000, delta=0.01) -> float:
    """
    Simulates deterministic evolution of a system using
    Newton-like propagation over force constraints.
    """
    x = 0.0
    v = 1.0  # Initial velocity
    for _ in range(step_count):
        a = -0.5 * x  # Simulated force: harmonic potential
        v += a * delta
        x += v * delta
    return x


@benchmark
def benchmark_dynamics_simulation(iterations=1000):
    results = [simulate_dynamics() for _ in range(iterations)]
    return np.mean(results)


# ----------------------------
# Simulation 2: Quantum Field Amplitude Grid
# ----------------------------

def simulate_quantum_field(grid_size=128, steps=50):
    """
    Simulates amplitude propagation over a grid using a simple
    unitary evolution approximation.
    """
    field = np.random.rand(grid_size, grid_size)
    for _ in range(steps):
        laplace = (
            np.roll(field, 1, axis=0)
            + np.roll(field, -1, axis=0)
            + np.roll(field, 1, axis=1)
            + np.roll(field, -1, axis=1)
            - 4 * field
        )
        field += 0.01 * laplace
    return np.sum(field)


@benchmark
def benchmark_quantum_field_simulation(iterations=20):
    return np.mean([simulate_quantum_field() for _ in range(iterations)])


# ----------------------------
# Simulation 3: Monte Carlo Force Chain Sampling
# ----------------------------

def simulate_monte_carlo(chain_length=32, trials=1000):
    """
    Uses Monte Carlo sampling to generate configurations of force interactions,
    selecting ones that minimize entropy-core trace.
    """
    min_trace = float('inf')
    for _ in range(trials):
        chain = [np.random.rand(chain_length) for _ in range(2)]
        tensor = np.outer(chain[0], chain[1]) + np.outer(chain[1], chain[0])
        trace = np.trace(tensor @ tensor.T)
        if trace < min_trace:
            min_trace = trace
    return min_trace


@benchmark
def benchmark_monte_carlo_sampling(runs=16):
    return np.mean([simulate_monte_carlo() for _ in range(runs)])


# ----------------------------
# Benchmark Runner
# ----------------------------

def run_simulation_benchmarks():
    print_system_info()

    print("\n--- Running Dynamics Simulation Benchmark ---")
    dynamics_result = benchmark_dynamics_simulation()

    print("\n--- Running Quantum Field Simulation Benchmark ---")
    qft_result = benchmark_quantum_field_simulation()

    print("\n--- Running Monte Carlo Sampling Benchmark ---")
    mc_result = benchmark_monte_carlo_sampling()

    print("\n--- Simulation Benchmark Results ---")
    print(f"Final Position (Dynamics): {dynamics_result:.6f}")
    print(f"Total Field Amplitude (QFT): {qft_result:.6f}")
    print(f"Minimal Trace (MC Sampling): {mc_result:.6f}")


if __name__ == "__main__":
    run_simulation_benchmarks()
