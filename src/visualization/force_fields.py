# src/visualization/force_fields.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional
from .base import BaseVisualization

class ForceFieldsVisualization(BaseVisualization):
    """
    Visualizes force field tensors as heatmaps or vector fields.
    
    Attributes:
        field_tensor (np.ndarray): A 2D array representing the computed force field.
        title (str): The title for the plot.
    """
    
    def __init__(self, field_tensor: Optional[np.ndarray] = None, title: Optional[str] = "Force Field Visualization"):
        super().__init__(title)
        self.field_tensor = field_tensor

    def generate_plot(self, mode: str = "heatmap") -> None:
        """
        Generates a plot of the force field tensor.
        
        Parameters:
            mode (str): The visualization mode. Options:
                        - "heatmap": Displays the tensor as a color-coded heatmap.
                        - "vector": Interprets the gradient of the tensor as a vector field.
        """
        if self.field_tensor is None:
            raise ValueError("Field tensor is not provided for visualization.")
        
        self.setup_plot(figsize=(8, 6))
        
        if mode == "heatmap":
            cax = self.ax.imshow(self.field_tensor, cmap="viridis", origin="lower")
            self.figure.colorbar(cax, ax=self.ax)
        elif mode == "vector":
            # Compute gradients to simulate a vector field representation.
            grad_y, grad_x = np.gradient(self.field_tensor)
            X, Y = np.meshgrid(np.arange(self.field_tensor.shape[1]), np.arange(self.field_tensor.shape[0]))
            self.ax.quiver(X, Y, grad_x, grad_y, scale=1, scale_units='inches', angles='xy')
        else:
            raise ValueError("Unsupported mode. Choose 'heatmap' or 'vector'.")
        
        self.ax.set_title(self.title)

    def update_field_tensor(self, new_tensor: np.ndarray) -> None:
        """
        Updates the current force field tensor to a new tensor.
        
        Parameters:
            new_tensor (np.ndarray): The new force field tensor for visualization.
        """
        self.field_tensor = new_tensor

    def __repr__(self) -> str:
        tensor_shape = self.field_tensor.shape if self.field_tensor is not None else "None"
        return f"<ForceFieldsVisualization title='{self.title}' tensor_shape={tensor_shape}>"
