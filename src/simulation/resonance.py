# src/simulation/resonance.py

import numpy as np
from typing import Optional
from ..simulation.dynamics import DynamicSystemSimulation

class ResonanceSimulation:
    """
    Detects resonance within a dynamic system based on the evolution of the total action
    functional. Resonance is characterized by the variance of the action over a sliding window
    falling below a specified threshold.
    """

    def __init__(self, dynamic_sim: DynamicSystemSimulation, resonance_threshold: float = 1e-4, window_size: int = 5):
        self.dynamic_sim = dynamic_sim
        self.resonance_threshold = resonance_threshold
        self.window_size = window_size
        self.resonance_time: Optional[float] = None
        self.resonance_detected: bool = False

    def detect_resonance(self) -> bool:
        """
        Runs the dynamic simulation and evaluates the variance of the action functional
        over the last 'window_size' time steps. If the variance is below the threshold,
        resonance is flagged and the detection time is recorded.
        """
        history = self.dynamic_sim.run()
        if len(history) < self.window_size:
            return False
        window = np.array(history[-self.window_size:])
        variance = np.var(window)
        if variance < self.resonance_threshold:
            self.resonance_detected = True
            self.resonance_time = self.dynamic_sim.current_time
        return self.resonance_detected

    def summary(self, verbose: bool = False) -> dict:
        """
        Provides a summary report including:
          - Whether resonance was detected.
          - The simulation time at which resonance was detected.
          - The variance of the action functional over the last window.
        """
        detected = self.detect_resonance()
        window = self.dynamic_sim.history[-self.window_size:] if len(self.dynamic_sim.history) >= self.window_size else []
        variance = float(np.var(window)) if window != [] else None
        if verbose:
            print(f"[ResonanceSimulation] Resonance Detected: {detected}")
            print(f"[ResonanceSimulation] Resonance Time: {self.resonance_time if self.resonance_time is not None else 'N/A'}")
            if variance is not None:
                print(f"[ResonanceSimulation] Action Variance (last {self.window_size} steps): {variance:.6e}")
            else:
                print("[ResonanceSimulation] Not enough data to compute variance.")
        return {
            "resonance_detected": detected,
            "resonance_time": self.resonance_time,
            "action_variance": variance
        }

    def __repr__(self):
        return f"<ResonanceSimulation detected={self.resonance_detected} time={self.resonance_time or 'N/A'}>"
