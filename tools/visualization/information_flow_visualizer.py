# tools/visualization/information_flow_visualizer.py

import numpy as np
import matplotlib.pyplot as plt
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.information import compute_information_gradient
from axabsent.core.mediator import MediatorSpace
from matplotlib import cm

class InformationFlowVisualizer:
    """
    Visualizes the entropy gradient and directional information flow resulting from
    cross-absolute mediation. This enables detection of source-sink dynamics,
    non-trivial entanglement polarity, and information density regions.

    Visual output is compliant with CEFT (Curvature Entropy Flux Tensor) mappings.
    """

    def __init__(
        self,
        source: AbsoluteEntity,
        target: AbsoluteEntity,
        mediator: MediatorSpace,
        resolution: int = 100,
    ):
        self.source = source
        self.target = target
        self.mediator = mediator
        self.resolution = resolution
        self.grid_x, self.grid_y = self._generate_grid()
        self.gradient_field = self._generate_gradient_field()

    def _generate_grid(self):
        """Create coordinate mesh for plotting."""
        axis = np.linspace(-1, 1, self.resolution)
        return np.meshgrid(axis, axis)

    def _generate_gradient_field(self):
        """Generate information gradient vectors over grid from mediator space."""
        Fx = np.zeros_like(self.grid_x)
        Fy = np.zeros_like(self.grid_y)
        for i in range(self.grid_x.shape[0]):
            for j in range(self.grid_x.shape[1]):
                point = np.array([self.grid_x[i, j], self.grid_y[i, j]])
                grad = compute_information_gradient(
                    self.source, self.target, self.mediator, point
                )
                Fx[i, j] = grad[0]
                Fy[i, j] = grad[1]
        return Fx, Fy

    def plot_entropy_flux(self):
        """Render entropy gradient vector field (information flow)."""
        Fx, Fy = self.gradient_field
        magnitude = np.sqrt(Fx**2 + Fy**2)

        fig, ax = plt.subplots(figsize=(8, 6))
        stream = ax.streamplot(
            self.grid_x, self.grid_y, Fx, Fy,
            color=magnitude, linewidth=1, cmap=cm.viridis, density=1.2
        )

        ax.set_title("Information Flow Field (Entropy Gradient)")
        ax.set_xlabel("Mediator X-axis")
        ax.set_ylabel("Mediator Y-axis")
        ax.grid(True)
        cbar = fig.colorbar(stream.lines, ax=ax, label="Information Flux Magnitude")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def compute_total_information_flux(self) -> float:
        """Quantifies net entropy flow between entities in given mediator frame."""
        Fx, Fy = self.gradient_field
        total_flux = np.sum(np.sqrt(Fx**2 + Fy**2))
        return float(total_flux)
