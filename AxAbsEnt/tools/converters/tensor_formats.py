# tools/converters/tensor_formats.py

import numpy as np
from typing import Union, Tuple, Dict, Any


class TensorFormatError(Exception):
    """Raised when a tensor does not comply with AxAbsEnt structural requirements."""
    pass


class TensorFormatConverter:
    """
    Core tensor formatting, validation, and transformation utilities for AxAbsEnt.
    Ensures compliance with shape, dtype, and interaction compatibility across simulation and ontology.
    """

    def __init__(self):
        pass

    def validate_tensor(self, tensor: np.ndarray, rank: int = 2, allow_singular: bool = False) -> None:
        """
        Validates that a tensor conforms to expected dimensional rank and shape.

        Parameters:
        - tensor: np.ndarray
        - rank: expected dimensional rank (e.g., 2 for matrices, 3 for field tensors)
        - allow_singular: whether to permit 1-element tensors as degenerate cases
        """
        if not isinstance(tensor, np.ndarray):
            raise TensorFormatError("Input is not a NumPy array.")

        if tensor.ndim != rank:
            if allow_singular and tensor.size == 1:
                return
            raise TensorFormatError(f"Tensor must be {rank}D; got shape {tensor.shape}")

        if np.isnan(tensor).any() or np.isinf(tensor).any():
            raise TensorFormatError("Tensor contains invalid (NaN or Inf) values.")

    def enforce_dtype(self, tensor: np.ndarray, dtype: Union[str, np.dtype] = np.float64) -> np.ndarray:
        """
        Converts tensor to a specific data type (default: float64).
        """
        return tensor.astype(dtype)

    def flatten_tensor(self, tensor: np.ndarray) -> np.ndarray:
        """
        Flattens any tensor to a 1D array. Used for entropy metrics or action scalars.
        """
        return tensor.flatten()

    def reshape_tensor(self, tensor: np.ndarray, target_shape: Tuple[int, ...]) -> np.ndarray:
        """
        Reshapes tensor to a new shape with strict element count preservation.
        """
        if np.prod(tensor.shape) != np.prod(target_shape):
            raise TensorFormatError(f"Cannot reshape {tensor.shape} to {target_shape}: size mismatch.")
        return tensor.reshape(target_shape)

    def normalize_tensor(self, tensor: np.ndarray, axis: int = None) -> np.ndarray:
        """
        Normalize tensor values between 0 and 1 across the entire tensor or along a given axis.
        """
        tensor = np.nan_to_num(tensor)
        if axis is None:
            min_val = np.min(tensor)
            max_val = np.max(tensor)
            return (tensor - min_val) / (max_val - min_val + 1e-12)
        else:
            min_val = np.min(tensor, axis=axis, keepdims=True)
            max_val = np.max(tensor, axis=axis, keepdims=True)
            return (tensor - min_val) / (max_val - min_val + 1e-12)

    def generate_identity_tensor(self, size: int) -> np.ndarray:
        """
        Generates a square identity matrix tensor — used as default signature of irreducible absolutes.
        """
        return np.eye(size)

    def to_dict(self, tensor: np.ndarray) -> Dict[str, Any]:
        """
        Converts tensor to a dictionary representation for JSON serialization.
        """
        return {
            "shape": tensor.shape,
            "dtype": str(tensor.dtype),
            "data": tensor.tolist()
        }

    def from_dict(self, obj: Dict[str, Any]) -> np.ndarray:
        """
        Converts dictionary-formatted tensor back into NumPy array.
        """
        return np.array(obj["data"], dtype=obj.get("dtype", "float64")).reshape(obj["shape"])
