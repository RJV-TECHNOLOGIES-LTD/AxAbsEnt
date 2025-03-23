# src/core/information.py

import numpy as np
from typing import Tuple, Optional
from .absolute import AbsoluteEntity
from .mediator import MediatorSpace

class InformationTransfer:
    """
    Models entropy-based information propagation between Absolute Entities
    using mediator-encoded projection tensors and curvature-aware channels.
    This mechanism operates under the constraint of non-local entropic causality.
    """

    def __init__(self, source: AbsoluteEntity, target: AbsoluteEntity, mediator: MediatorSpace):
        self.source = source
        self.target = target
        self.mediator = mediator
        self.information_flux: Optional[np.ndarray] = None
        self.entropy_delta: Optional[float] = None

    def compute_flux(self):
        """
        Computes the projected information flux vector from source to target using
        mediator curvature and symmetry-preserving selection metrics.
        """
        P = self.mediator.generate_projection_tensor()

        S = self.source.signature
        T = self.target.signature

        flux_matrix = P @ (S - T) @ P.T
        self.information_flux = flux_matrix
        return flux_matrix

    def evaluate_entropy_delta(self):
        """
        Measures the entropy shift due to information flux using the Frobenius norm
        of the flux matrix. This indicates how much structural information is transmitted.
        """
        if self.information_flux is None:
            self.compute_flux()
        self.entropy_delta = np.linalg.norm(self.information_flux, ord="fro")
        return self.entropy_delta

    def is_reversible(self, threshold: float = 1e-8) -> bool:
        """
        Evaluates if the information transfer is entropy-reversible under CEFT.
        A low entropy delta implies theoretical reversibility of state.
        """
        if self.entropy_delta is None:
            self.evaluate_entropy_delta()
        return self.entropy_delta < threshold

    def summary(self, verbose: bool = False) -> Tuple[np.ndarray, float, bool]:
        """
        Returns a full summary of the transfer operation.
        """
        flux = self.compute_flux()
        delta = self.evaluate_entropy_delta()
        reversible = self.is_reversible()
        if verbose:
            print(f"[InformationTransfer] Entropy Δ: {delta:.6f} | Reversible: {reversible}")
        return flux, delta, reversible

    def __repr__(self):
        return f"<InformationTransfer source={self.source.identifier[:6]} target={self.target.identifier[:6]} entropy_delta={self.entropy_delta or 'uncomputed'}>"
