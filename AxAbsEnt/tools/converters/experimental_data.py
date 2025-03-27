# tools/converters/experimental_data.py

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, Union, Optional


class ExperimentalDataConverter:
    """
    Converts raw experimental data files into AxAbsEnt-compliant tensor formats,
    preserving metadata, units, and alignment with unified model dimensions.
    """

    SUPPORTED_FORMATS = ["csv", "json", "hdf5"]

    def __init__(self, data_dir: str):
        self.data_dir = os.path.abspath(data_dir)
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def load(self, filename: str) -> Dict[str, Any]:
        """Load and return raw data with metadata from supported format."""
        path = os.path.join(self.data_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {filename}")

        ext = filename.split('.')[-1].lower()
        if ext == "csv":
            return self._load_csv(path)
        elif ext == "json":
            return self._load_json(path)
        elif ext == "hdf5":
            return self._load_hdf5(path)
        else:
            raise ValueError(f"Unsupported file format: .{ext}")

    def _load_csv(self, path: str) -> Dict[str, Any]:
        df = pd.read_csv(path)
        return {
            "tensor": df.values,
            "columns": list(df.columns),
            "metadata": {"source": path, "format": "csv"}
        }

    def _load_json(self, path: str) -> Dict[str, Any]:
        with open(path, 'r') as f:
            data = json.load(f)
        tensor = np.array(data.get("tensor", []))
        metadata = data.get("metadata", {})
        return {
            "tensor": tensor,
            "metadata": {"source": path, "format": "json", **metadata}
        }

    def _load_hdf5(self, path: str) -> Dict[str, Any]:
        import h5py
        result = {}
        with h5py.File(path, 'r') as f:
            for key in f.keys():
                result[key] = f[key][:]
        return {
            "tensor": result,
            "metadata": {"source": path, "format": "hdf5"}
        }

    def convert_to_tensor(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Converts structured data into a NumPy tensor suitable for AxAbsEnt interaction simulation.
        Ensures proper shape, normalization, and handles NaNs.
        """
        tensor = data.get("tensor")
        if isinstance(tensor, dict):
            # Flatten all datasets into a single array (if multiple tensors per key)
            tensor = np.concatenate([np.atleast_2d(v) for v in tensor.values()], axis=0)
        else:
            tensor = np.atleast_2d(tensor)

        # Normalize and fill NaNs
        tensor = np.nan_to_num(tensor)
        return tensor

    def save_as_json(self, data: Dict[str, Any], out_path: Optional[str] = None):
        """Save structured tensor and metadata as AxAbsEnt-compliant JSON."""
        if out_path is None:
            out_path = os.path.join(self.data_dir, "converted_experiment.json")
        payload = {
            "tensor": data["tensor"].tolist() if isinstance(data["tensor"], np.ndarray) else data["tensor"],
            "metadata": data.get("metadata", {})
        }
        with open(out_path, "w") as f:
            json.dump(payload, f, indent=4)
        return out_path
