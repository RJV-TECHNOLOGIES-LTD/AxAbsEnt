# benchmarks/__init__.py

"""
AxAbsEnt Benchmarking Suite

Initializes the benchmark framework for evaluating the performance of all core modules
of the AxAbsEnt system including:

- Core interaction computations
- Transfinite recursive chains
- Force extraction and emergence
- Simulation engines (classical, quantum, cosmological)
- Visualization pipelines (2D, 3D, entropy mapping)
- GPU acceleration and CUDA kernels
- Parallel and distributed execution

All benchmarks conform to reproducible testing standards and are structured to isolate
performance-critical paths for scientific optimization.

This module provides central access to the benchmarking orchestrator.
"""

import time
import functools
import logging
import platform
import psutil
import numpy as np

logger = logging.getLogger("axabsent.benchmark")
logging.basicConfig(level=logging.INFO)


def benchmark(func):
    """
    Decorator to measure the execution time and memory footprint of a function.
    Logs results to the AxAbsEnt benchmarking interface.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        mem_before = process.memory_info().rss
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        mem_after = process.memory_info().rss
        duration = end_time - start_time
        mem_used = (mem_after - mem_before) / 1024**2

        logger.info(f"[{func.__name__}] Time: {duration:.6f}s | Mem: {mem_used:.3f} MB")
        return result

    return wrapper


def system_info():
    """
    Returns a dictionary with current system benchmarking context:
    CPU, RAM, OS, Python version, and active CUDA device (if available).
    """
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        cuda_device = torch.cuda.get_device_name(0) if cuda_available else "None"
    except ImportError:
        cuda_available = False
        cuda_device = "Unavailable"

    return {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(logical=True),
        "total_ram_gb": round(psutil.virtual_memory().total / 1024**3, 2),
        "python_version": platform.python_version(),
        "cuda_enabled": cuda_available,
        "cuda_device": cuda_device
    }


def print_system_info():
    """
    Logs system info to benchmark logger.
    """
    info = system_info()
    logger.info("System Benchmark Context:")
    for key, val in info.items():
        logger.info(f"  {key}: {val}")
