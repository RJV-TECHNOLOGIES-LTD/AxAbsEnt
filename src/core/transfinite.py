# src/core/transfinite.py

import numpy as np
from typing import List, Optional
from .interaction_composition import InteractionComposition

class TransfiniteChain:
    """
    Represents a recursive transfinite sequence of interaction compositions.
    Models force propagation and resonance diffusion across ordinal levels,
    enabling access to non-finite interaction behavior and entropy chains.
    """

    def __init__(self, base_compositions: List[InteractionComposition], ordinal_limit: int = 10):
        if ordinal_limit < 1:
            raise ValueError("Ordinal limit must be at least 1.")
        self.base_compositions = base_compositions
        self.ordinal_limit = ordinal_limit
        self.chain: List[np.ndarray] = []
        self.entropy_trace: List[float] = []
        self.entanglement_matrix: Optional[np.ndarray] = None

    def generate_chain(self):
        """
        Iteratively builds the transfinite chain using recurrence on composite tensors.
        Each step is a transformation on the prior layer via CEFT-prescribed entropy decay.
        """
        current = None
        self.chain.clear()
        self.entropy_trace.clear()

        for idx in range(self.ordinal_limit):
            base = self.base_compositions[idx % len(self.base_compositions)]
            tensor = base.fuse_tensor_fields()
            entropy = base.compute_global_entropy()
            if current is None:
                current = tensor
            else:
                current = 0.5 * (current + tensor) - 0.1 * np.eye(current.shape[0]) * entropy  # Controlled decay
            self.chain.append(current.copy())
            self.entropy_trace.append(np.linalg.norm(current, ord="fro"))

    def build_entanglement_matrix(self):
        """
        Constructs a matrix where each row is an entanglement vector at a transfinite ordinal step.
        """
        vectors = []
        for base in self.base_compositions:
            vec = base.derive_entanglement_signature()
            vectors.append(vec)
        self.entanglement_matrix = np.vstack(vectors)
        return self.entanglement_matrix

    def evaluate_chain_stability(self) -> float:
        """
        Measures the overall entropy flux variance across the transfinite sequence.
        Lower variance indicates higher topological coherence.
        """
        if not self.entropy_trace:
            self.generate_chain()
        return float(np.var(self.entropy_trace))

    def summarize(self, verbose: bool = False):
        """
        Summary report for the transfinite chain: entropy decay, stability, and entanglement behavior.
        """
        if not self.entanglement_matrix:
            self.build_entanglement_matrix()
        stability = self.evaluate_chain_stability()
        if verbose:
            print(f"[Transfinite Chain] Ordinal Steps: {self.ordinal_limit}")
            print(f"[Transfinite Chain] Stability Index (Entropy Variance): {stability:.6e}")
            print(f"[Transfinite Chain] Entanglement Matrix Shape: {self.entanglement_matrix.shape}")
        return {
            "ordinal_steps": self.ordinal_limit,
            "entropy_variance": stability,
            "entanglement_shape": self.entanglement_matrix.shape
        }

    def __repr__(self):
        return f"<TransfiniteChain steps={self.ordinal_limit} stability={self.evaluate_chain_stability():.4e}>"
