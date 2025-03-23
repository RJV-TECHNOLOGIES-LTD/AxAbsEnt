# src/simulation/dynamics.py

import numpy as np
from typing import List
from ..core.absolute import AbsoluteEntity
from ..core.interaction import InteractionOperator
from ..core.action import CrossAbsoluteAction
from ..mathematics.tensors import tensor_norm

class DynamicSystemSimulation:
    """
    Simulates the dynamic evolution of a cross-absolute system by integrating the action
    functional, interaction dynamics, and mediator curvature effects. The simulation
    uses a time-stepping algorithm to update the system's state and records emergent
    force trends over time.
    """

    def __init__(self, entities: List[AbsoluteEntity], time_step: float = 0.01, total_time: float = 1.0):
        if not entities or len(entities) < 2:
            raise ValueError("Dynamic simulation requires at least two interacting Absolute Entities.")
        self.entities = entities
        self.time_step = time_step
        self.total_time = total_time
        self.current_time = 0.0
        self.history = []  # Records the total action functional at each time step
        
        # Initialize the system interaction and corresponding action functional
        self.interaction = InteractionOperator(entities)
        self.action = CrossAbsoluteAction([self.interaction])

    def update_state(self):
        """
        Updates the system's state by computing the current action and adjusting each
        Absolute Entity's property (e.g., 'state_value') based on the gradient of the action.
        """
        # Evaluate current action functional value
        current_action = self.action.evaluate_action()
        self.history.append(current_action)
        
        # Compute the gradient field (interpreted as an emergent force vector)
        gradient = self.action.compute_gradient_field()
        grad_magnitude = np.mean(np.abs(gradient))
        
        # Update each entity's 'state_value' property using a simple gradient descent-like rule
        for entity in self.entities:
            current_value = entity.properties.get("state_value", 1.0)
            new_value = current_value - self.time_step * grad_magnitude
            entity.set_property("state_value", new_value)

    def run(self) -> List[float]:
        """
        Runs the dynamic simulation until the total simulation time is reached.
        Returns the history of the total action functional over time.
        """
        while self.current_time < self.total_time:
            self.update_state()
            self.current_time += self.time_step
        return self.history

    def summary(self, verbose: bool = False) -> dict:
        """
        Provides a summary of the simulation including the final action value, action history,
        and total simulation time.
        """
        history = self.run()
        final_action = history[-1] if history else None
        if verbose:
            print(f"[DynamicSystemSimulation] Final Action: {final_action:.6f}")
            print(f"[DynamicSystemSimulation] Last 5 Action Values: {history[-5:]}")
            print(f"[DynamicSystemSimulation] Total Simulation Time: {self.current_time:.3f}s")
        return {
            "final_action": final_action,
            "action_history": history,
            "total_time": self.current_time
        }

    def __repr__(self):
        return f"<DynamicSystemSimulation time_step={self.time_step} total_time={self.total_time} current_time={self.current_time}>"
