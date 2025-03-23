# src/core/interaction.py

import numpy as np
from typing import List, Dict, Optional
from .absolute import AbsoluteEntity
from .constraints import validate_symmetry_conditions

class InteractionOperator:
    """
    Models the interaction between multiple Absolute Entities using symmetry decay,
    projection tensors, and the cross-absolute selection principle.
    """

    def __init__(self, participants: List[AbsoluteEntity], label: Optional[str] = None):
        if len(participants) < 2:
            raise ValueError("At least two Absolute Entities are required for an interaction.")
        self.participants = participants
        self.label = label or "UnnamedInteraction"
        self.tensor_field: Optional[np.ndarray] = None
        self.interaction_entropy: Optional[float] = None
        self.selection_scalar: Optional[float] = None
        self._validated = False

    def compose_tensor_field(self):
        """
        Compose the global interaction tensor field from all participants' signatures.
        """
        tensors = [abs.signature for abs in self.participants]
        self.tensor_field = sum(tensors)
        return self.tensor_field

    def compute_selection_scalar(self):
        """
        Apply the selection principle to all Absolute Entities, generating a composite scalar.
        This scalar represents the projected interaction entropy in mediator space.
        """
        scalars = [abs.encode_selection() for abs in self.participants]
        self.selection_scalar = sum(scalars) / len(scalars)
        return self.selection_scalar

    def validate_symmetry_break(self):
        """
        Check all symmetry conditions across Absolute Entities. This invokes the universal
        decay constraints as required by CEFT and SDI.
        """
        self._validated = validate_symmetry_conditions(self.participants)
        return self._validated

    def calculate_interaction_entropy(self):
        """
        Derive the entropy of interaction via Frobenius norm of the projected tensor field.
        """
        if self.tensor_field is None:
            self.compose_tensor_field()
        self.interaction_entropy = np.linalg.norm(self.tensor_field, ord="fro")
        return self.interaction_entropy

    def evaluate(self, verbose: bool = False) -> Dict[str, float]:
        """
        Full interaction evaluation pipeline.
        Returns a dictionary containing entropy, scalar, and symmetry status.
        """
        if not self._validated:
            self.validate_symmetry_break()
        entropy = self.calculate_interaction_entropy()
        scalar = self.compute_selection_scalar()
        if verbose:
            print(f"[{self.label}] Interaction Entropy: {entropy:.5f}, Selection Scalar: {scalar:.5f}")
        return {
            "interaction_entropy": entropy,
            "selection_scalar": scalar,
            "symmetry_valid": self._validated
        }

    def __repr__(self):
        return f"<InteractionOperator label={self.label} participants={len(self.participants)}>"
