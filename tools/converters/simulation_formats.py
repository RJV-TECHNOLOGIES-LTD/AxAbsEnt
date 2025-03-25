# tools/converters/simulation_formats.py

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union


class SimulationFormatConverter:
    """
    Converts raw simulation outputs to AxAbsEnt-standardized tensor formats
    with traceable structure for downstream visualization, validation, and resonance detection.
    Supports merging across distributed or parallel simulation outputs.
    """

    SUPPORTED_FORMATS = ["json", "csv", "npy", "npz"]

    def __init__(self, sim_dir: str):
        self.sim_dir = os.path.abspath(sim_dir)
        if not os.path.exists(self.sim_dir):
            raise FileNotFoundError(f"Simulation directory not found: {self.sim_dir}")

    def load(self, filename: str) -> Dict[str, Any]:
        """Loads simulation result into structured AxAbsEnt tensor form."""
        path = os.path.join(self.sim_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        ext = filename.split(".")[-1].lower()

        if ext == "json":
            return self._load_json(path)
        elif ext == "csv":
            return self._load_csv(path)
        elif ext == "npy":
            return self._load_npy(path)
        elif ext == "npz":
            return self._load_npz(path)
        else:
            raise ValueError(f"Unsupported simulation format: {ext}")

    def _load_json(self, path: str) -> Dict[str, Any]:
        with open(path, 'r') as f:
            data = json.load(f)
        tensor = np.array(data.get("tensor", []))
        metadata = data.get("metadata", {})
        return {
            "tensor": tensor,
            "metadata": {"source": path, "format": "json", **metadata}
        }

    def _load_csv(self, path: str) -> Dict[str, Any]:
        df = pd.read_csv(path)
        return {
            "tensor": df.values,
            "columns": list(df.columns),
            "metadata": {"source": path, "format": "csv"}
        }

    def _load_npy(self, path: str) -> Dict[str, Any]:
        tensor = np.load(path)
        return {
            "tensor": tensor,
            "metadata": {"source": path, "format": "npy"}
        }

    def _load_npz(self, path: str) -> Dict[str, Any]:
        loaded = np.load(path)
        tensors = {key: loaded[key] for key in loaded.files}
        return {
            "tensor": tensors,
            "metadata": {"source": path, "format": "npz", "keys": list(tensors.keys())}
        }

    def merge_distributed_outputs(self, outputs: Dict[str, np.ndarray], axis: int = 0) -> np.ndarray:
        """
        Merges multiple tensor outputs from parallel or distributed simulations.
        Assumes consistent shape except for merge axis.
        """
        arrays = [np.atleast_2d(arr) for arr in outputs.values()]
        return np.concatenate(arrays, axis=axis)

    def normalize_tensor(self, tensor: np.ndarray, method: str = "minmax") -> np.ndarray:
        """
        Normalize tensor for downstream resonance analysis or entropy validation.
        Supports 'minmax' or 'zscore'.
        """
        if method == "minmax":
            min_val = np.min(tensor)
            max_val = np.max(tensor)
            return (tensor - min_val) / (max_val - min_val + 1e-12)
        elif method == "zscore":
            mean = np.mean(tensor)
            std = np.std(tensor) + 1e-12
            return (tensor - mean) / std
        else:
            raise ValueError(f"Unknown normalization method: {method}")

    def export_as_npz(self, data: Dict[str, Any], out_path: Optional[str] = None):
        """Save tensor or multiple arrays in compressed `.npz` format."""
        if out_path is None:
            out_path = os.path.join(self.sim_dir, "converted_simulation.npz")
        tensors = data.get("tensor")
        if isinstance(tensors, dict):
            np.savez_compressed(out_path, **tensors)
        elif isinstance(tensors, np.ndarray):
            np.savez_compressed(out_path, tensor=tensors)
        else:
            raise TypeError("Unsupported tensor type for export.")
        return out_path
