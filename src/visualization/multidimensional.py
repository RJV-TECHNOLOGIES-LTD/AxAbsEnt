# src/visualization/multidimensional.py

import numpy as np
from typing import Optional
from .base import BaseVisualization

class MultidimensionalVisualization(BaseVisualization):
    """
    Visualizes multi-dimensional data by reducing it to 2D via Principal Component Analysis (PCA)
    and displaying a scatter plot. This is useful for visualizing complex datasets such as
    force field metrics, entropy maps, or simulation outputs from the AxAbsEnt framework.
    """
    
    def __init__(self, data: np.ndarray, labels: Optional[np.ndarray] = None, title: Optional[str] = "Multidimensional Visualization"):
        """
        Parameters:
            data (np.ndarray): A 2D array with shape (n_samples, n_features) representing the dataset.
            labels (Optional[np.ndarray]): An optional array of labels (or numerical values) for coloring the data points.
            title (Optional[str]): Title of the plot.
        """
        super().__init__(title)
        self.data = data
        self.labels = labels

    def _perform_pca(self, n_components: int = 2) -> np.ndarray:
        """
        Performs a simple PCA on the data to reduce it to n_components dimensions.
        
        Returns:
            np.ndarray: Transformed data with shape (n_samples, n_components).
        """
        # Center the data
        mean = np.mean(self.data, axis=0)
        centered_data = self.data - mean
        
        # Compute covariance matrix
        cov_matrix = np.cov(centered_data, rowvar=False)
        
        # Eigen decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # Sort eigenvectors by descending eigenvalues
        sorted_indices = np.argsort(eigenvalues)[::-1]
        top_components = eigenvectors[:, sorted_indices[:n_components]]
        
        # Project data onto top principal components
        transformed_data = centered_data.dot(top_components)
        return transformed_data

    def generate_plot(self, n_components: int = 2) -> None:
        """
        Generates a scatter plot of the data after reducing it to n_components dimensions.
        
        Parameters:
            n_components (int): Number of dimensions to reduce to (default is 2 for scatter plotting).
        """
        self.setup_plot(figsize=(8, 6))
        transformed_data = self._perform_pca(n_components)
        
        if self.labels is not None:
            scatter = self.ax.scatter(transformed_data[:, 0], transformed_data[:, 1], 
                                      c=self.labels, cmap="viridis", edgecolor='k')
            self.figure.colorbar(scatter, ax=self.ax)
        else:
            self.ax.scatter(transformed_data[:, 0], transformed_data[:, 1])
            
        self.ax.set_xlabel("Principal Component 1")
        self.ax.set_ylabel("Principal Component 2")
        self.ax.set_title(self.title)

    def update_data(self, new_data: np.ndarray, new_labels: Optional[np.ndarray] = None) -> None:
        """
        Updates the dataset and optional labels for visualization.
        
        Parameters:
            new_data (np.ndarray): New data array with shape (n_samples, n_features).
            new_labels (Optional[np.ndarray]): Optional new labels for the data points.
        """
        self.data = new_data
        self.labels = new_labels

    def __repr__(self) -> str:
        return f"<MultidimensionalVisualization title='{self.title}' data_shape={self.data.shape}>"
