# src/forces/strong.py

import numpy as np
from typing import List, Optional
from ..core.absolute import AbsoluteEntity
from ..core.interaction_composition import InteractionComposition
from ..core.transfinite import TransfiniteChain
from ..core.mediator import MediatorSpace

class StrongForceField:
    """
    Models the strong interaction as a confinement-based tensor field formed by
    intra-signature compression and topological phase-locking of absolutes within
    a curvature-stabilized mediator space. Emerges through entanglement collapse
    and entropy flux acceleration across transfinite chains.
    """

    def __init__(self, compositions: List[InteractionComposition], mediator: MediatorSpace, steps: int = 5):
        self.compositions = compositions
        self.mediator = mediator
        self.transfinite_chain = TransfiniteChain(compositions, ordinal_limit=steps)
        self.entanglement_matrix: Optional[np.ndarray] = None
        self.binding_energy: Optional[float] = None
        self.confinement_tensor: Optional[np.ndarray] = None

    def build_entanglement_matrix(self):
        """
        Constructs the cross-chain entanglement matrix using transfinite propagation.
        """
        self.entanglement_matrix = self.transfinite_chain.build_entanglement_matrix()
        return self.entanglement_matrix

    def compute_binding_energy(self):
        """
        Computes the emergent binding energy by evaluating curvature-locked entropy variance.
        This reflects the phase collapse strength responsible for confinement.
        """
        self.transfinite_chain.generate_chain()
        variance = self.transfinite_chain.evaluate_chain_stability()
        curvature_flux = self.mediator.evaluate_curvature_flux()
        self.binding_energy = 1.0 / (variance + 1e-9) * curvature_flux  # Inverse-variance weight
        return self.binding_energy

    def generate_confinement_tensor(self):
        """
        Generates a confinement tensor by collapsing the entanglement matrix
        into curvature-projected entropic pressure.
        """
        if self.entanglement_matrix is None:
            self.build_entanglement_matrix()
        curvature = self.mediator.curvature_tensor
        pressure = self.entanglement_matrix @ self.entanglement_matrix.T
        self.confinement_tensor = curvature @ pressure @ curvature.T
        return self.confinement_tensor

    def summary(self, verbose: bool = False):
        """
        Returns all measurable quantities for strong interaction emergence.
        """
        entanglement = self.build_entanglement_matrix()
        energy = self.compute_binding_energy()
        tensor = self.generate_confinement_tensor()
        if verbose:
            print(f"[StrongForceField] Binding Energy: {energy:.6f}")
            print(f"[StrongForceField] Confinement Tensor:\n{tensor}")
            print(f"[StrongForceField] Entanglement Matrix Shape: {entanglement.shape}")
        return {
            "binding_energy": energy,
            "confinement_tensor": tensor,
            "entanglement_matrix": entanglement
        }

    def __repr__(self):
        return f"<StrongForceField chains={len(self.compositions)} energy={self.binding_energy or 'uncomputed'}>"
