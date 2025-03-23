# src/core/selection.py

import numpy as np
from typing import List, Optional
from .absolute import AbsoluteEntity
from .interaction import InteractionOperator

class SelectionPrinciple:
    """
    Enforces the principle of least cross-absolute action across a set of interaction operators.
    The selection mechanism identifies the minimal entropy path for force emergence and
    information continuity using CEFT and FDT constraints.
    """

    def __init__(self, candidates: List[InteractionOperator]):
        if not candidates or len(candidates) < 2:
            raise ValueError("At least two interactions are required for selection.")
        self.candidates = candidates
        self.minimal_index: Optional[int] = None
        self.minimal_entropy: Optional[float] = None
        self.entropy_landscape: List[float] = []

    def evaluate_candidates(self):
        """
        Computes the entropy of all candidate interactions and identifies
        the minimum-entropy path.
        """
        self.entropy_landscape = []
        for i, interaction in enumerate(self.candidates):
            entropy = interaction.calculate_interaction_entropy()
            self.entropy_landscape.append(entropy)

        self.minimal_index = int(np.argmin(self.entropy_landscape))
        self.minimal_entropy = self.entropy_landscape[self.minimal_index]

    def get_selected_interaction(self) -> InteractionOperator:
        """
        Returns the interaction that minimizes cross-absolute action.
        """
        if self.minimal_index is None:
            self.evaluate_candidates()
        return self.candidates[self.minimal_index]

    def is_coherent(self, tolerance: float = 1e-6) -> bool:
        """
        Checks if the entropy landscape is flat enough to indicate degeneracy (i.e., coherent fields).
        """
        if not self.entropy_landscape:
            self.evaluate_candidates()
        std_dev = np.std(self.entropy_landscape)
        return std_dev < tolerance

    def summary(self, verbose: bool = False) -> dict:
        """
        Full report of selection, including entropy comparisons and coherence check.
        """
        self.evaluate_candidates()
        selected = self.get_selected_interaction()
        coherence = self.is_coherent()
        if verbose:
            print(f"[SelectionPrinciple] Selected: {selected.label}")
            print(f"[SelectionPrinciple] Minimal Entropy: {self.minimal_entropy:.6f}")
            print(f"[SelectionPrinciple] Coherence: {coherence}")
        return {
            "selected_label": selected.label,
            "minimal_entropy": self.minimal_entropy,
            "coherence": coherence,
            "entropy_landscape": self.entropy_landscape
        }

    def __repr__(self):
        return f"<SelectionPrinciple candidates={len(self.candidates)} minimal_entropy={self.minimal_entropy or 'uncomputed'}>"
