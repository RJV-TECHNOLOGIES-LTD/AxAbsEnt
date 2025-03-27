# benchmarks/benchmark_interaction.py

"""
Benchmark: Cross-Absolute Interaction Composition

Measures performance of pairwise and compositional interaction operators
across large sets of Absolute Entities.

Tests include:

- Pairwise interaction tensor construction
- Composition chaining (mediator propagation)
- Entropy-core stability under recursive interaction depth
- Action minimization across transfinite threads
"""

import numpy as np
from benchmarks import benchmark, print_system_info


# ----------------------------
# Simulated Interaction Logic
# ----------------------------

def construct_interaction_tensor(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Constructs a simulated interaction tensor between two absolute signatures.
    Emulates entropy propagation via outer-product composite.
    """
    return np.outer(A, B) + np.outer(B, A)


def compose_interactions_chain(entities: list) -> np.ndarray:
    """
    Recursively composes interaction tensors through transfinite link chaining.
    """
    composed = np.zeros((entities[0].size, entities[0].size))
    for i in range(len(entities) - 1):
        interaction = construct_interaction_tensor(entities[i], entities[i + 1])
        composed += interaction
    return composed


# ----------------------------
# Benchmark 1: Pairwise Composition
# ----------------------------

@benchmark
def benchmark_pairwise_interaction(dimension=512):
    A = np.random.rand(dimension)
    B = np.random.rand(dimension)
    interaction_tensor = construct_interaction_tensor(A, B)
    return np.trace(interaction_tensor)


# ----------------------------
# Benchmark 2: Transfinite Chain Composition
# ----------------------------

@benchmark
def benchmark_compositional_chain(dimension=256, chain_length=128):
    entities = [np.random.rand(dimension) for _ in range(chain_length)]
    composite_tensor = compose_interactions_chain(entities)
    return np.linalg.norm(composite_tensor)


# ----------------------------
# Benchmark 3: Action Minimization Trace
# ----------------------------

@benchmark
def benchmark_minimal_action_projection(dimension=384):
    signature = np.random.rand(dimension, dimension)
    entropy_core = signature @ signature.T
    selection_tensor = entropy_core / (np.linalg.norm(entropy_core) + 1e-9)
    minimal_action = np.trace(selection_tensor)
    return minimal_action


# ----------------------------
# Benchmark Runner
# ----------------------------

def run_interaction_benchmarks():
    print_system_info()

    print("\n--- Running Pairwise Interaction Benchmark ---")
    pairwise_result = benchmark_pairwise_interaction()

    print("\n--- Running Compositional Chain Benchmark ---")
    chain_result = benchmark_compositional_chain()

    print("\n--- Running Minimal Action Trace Benchmark ---")
    action_result = benchmark_minimal_action_projection()

    print("\n--- Interaction Benchmark Results ---")
    print(f"Pairwise Trace: {pairwise_result}")
    print(f"Chain Norm: {chain_result}")
    print(f"Selection Trace: {action_result}")


if __name__ == "__main__":
    run_interaction_benchmarks()
