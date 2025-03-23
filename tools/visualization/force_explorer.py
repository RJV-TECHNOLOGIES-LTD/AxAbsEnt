# tools/visualization/force_explorer.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from axabsent.forces.extraction import extract_force_field
from axabsent.core.absolute import AbsoluteEntity
from axabsent.forces.signatures import generate_force_signature

class ForceExplorer:
    """
    Visualizes emergent force fields from cross-absolute interactions.
    Uses vector field plotting in 2D and 3D, supporting force emergence inspection
    from gravitational, electromagnetic, strong, and weak modes.

    The visualization is dynamically generated from force signature data encoded in
    AbsoluteEntity configurations and cross-absolute state gradients.
    """

    def __init__(self, entity: AbsoluteEntity, field_resolution: int = 30):
        self.entity = entity
        self.field_resolution = field_resolution
        self.signature = generate_force_signature(entity)
        self.force_field = extract_force_field(entity, resolution=field_resolution)

    def _generate_grid(self):
        """Generate spatial coordinate grid for field mapping."""
        axis = np.linspace(-1, 1, self.field_resolution)
        X, Y = np.meshgrid(axis, axis)
        return X, Y

    def _get_vector_components(self, X, Y):
        """Calculate vector field components from extracted force field."""
        Fx = np.zeros_like(X)
        Fy = np.zeros_like(Y)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                position = np.array([X[i, j], Y[i, j]])
                F_vec = self.force_field(position)
                Fx[i, j] = F_vec[0]
                Fy[i, j] = F_vec[1]
        return Fx, Fy

    def plot_vector_field(self):
        """Display 2D vector field of emergent forces using matplotlib."""
        X, Y = self._generate_grid()
        Fx, Fy = self._get_vector_components(X, Y)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X, Y, Fx, Fy, color='blue')
        ax.set_title("Emergent Force Field from AbsoluteEntity Signature")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def interactive_explorer(self):
        """
        Launch an interactive interface with a slider to modulate force signature strength
        and observe field response.
        """
        X, Y = self._generate_grid()
        Fx, Fy = self._get_vector_components(X, Y)

        fig, ax = plt.subplots()
        q = ax.quiver(X, Y, Fx, Fy)
        ax.set_title("Interactive Force Explorer")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
        slider = Slider(ax_slider, 'Signature Scale', 0.1, 5.0, valinit=1.0)

        def update(val):
            scale = slider.val
            modified_entity = AbsoluteEntity(
                identifier=self.entity.identifier,
                signature=self.entity.signature * scale,
                properties=self.entity.properties,
                state=self.entity.state
            )
            updated_field = extract_force_field(modified_entity, resolution=self.field_resolution)
            Fx_new, Fy_new = np.zeros_like(X), np.zeros_like(Y)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    F_vec = updated_field(np.array([X[i, j], Y[i, j]]))
                    Fx_new[i, j] = F_vec[0]
                    Fy_new[i, j] = F_vec[1]
            q.set_UVC(Fx_new, Fy_new)
            fig.canvas.draw_idle()

        slider.on_changed(update)
        plt.tight_layout()
        plt.show()
