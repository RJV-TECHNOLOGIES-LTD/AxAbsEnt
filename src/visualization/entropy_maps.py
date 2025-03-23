# src/visualization/entropy_maps.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional
from .base import BaseVisualization

class EntropyMapsVisualization(BaseVisualization):
    """
    Visualizes entropy maps by rendering a heatmap from a 2D entropy matrix.
    
    The entropy map highlights the spatial variation of entropy values, which can be
    derived from simulation outputs, force field measurements, or entropy computations.
    """
    
    def __init__(self, entropy_matrix: Optional[np.ndarray] = None, title: Optional[str] = "Entropy Map"):
        super().__init__(title)
        self.entropy_matrix = entropy_matrix

    def generate_plot(self, cmap: str = "inferno") -> None:
        """
        Generates a heatmap of the entropy matrix.
        
        Parameters:
            cmap (str): The colormap to be used for the heatmap (default is "inferno").
        """
        if self.entropy_matrix is None:
            raise ValueError("Entropy matrix is not provided for visualization.")
        
        self.setup_plot(figsize=(8, 6))
        cax = self.ax.imshow(self.entropy_matrix, cmap=cmap, origin="lower")
        self.figure.colorbar(cax, ax=self.ax)
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Dimension 1")
        self.ax.set_ylabel("Dimension 2")
    
    def update_entropy_matrix(self, new_matrix: np.ndarray) -> None:
        """
        Updates the current entropy matrix with a new one.
        
        Parameters:
            new_matrix (np.ndarray): A new 2D array representing the entropy distribution.
        """
        self.entropy_matrix = new_matrix

    def __repr__(self) -> str:
        matrix_shape = self.entropy_matrix.shape if self.entropy_matrix is not None else "None"
        return f"<EntropyMapsVisualization title='{self.title}' matrix_shape={matrix_shape}>"
