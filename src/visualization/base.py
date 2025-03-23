# src/visualization/base.py

import matplotlib.pyplot as plt
from typing import Any, Optional, Tuple

class BaseVisualization:
    """
    Base class for all visualization tools in the AxAbsEnt system.
    
    Provides common functionality such as:
      - Plot initialization and configuration
      - Displaying and saving figures
      - Abstract plotting interface for subclass extensions
    """
    
    def __init__(self, title: Optional[str] = "AxAbsEnt Visualization"):
        self.title = title
        self.figure = None
        self.ax = None

    def setup_plot(self, figsize: Tuple[int, int] = (8, 6)) -> None:
        """
        Initializes the matplotlib figure and axis with a given size.
        """
        self.figure, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_title(self.title)

    def generate_plot(self, data: Any) -> None:
        """
        Abstract method to generate a plot based on provided data.
        Subclasses must override this method.
        """
        raise NotImplementedError("Subclasses should implement the generate_plot() method.")

    def show(self) -> None:
        """
        Displays the current plot.
        """
        if self.figure is None or self.ax is None:
            self.setup_plot()
        plt.show()

    def save(self, filename: str = "visualization.png", dpi: int = 300) -> None:
        """
        Saves the current figure to a file.
        """
        if self.figure is None:
            raise ValueError("No figure available to save. Generate a plot first.")
        self.figure.savefig(filename, dpi=dpi)

    def clear(self) -> None:
        """
        Clears the current figure.
        """
        if self.figure:
            plt.clf()
            self.figure, self.ax = None, None

    def __repr__(self) -> str:
        return f"<BaseVisualization title='{self.title}'>"
