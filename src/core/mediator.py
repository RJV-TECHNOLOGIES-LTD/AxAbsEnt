# src/core/mediator.py

import numpy as np
from typing import List, Dict, Optional
from .absolute import AbsoluteEntity

class MediatorSpace:
    """
    Represents a topological projection layer that facilitates valid interactions
    between Absolute Entities without altering their irreducible identity.
    
    MediatorSpaces apply transformation metrics, activation frames, and dimensional
    embeddings that satisfy the CEFT and FDT protocols for force emergence and transfer.
    """

    def __init__(self, dimension: int, curvature_tensor: Optional[np.ndarray] = None):
        self.dimension = dimension
        self.curvature_tensor = curvature_tensor or np.eye(dimension)
        self.projection_metric = np.eye(dimension)
        self.connection_form: Optional[np.ndarray] = None
        self.metadata: Dict[str, any] = {}

    def embed_entity(self, entity: AbsoluteEntity) -> np.ndarray:
        """
        Embed an Absolute Entity into the mediator space using its signature.
        """
        if entity.signature.shape[0] != self.dimension:
            raise ValueError("Mediator dimension mismatch with entity signature.")
        projected = self.projection_metric @ entity.signature
        return projected

    def activate_connection_form(self, method: str = "default"):
        """
        Constructs the mediator's connection form—curvature-constrained transformation tensor.
        Can use advanced methods in FDT like topological torsion balancing.
        """
        if method == "default":
            self.connection_form = self.curvature_tensor.T @ self.curvature_tensor
        else:
            raise NotImplementedError(f"Connection method '{method}' not yet implemented.")
        return self.connection_form

    def evaluate_curvature_flux(self) -> float:
        """
        Computes the scalar curvature flux using the trace of the mediator’s curvature form.
        Required for CEFT evaluation.
        """
        if self.connection_form is None:
            self.activate_connection_form()
        return np.trace(self.connection_form)

    def generate_projection_tensor(self) -> np.ndarray:
        """
        Derive the dynamic projection tensor from curvature and topology conditions.
        Can be used in interaction projections or force transformations.
        """
        return self.curvature_tensor @ self.projection_metric

    def __repr__(self):
        return f"<MediatorSpace dim={self.dimension} curvature=trace({np.trace(self.curvature_tensor):.4f})>"
