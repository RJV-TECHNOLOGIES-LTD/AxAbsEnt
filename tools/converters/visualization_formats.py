# tools/converters/visualization_formats.py

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, Union
import json


class VisualizationFormatConverter:
    """
    Converts structured simulation or interaction data into formats suitable for
    AxAbsEnt visualization modules (force maps, entropy fields, interaction graphs, resonance plots).
    """

    def __init__(self):
        pass

    def tensor_to_dataframe(self, tensor: np.ndarray, axis_labels: Optional[Tuple[str, ...]] = None) -> pd.DataFrame:
        """
        Converts a 2D or 3D tensor into a flat DataFrame for plotting and graph generation.

        Parameters:
        - tensor: np.ndarray
        - axis_labels: Optional axis names, e.g. ("x", "y", "value")
        """
        tensor = np.nan_to_num(tensor)

        if tensor.ndim == 2:
            df = pd.DataFrame(tensor)
            if axis_labels and len(axis_labels) == 2:
                df.columns = [f"{axis_labels[1]}_{i}" for i in range(tensor.shape[1])]
                df[axis_labels[0]] = np.arange(tensor.shape[0])
        elif tensor.ndim == 3:
            x, y, z = tensor.shape
            flat = tensor.reshape((x * y, z))
            df = pd.DataFrame(flat)
            if axis_labels and len(axis_labels) == 3:
                df.columns = [f"{axis_labels[2]}_{i}" for i in range(z)]
                df[axis_labels[0]] = np.repeat(np.arange(x), y)
                df[axis_labels[1]] = np.tile(np.arange(y), x)
        else:
            raise ValueError("Only 2D or 3D tensors can be visualized using this converter.")

        return df

    def encode_interaction_graph(self, interaction_tensor: np.ndarray) -> Dict[str, Any]:
        """
        Converts an interaction tensor into a node-edge JSON format for force-directed graph plotting.

        Assumes interaction_tensor is square and symmetric: shape (N, N).
        """
        self._validate_square_tensor(interaction_tensor)
        num_nodes = interaction_tensor.shape[0]
        nodes = [{"id": i, "label": f"Abs{i}"} for i in range(num_nodes)]
        edges = []

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                weight = interaction_tensor[i, j]
                if weight != 0:
                    edges.append({"source": i, "target": j, "weight": float(weight)})

        return {"nodes": nodes, "edges": edges}

    def prepare_field_map(self, field_tensor: np.ndarray, normalize: bool = True) -> np.ndarray:
        """
        Prepares a 2D field (e.g. entropy, force magnitude, curvature) for heatmap rendering.

        - Normalizes values between 0 and 1 if requested.
        - Assumes input is 2D.
        """
        if field_tensor.ndim != 2:
            raise ValueError("Field tensor must be 2D for visualization.")
        tensor = np.nan_to_num(field_tensor)
        if normalize:
            min_val = np.min(tensor)
            max_val = np.max(tensor)
            tensor = (tensor - min_val) / (max_val - min_val + 1e-12)
        return tensor

    def export_plot_data(self, df: pd.DataFrame, output_path: str):
        """
        Exports a DataFrame as a JSON file for use in frontend plotting engines.
        """
        df.to_json(output_path, orient="records", indent=2)

    def export_graph_json(self, graph_dict: Dict[str, Any], output_path: str):
        """
        Exports an interaction graph dictionary to a JSON file.
        """
        with open(output_path, "w") as f:
            json.dump(graph_dict, f, indent=2)

    def _validate_square_tensor(self, tensor: np.ndarray):
        if tensor.ndim != 2:
            raise ValueError("Tensor must be 2D for graph encoding.")
        if tensor.shape[0] != tensor.shape[1]:
            raise ValueError("Tensor must be square (NxN) for interaction graph encoding.")
