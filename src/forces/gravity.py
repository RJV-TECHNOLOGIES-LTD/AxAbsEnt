# src/forces/gravity.py

import numpy as np
from typing import List, Optional
from ..core.absolute import AbsoluteEntity
from ..core.interaction import InteractionOperator
from ..core.action import CrossAbsoluteAction
from ..core.mediator import MediatorSpace

class GravitationalField:
    """
    Emergent gravitational field computed from entropic curvature flux between
    absolute entities. This is derived as the topological gradient of action
    across mediator space curvature tensors.
    """

    def __init__(self, entities: List[AbsoluteEntity], mediator: MediatorSpace):
        if len(entities) < 2:
            raise ValueError("At least two entities are required to compute a gravitational field.")
        self.entities = entities
        self.mediator = mediator
        self.interaction = InteractionOperator(entities)
        self.action = CrossAbsoluteAction([self.interaction])
        self.field_tensor: Optional[np.ndarray] = None
        self.potential: Optional[float] = None
        self.curvature_flux: Optional[float] = None

    def compute_curvature_flux(self):
        """
        Measures the scalar curvature flux across mediator topology (CEFT).
        This reflects the gravitational intensity prior to field projection.
        """
        self.curvature_flux = self.mediator.evaluate_curvature_flux()
        return self.curvature_flux

    def compute_field_tensor(self):
        """
        Computes the gravitational field tensor as a projected entropy-action gradient
        across mediator curvature and signature variance.
        """
        entropy_gradient = self.action.compute_gradient_field()
        curvature = self.mediator.curvature_tensor
        P = self.mediator.generate_projection_tensor()

        gradient_matrix = np.outer(entropy_gradient, entropy_gradient)
        self.field_tensor = P @ gradient_matrix @ P.T @ curvature
        return self.field_tensor

    def compute_potential_energy(self):
        """
        Computes a scalar gravitational potential based on action and curvature flux.
        """
        if self.curvature_flux is None:
            self.compute_curvature_flux()
        total_action = self.action.evaluate_action()
        self.potential = self.curvature_flux * total_action
        return self.potential

    def summary(self, verbose: bool = False):
        """
        Returns full gravitational field report: tensor, potential, and flux.
        """
        tensor = self.compute_field_tensor()
        potential = self.compute_potential_energy()
        flux = self.curvature_flux
        if verbose:
            print(f"[GravitationalField] Potential: {potential:.6f}")
            print(f"[GravitationalField] Curvature Flux: {flux:.6f}")
            print(f"[GravitationalField] Field Tensor:\n{tensor}")
        return {
            "gravitational_tensor": tensor,
            "gravitational_potential": potential,
            "curvature_flux": flux
        }

    def __repr__(self):
        return f"<GravitationalField entities={len(self.entities)} potential={self.potential or 'uncomputed'}>"
