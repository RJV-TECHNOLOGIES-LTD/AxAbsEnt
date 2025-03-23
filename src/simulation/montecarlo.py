# src/simulation/montecarlo.py

import numpy as np
from typing import List, Callable
from ..core.absolute import AbsoluteEntity
from ..simulation.dynamics import DynamicSystemSimulation

class MonteCarloSimulation:
    """
    Performs Monte Carlo simulation for the cross-absolute dynamic system.
    It runs a specified number of simulation iterations with randomized initial conditions,
    collecting statistics on the final action functional and related emergent parameters.
    """

    def __init__(self, 
                 entities_factory: Callable[[], List[AbsoluteEntity]], 
                 time_step: float = 0.01, 
                 total_time: float = 1.0, 
                 num_runs: int = 100):
        """
        Parameters:
            entities_factory: A callable that returns a fresh list of AbsoluteEntity objects,
                              each with randomized properties/signatures.
            time_step: Time step for the dynamic simulation.
            total_time: Total time for each simulation run.
            num_runs: Number of Monte Carlo simulation iterations.
        """
        self.entities_factory = entities_factory
        self.time_step = time_step
        self.total_time = total_time
        self.num_runs = num_runs
        self.results = []  # To store simulation outcomes for each run

    def run_simulation(self) -> None:
        """
        Executes the simulation num_runs times, each with new initial conditions,
        and collects the final action value along with simulation history.
        """
        self.results.clear()
        for run in range(self.num_runs):
            entities = self.entities_factory()
            sim = DynamicSystemSimulation(entities, time_step=self.time_step, total_time=self.total_time)
            history = sim.run()
            final_action = history[-1] if history else None
            self.results.append({
                "final_action": final_action,
                "action_history": history,
                "simulation_time": sim.current_time
            })

    def compute_statistics(self) -> dict:
        """
        Computes statistical metrics over the Monte Carlo runs.
        Returns a dictionary with the mean and variance of the final action values.
        """
        final_actions = [res["final_action"] for res in self.results if res["final_action"] is not None]
        if not final_actions:
            return {"mean_final_action": None, "variance_final_action": None, "num_runs": 0}
        mean_action = np.mean(final_actions)
        variance_action = np.var(final_actions)
        return {
            "mean_final_action": mean_action,
            "variance_final_action": variance_action,
            "num_runs": len(final_actions)
        }

    def summary(self, verbose: bool = False) -> dict:
        """
        Runs the full Monte Carlo simulation, computes statistics,
        and returns a summary of the results.
        """
        self.run_simulation()
        stats = self.compute_statistics()
        if verbose:
            print(f"[MonteCarloSimulation] Runs: {stats['num_runs']}")
            if stats['mean_final_action'] is not None:
                print(f"[MonteCarloSimulation] Mean Final Action: {stats['mean_final_action']:.6f}")
                print(f"[MonteCarloSimulation] Variance: {stats['variance_final_action']:.6e}")
            else:
                print("[MonteCarloSimulation] No valid final action values computed.")
        return stats

    def __repr__(self):
        return f"<MonteCarloSimulation runs={self.num_runs}>"
