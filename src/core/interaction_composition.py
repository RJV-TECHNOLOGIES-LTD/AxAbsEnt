# src/core/interaction_composition.py

import numpy as np
from typing import List, Dict
from .interaction import InteractionOperator
from .mediator import MediatorSpace

class InteractionComposition:
    """
    Represents a higher-order composition of multiple InteractionOperators
    within or across different MediatorSpaces. Enables chaining, entanglement,
    and projection across topological strata using composite projection tensors.
    """

    def __init__(self, interactions: List[InteractionOperator], mediators: List[MediatorSpace]):
        if len(interactions) != len(mediators):
            raise ValueError("Each interaction must be assigned a corresponding mediator space.")
        self.interactions = interactions
        self.mediators = mediators
        self.composite_tensor: np.ndarray = None
        self.global_entropy: float = None
        self.entanglement_signature: np.ndarray = None

    def fuse_tensor_fields(self) -> np.ndarray:
        """
        Fuse all interaction tensor fields via mediator-projected composition.
        This creates a single high-order field used in topological unification.
        """
        fused = None
        for interaction, mediator in zip(self.interactions, self.mediators):
            tensor = interaction.compose_tensor_field()
            projection = mediator.generate_projection_tensor()
            projected_tensor = projection @ tensor @ projection.T
            fused = projected_tensor if fused is None else fused + projected_tensor
        self.composite_tensor = fused
        return self.composite_tensor

    def compute_global_entropy(self) -> float:
        """
        Calculate the Frobenius norm of the fused field to obtain system-wide entropy.
        """
        if self.composite_tensor is None:
            self.fuse_tensor_fields()
        self.global_entropy = np.linalg.norm(self.composite_tensor, ord="fro")
        return self.global_entropy

    def derive_entanglement_signature(self) -> np.ndarray:
        """
        Constructs a derived entanglement tensor across all interactions,
        representing the integrated trace of mediator-projected cross-absolute entropies.
        """
        signatures = []
        for interaction in self.interactions:
            interaction.compute_selection_scalar()
            entropy = interaction.calculate_interaction_entropy()
            scalar = interaction.selection_scalar
            signatures.append(scalar * entropy)
        self.entanglement_signature = np.array(signatures)
        return self.entanglement_signature

    def summarize(self, verbose: bool = False) -> Dict[str, float]:
        """
        Full summary of composition result, entropy, and entanglement structure.
        """
        entropy = self.compute_global_entropy()
        entanglement = self.derive_entanglement_signature()
        if verbose:
            print(f"[Composition] Global Entropy: {entropy:.6f}")
            print(f"[Composition] Entanglement Signature: {entanglement}")
        return {
            "global_entropy": entropy,
            "entanglement_vector": entanglement
        }

    def __repr__(self):
        return f"<InteractionComposition sets={len(self.interactions)} global_entropy={self.global_entropy or 'uncomputed'}>"
