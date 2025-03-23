# src/visualization/information_flow.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional
from .base import BaseVisualization

class InformationFlowVisualization(BaseVisualization):
    """
    Visualizes the information flow dynamics within the system.
    
    The information flow is provided as a 2D flow matrix representing either
    the magnitude or directionality of information transfer. This class can
    render the flow as either a vector field or using streamlines.
    """
    
    def __init__(self, flow_matrix: Optional[np.ndarray] = None, title: Optional[str] = "Information Flow Visualization"):
        super().__init__(title)
        self.flow_matrix = flow_matrix

    def generate_plot(self, mode: str = "vector") -> None:
        """
        Generates a plot of the information flow.
        
        Parameters:
            mode (str): Visualization mode. Options:
                        - "vector": Uses quiver to display flow vectors.
                        - "stream": Uses streamplot to depict continuous flow lines.
        """
        if self.flow_matrix is None:
            raise ValueError("Flow matrix is not provided for visualization.")
        
        self.setup_plot(figsize=(10, 8))
        
        # Assume flow_matrix is a 2D array where each element represents the magnitude 
        # of information flow; gradients can simulate directionality.
        # For a more sophisticated representation, the flow_matrix might be structured 
        # to include directional components.
        nrows, ncols = self.flow_matrix.shape
        X, Y = np.meshgrid(np.arange(ncols), np.arange(nrows))
        
        # Compute gradients to infer direction (as a simple approximation)
        grad_y, grad_x = np.gradient(self.flow_matrix)
        
        if mode == "vector":
            q = self.ax.quiver(X, Y, grad_x, grad_y, self.flow_matrix, cmap="plasma", scale=50)
            self.figure.colorbar(q, ax=self.ax)
        elif mode == "stream":
            strm = self.ax.streamplot(X, Y, grad_x, grad_y, color=self.flow_matrix, cmap="plasma")
            self.figure.colorbar(strm.lines, ax=self.ax)
        else:
            raise ValueError("Unsupported mode. Choose 'vector' or 'stream'.")
        
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Dimension 1")
        self.ax.set_ylabel("Dimension 2")
        
    def update_flow_matrix(self, new_flow_matrix: np.ndarray) -> None:
        """
        Updates the current flow matrix to a new matrix.
        
        Parameters:
            new_flow_matrix (np.ndarray): The new information flow matrix.
        """
        self.flow_matrix = new_flow_matrix

    def __repr__(self) -> str:
        matrix_shape = self.flow_matrix.shape if self.flow_matrix is not None else "None"
        return f"<InformationFlowVisualization title='{self.title}' matrix_shape={matrix_shape}>"
