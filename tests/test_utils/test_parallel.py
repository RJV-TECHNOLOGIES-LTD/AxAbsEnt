"""
AxAbsEnt Parallelization Utility Tests

This suite validates the mathematical and epistemological integrity of AxAbsEnt's
parallel computation layer. The functions under test support:

- Process-based and thread-based parallelism
- Deterministic, fault-tolerant distributed task mapping
- Computational acceleration for interaction chains and entropic simulation

Tests follow the doctrinal standards of transfinite execution, recursion integrity,
and total information-preserving task propagation.
"""

import pytest
import time
from typing import List

from axabsent.utils.parallel import (
    parallel_map,
    threaded_map,
    distribute_tasks
)


# ------------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------------

def _square(x: int) -> int:
    """Return x squared."""
    return x * x


def _simulate_delay(x: int) -> int:
    """Artificial delay function to simulate workload."""
    time.sleep(0.01)
    return x + 100


# ------------------------------------------------------------------------------------
# Core Functional Tests
# ------------------------------------------------------------------------------------

@pytest.mark.utils
def test_parallel_map_correctness_and_order():
    """
    Verify parallel_map preserves element-wise results and output ordering.

    Theoretical Context:
    Preserves determinism under absolute parallel isolation (Orthogonality O(Aᵢ, Aⱼ) ≠ 1).
    Complexity: O(n)
    """
    data: List[int] = list(range(10))
    expected = [_square(x) for x in data]

    result = parallel_map(_square, data, workers=4)

    assert result == expected


@pytest.mark.utils
def test_threaded_map_correctness():
    """
    Validate threaded_map produces correct results under concurrency constraints.

    Theoretical Context:
    Used for non-isolated memory-side propagation (intra-mediator chain resolution).
    Complexity: O(n) with thread contention
    """
    data = list(range(10))
    expected = [_square(x) for x in data]

    result = threaded_map(_square, data, workers=4)

    assert result == expected


@pytest.mark.utils
def test_parallel_execution_outperforms_sequential():
    """
    Confirm parallel_map provides measurable speedup over sequential execution.

    Theoretical Context:
    Reflects the Φ-optimized entropic acceleration path in emergent chain execution.
    Complexity: O(n) vs. O(n / p) with overhead
    """
    dataset = list(range(20))

    t_seq_start = time.time()
    seq_result = [_simulate_delay(x) for x in dataset]
    t_seq_end = time.time()

    t_par_start = time.time()
    par_result = parallel_map(_simulate_delay, dataset, workers=4)
    t_par_end = time.time()

    assert par_result == seq_result
    assert (t_par_end - t_par_start) < (t_seq_end - t_seq_start)


# ------------------------------------------------------------------------------------
# Backend-Oriented Validation
# ------------------------------------------------------------------------------------

@pytest.mark.utils
def test_distribute_tasks_process_backend():
    """
    Distribute tasks using 'process' backend and verify propagation success.

    Theoretical Context:
    Models orthogonal interaction chain forked by isolation tensor groups.
    """
    tasks = list(range(8))
    result = distribute_tasks(tasks, worker_fn=_square, backend="process")

    assert result == [_square(x) for x in tasks]


@pytest.mark.utils
def test_distribute_tasks_thread_backend():
    """
    Distribute tasks using 'thread' backend and verify correctness.

    Theoretical Context:
    Reflects topological tensor spread under coherent mediator interpolation.
    """
    tasks = list(range(5))
    result = distribute_tasks(tasks, worker_fn=_simulate_delay, backend="thread")

    assert result == [_simulate_delay(x) for x in tasks]


@pytest.mark.utils
def test_distribute_tasks_invalid_backend_raises():
    """
    Ensure backend validation protects against unsupported execution models.

    Theoretical Context:
    Fault prevention mechanism reflecting Selection Principle boundary violation.
    """
    with pytest.raises(ValueError):
        distribute_tasks([1, 2, 3], worker_fn=_square, backend="quantum-dreamstream")
