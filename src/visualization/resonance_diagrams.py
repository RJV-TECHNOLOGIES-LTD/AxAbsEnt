# src/visualization/resonance_diagrams.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, List
from .base import BaseVisualization

class ResonanceDiagramsVisualization(BaseVisualization):
    """
    Visualizes resonance patterns by plotting the time evolution of the action functional
    and marking regions where resonance is detected (i.e., where the variance falls below a threshold).
    
    The diagram typically includes:
      - A line plot of the action functional over time.
      - Shaded regions or markers indicating resonance intervals.
      - Annotations for critical transition points.
    """
    
    def __init__(self, 
                 time_series: Optional[List[float]] = None, 
                 time_points: Optional[List[float]] = None, 
                 resonance_threshold: Optional[float] = None,
                 title: Optional[str] = "Resonance Diagram"):
        """
        Parameters:
            time_series (List[float]): A list of action functional values over time.
            time_points (List[float]): Corresponding time points for each action value.
            resonance_threshold (float): Threshold below which resonance is flagged.
            title (str): Title of the diagram.
        """
        super().__init__(title)
        self.time_series = time_series
        self.time_points = time_points
        self.resonance_threshold = resonance_threshold

    def generate_plot(self) -> None:
        """
        Generates the resonance diagram:
          - Plots the action functional over time.
          - Marks regions where the action variance indicates resonance (action value below the threshold).
        """
        if self.time_series is None or self.time_points is None:
            raise ValueError("Time series data and corresponding time points are required.")
        if self.resonance_threshold is None:
            raise ValueError("A resonance threshold value must be provided.")

        self.setup_plot(figsize=(10, 6))
        self.ax.plot(self.time_points, self.time_series, label="Action Functional", color="blue")
        
        # Identify regions where action values fall below the threshold (resonance regions)
        resonance_regions = np.array(self.time_series) < self.resonance_threshold
        if resonance_regions.any():
            # Create a mask for shading
            self.ax.fill_between(
                self.time_points, 
                self.time_series, 
                self.resonance_threshold,
                where=resonance_regions,
                color="orange",
                alpha=0.5,
                label="Resonance Region"
            )
        
        self.ax.axhline(self.resonance_threshold, color="red", linestyle="--", label="Resonance Threshold")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Action Functional Value")
        self.ax.set_title(self.title)
        self.ax.legend()

    def update_data(self, time_series: List[float], time_points: List[float], resonance_threshold: float) -> None:
        """
        Updates the time series data and resonance threshold.
        """
        self.time_series = time_series
        self.time_points = time_points
        self.resonance_threshold = resonance_threshold

    def __repr__(self) -> str:
        ts_len = len(self.time_series) if self.time_series is not None else "None"
        return f"<ResonanceDiagramsVisualization title='{self.title}' data_points={ts_len}>"
