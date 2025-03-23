# src/forces/weak.py

import numpy as np
from typing import List, Optional
from ..core.absolute import AbsoluteEntity
from ..core.interaction import InteractionOperator
from ..core.action import CrossAbsoluteAction
from ..core.constraints import validate_signature_matrix
from ..core.mediator import MediatorSpace

class WeakForceField:
    """
    Models the weak interaction as an emergent result of symmetry-breaking stress
    and entropy gradient discontinuities. This force initiates structural transitions
    when curvature tolerances are violated under asymmetric entropic flow.
    """

    def __init__(self, entities: List[AbsoluteEntity], mediator: MediatorSpace):
        if len(entities) < 2:
            raise ValueError("Weak interaction requires at least two interacting absolutes.")
        self.entities = entities
        self.mediator = mediator
        self.interaction = InteractionOperator(entities)
        self.action = CrossAbsoluteAction([self.interaction])
        self.parity_break_tensor: Optional[np.ndarray] = None
        self.transition_probability: Optional[float] = None
        self.stress_index: Optional[float] = None

    def compute_stress_index(self):
        """
        Quantifies entropy asymmetry as the standard deviation of action gradients.
        A high stress index indicates instability and symmetry pressure.
        """
        gradients = self.action.compute_gradient_field()
        self.stress_index = float(np.std(gradients))
        return self.stress_index

    def compute_parity_break_tensor(self):
        """
        Constructs a tensor measuring topological parity loss via non-symmetric projections
        across mediator space and signature deformations.
        """
        if not all(validate_signature_matrix(e.signature) for e in self.entities):
            raise ValueError("Invalid signature matrix detected.")

        signatures = [e.signature for e in self.entities]
        diffs = [s - s.T for s in signatures]
        accumulator = sum(d @ d.T for d in diffs)
        curvature = self.mediator.curvature_tensor
        self.parity_break_tensor = curvature @ accumulator @ curvature.T
        return self.parity_break_tensor

    def compute_transition_probability(self):
        """
        Computes the likelihood of a weak-force-induced state transition as a normalized
        entropy-stress scalar against mediator curvature deformation.
        """
        if self.stress_index is None:
            self.compute_stress_index()
        entropy = self.action.evaluate_action()
        curvature_flux = self.mediator.evaluate_curvature_flux()
        self.transition_probability = np.tanh(self.stress_index * entropy / (curvature_flux + 1e-9))
        return self.transition_probability

    def summary(self, verbose: bool = False):
        """
        Returns weak interaction field results: stress, transition probability, and parity tensor.
        """
        stress = self.compute_stress_index()
        tensor = self.compute_parity_break_tensor()
        probability = self.compute_transition_probability()
        if verbose:
            print(f"[WeakForceField] Stress Index: {stress:.6f}")
            print(f"[WeakForceField] Transition Probability: {probability:.6f}")
            print(f"[WeakForceField] Parity Break Tensor:\n{tensor}")
        return {
            "stress_index": stress,
            "transition_probability": probability,
            "parity_break_tensor": tensor
        }

    def __repr__(self):
        return f"<WeakForceField entities={len(self.entities)} transition_p={self.transition_probability or 'uncomputed'}>"
