# src/core/action.py

import numpy as np
from typing import List
from .interaction import InteractionOperator
from .selection import SelectionPrinciple

class CrossAbsoluteAction:
    """
    Computes the total action functional across a system of interacting absolutes.
    This scalar integrates entropy, field symmetry, and curvature response under
    CEFT + SDI constraints and serves as the emergent driver for force formation.
    """

    def __init__(self, interactions: List[InteractionOperator]):
        if len(interactions) < 2:
            raise ValueError("Cross-Absolute Action requires multiple interaction layers.")
        self.interactions = interactions
        self.selection = SelectionPrinciple(interactions)
        self.total_action: float = 0.0
        self.gradient_field: np.ndarray = None

    def evaluate_action(self):
        """
        Computes the scalar action value as the sum of weighted entropies,
        modulated by the selection scalar and cross-absolute geometry.
        """
        self.selection.evaluate_candidates()
        entropies = self.selection.entropy_landscape
        selected = self.selection.get_selected_interaction()
        scalar = selected.compute_selection_scalar()
        self.total_action = scalar * np.sum(entropies)
        return self.total_action

    def compute_gradient_field(self):
        """
        Computes the entropy gradient field from the entropy landscape.
        This is a synthetic 'force field' emerging from cross-absolute action flow.
        """
        entropies = np.array(self.selection.entropy_landscape)
        diffs = np.diff(entropies, prepend=entropies[0])
        self.gradient_field = -1.0 * diffs  # Negative gradient = direction of action flow
        return self.gradient_field

    def detect_resonance(self, tolerance: float = 1e-5) -> bool:
        """
        Determines whether the system exhibits degeneracy (resonance),
        where entropy gradients flatten across interactions.
        """
        if self.gradient_field is None:
            self.compute_gradient_field()
        return np.max(np.abs(self.gradient_field)) < tolerance

    def summary(self, verbose: bool = False):
        """
        Returns a full report of action, field, and resonance status.
        """
        action = self.evaluate_action()
        field = self.compute_gradient_field()
        resonance = self.detect_resonance()
        if verbose:
            print(f"[CrossAbsoluteAction] Total Action: {action:.6f}")
            print(f"[CrossAbsoluteAction] Gradient Field: {field}")
            print(f"[CrossAbsoluteAction] Resonant: {resonance}")
        return {
            "total_action": action,
            "gradient_field": field,
            "resonant": resonance
        }

    def __repr__(self):
        return f"<CrossAbsoluteAction interactions={len(self.interactions)} action={self.total_action:.6f}>"
