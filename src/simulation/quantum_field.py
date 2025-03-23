# src/simulation/quantum_field.py

import numpy as np
from typing import List, Optional
from ..core.absolute import AbsoluteEntity
from ..core.mediator import MediatorSpace
from ..mathematics.tensors import tensor_norm
from ..mathematics.entropy import von_neumann_entropy

class QuantumFieldSimulation:
    """
    Simulates the evolution of a quantum field over a set of Absolute Entities.
    The field is initialized as a composite state derived from entity signatures and
    evolves under a simplified quantum evolution equation, incorporating mediator curvature.
    """

    def __init__(self, entities: List[AbsoluteEntity], mediator: MediatorSpace, time_step: float = 0.01, total_time: float = 1.0):
        if not entities:
            raise ValueError("At least one Absolute Entity is required for quantum field simulation.")
        self.entities = entities
        self.mediator = mediator
        self.time_step = time_step
        self.total_time = total_time
        self.current_time = 0.0
        self.field_state: Optional[np.ndarray] = None  # Composite field state tensor

    def initialize_field(self) -> np.ndarray:
        """
        Initializes the quantum field state by averaging the signatures of all entities.
        The field state is normalized for stability in the evolution.
        """
        tensors = [entity.signature for entity in self.entities]
        composite_tensor = np.mean(tensors, axis=0)
        self.field_state = composite_tensor / tensor_norm(composite_tensor)
        return self.field_state

    def update_field(self) -> np.ndarray:
        """
        Evolves the quantum field state using a simplified evolution operator derived from
        the mediator's curvature tensor. In a full model, this operator would encapsulate
        Hamiltonian evolution, potential interactions, and entropic contributions.
        """
        if self.field_state is None:
            self.initialize_field()
        curvature = self.mediator.curvature_tensor
        # Construct a linear evolution operator; identity plus a curvature-derived perturbation
        evolution_operator = np.eye(curvature.shape[0]) + self.time_step * (curvature - np.eye(curvature.shape[0]))
        new_state = evolution_operator @ self.field_state @ evolution_operator.T
        # Normalize the updated field state to prevent divergence
        new_state = new_state / tensor_norm(new_state)
        self.field_state = new_state
        self.current_time += self.time_step
        return self.field_state

    def run(self) -> np.ndarray:
        """
        Runs the simulation until the total simulation time is reached.
        Returns the final quantum field state.
        """
        self.initialize_field()
        while self.current_time < self.total_time:
            self.update_field()
        return self.field_state

    def compute_field_entropy(self) -> float:
        """
        Computes the entropy of the current quantum field state using a surrogate density matrix.
        The field state is converted into a density matrix and processed with the Von Neumann entropy.
        """
        if self.field_state is None:
            raise ValueError("Field state is not initialized.")
        # Construct a density matrix via the outer product (ensuring positive semi-definiteness)
        density_matrix = np.dot(self.field_state, self.field_state.T)
        return von_neumann_entropy(density_matrix)

    def summary(self, verbose: bool = False) -> dict:
        """
        Runs the simulation and returns a summary including the final field state,
        its entropy, and the total simulation time.
        """
        final_state = self.run()
        entropy = self.compute_field_entropy()
        if verbose:
            print(f"[QuantumFieldSimulation] Final Field State:\n{final_state}")
            print(f"[QuantumFieldSimulation] Field Entropy: {entropy:.6f}")
            print(f"[QuantumFieldSimulation] Total Simulation Time: {self.current_time:.3f}s")
        return {
            "final_state": final_state,
            "field_entropy": entropy,
            "simulation_time": self.current_time
        }

    def __repr__(self):
        return f"<QuantumFieldSimulation time_step={self.time_step} total_time={self.total_time} current_time={self.current_time}>"
