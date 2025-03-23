# src/visualization/interactive.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from typing import Callable, Optional, Any
from .base import BaseVisualization

class InteractiveVisualization(BaseVisualization):
    """
    An interactive visualization tool that allows dynamic adjustment of a parameter
    affecting a plot. It uses a slider to update the visualization based on a provided
    update function, and a reset button to return to default settings.
    
    Attributes:
        data (np.ndarray): The base dataset to visualize.
        update_func (Callable[[np.ndarray, float], np.ndarray]):
            A function that takes the base data and a parameter value, and returns the updated data.
        slider_val (float): The current value of the interactive parameter.
    """
    
    def __init__(self, 
                 data: np.ndarray, 
                 update_func: Callable[[np.ndarray, float], np.ndarray],
                 title: Optional[str] = "Interactive Visualization"):
        super().__init__(title)
        self.data = data
        self.update_func = update_func
        self.slider_val = 1.0  # default initial parameter
        self.slider = None
        self.button = None
        self.im = None  # to hold the image plot
        
    def generate_plot(self) -> None:
        """
        Generates an interactive plot. Displays the initial data as a heatmap,
        and adds a slider to adjust a parameter that dynamically updates the plot.
        Also provides a reset button to revert to the default parameter.
        """
        self.setup_plot(figsize=(10, 6))
        
        # Display initial data using a heatmap.
        self.im = self.ax.imshow(self.data, cmap="viridis", origin="lower")
        self.ax.set_title(self.title)
        
        # Adjust layout to accommodate slider and button.
        plt.subplots_adjust(bottom=0.25)
        
        # Create slider axis and slider widget.
        ax_slider = self.figure.add_axes([0.25, 0.1, 0.65, 0.03], facecolor="lightgoldenrodyellow")
        self.slider = Slider(ax_slider, 'Parameter', 0.1, 10.0, valinit=self.slider_val)
        self.slider.on_changed(self.on_slider_change)
        
        # Create a reset button.
        ax_button = self.figure.add_axes([0.8, 0.025, 0.1, 0.04])
        self.button = Button(ax_button, 'Reset', color="lightgoldenrodyellow", hovercolor="0.975")
        self.button.on_clicked(self.on_reset)
        
    def on_slider_change(self, val: float) -> None:
        """
        Callback function that updates the visualization when the slider value changes.
        
        Parameters:
            val (float): The current value of the slider.
        """
        self.slider_val = val
        # Compute new data using the update function.
        new_data = self.update_func(self.data, val)
        # Update the heatmap data.
        self.im.set_data(new_data)
        self.figure.canvas.draw_idle()
        
    def on_reset(self, event: Any) -> None:
        """
        Resets the slider to its initial value and updates the visualization accordingly.
        """
        self.slider.reset()
        
    def __repr__(self) -> str:
        return f"<InteractiveVisualization title='{self.title}' slider_val={self.slider_val}>"
