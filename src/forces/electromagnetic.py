# src/forces/electromagnetic.py

import numpy as np
from typing import List, Optional
from ..core.absolute import AbsoluteEntity
from ..core.information import InformationTransfer
from ..core.mediator import MediatorSpace

class ElectromagneticField:
    """
    Models electromagnetic force emergence as a polarity-resonant information flux.
    EM behavior is constructed as a curl of entropic phase variance between paired
    Absolute Entities, and modulated by topological vector rotation in mediator space.
    """

    def __init__(self, source: AbsoluteEntity, target: AbsoluteEntity, mediator: MediatorSpace):
        self.source = source
        self.target = target
        self.mediator = mediator
        self.transfer = InformationTransfer(source, target, mediator)
        self.flux_matrix: Optional[np.ndarray] = None
        self.field_vector: Optional[np.ndarray] = None
        self.potential_vector: Optional[np.ndarray] = None
        self.resonant: Optional[bool] = None

    def compute_flux_matrix(self):
        """
        Uses mediator-projected flux between source and target signatures.
        """
        self.flux_matrix = self.transfer.compute_flux()
        return self.flux_matrix

    def compute_field_vector(self):
        """
        Computes the electromagnetic field as the curl of projected entropy differences.
        This is a topological analogy to Maxwell's ∇×E and ∇×B over information flow.
        """
        if self.flux_matrix is None:
            self.compute_flux_matrix()
        # Use antisymmetric projection as a rotational field
        antisymmetric = 0.5 * (self.flux_matrix - self.flux_matrix.T)
        self.field_vector = np.sum(antisymmetric, axis=1)
        return self.field_vector

    def compute_potential_vector(self):
        """
        Calculates the directional entropy vector (potential) from signed entropy delta.
        This represents the polarity-aligned component of the force field.
        """
        entropy_delta = self.transfer.evaluate_entropy_delta()
        signature_diff = self.source.signature - self.target.signature
        direction = np.sum(signature_diff, axis=1)
        self.potential_vector = entropy_delta * direction
        return self.potential_vector

    def detect_resonance(self, tolerance: float = 1e-6):
        """
        Detects phase resonance condition where transfer is entropy-reversible.
        """
        self.resonant = self.transfer.is_reversible(threshold=tolerance)
        return self.resonant

    def summary(self, verbose: bool = False):
        """
        Returns full electromagnetic field result: field vector, potential, resonance status.
        """
        field = self.compute_field_vector()
        potential = self.compute_potential_vector()
        resonance = self.detect_resonance()
        if verbose:
            print(f"[ElectromagneticField] Field Vector: {field}")
            print(f"[ElectromagneticField] Potential Vector: {potential}")
            print(f"[ElectromagneticField] Resonant: {resonance}")
        return {
            "field_vector": field,
            "potential_vector": potential,
            "resonant": resonance
        }

    def __repr__(self):
        return f"<ElectromagneticField source={self.source.identifier[:6]} target={self.target.identifier[:6]} resonant={self.resonant}>"
