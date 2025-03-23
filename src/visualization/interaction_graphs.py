# src/visualization/interaction_graphs.py

import matplotlib.pyplot as plt
import networkx as nx
from typing import Optional
from .base import BaseVisualization

class InteractionGraphVisualization(BaseVisualization):
    """
    Visualizes interaction graphs among Absolute Entities.
    
    Each node represents an Absolute Entity, and each edge indicates an interaction operator
    linking a pair of entities. This module supports various layout algorithms to depict
    the network structure.
    """
    
    def __init__(self, graph: Optional[nx.Graph] = None, title: Optional[str] = "Interaction Graph"):
        super().__init__(title)
        # If no graph is provided, initialize an empty undirected graph.
        self.graph = graph if graph is not None else nx.Graph()

    def generate_plot(self, layout: Optional[str] = "spring") -> None:
        """
        Generates an interaction graph plot using NetworkX and Matplotlib.
        
        Parameters:
            layout (str): Layout algorithm to use. Options include:
                          'spring' (default), 'circular', 'shell'.
        """
        self.setup_plot(figsize=(10, 8))
        # Select layout algorithm
        if layout == "spring":
            pos = nx.spring_layout(self.graph)
        elif layout == "circular":
            pos = nx.circular_layout(self.graph)
        elif layout == "shell":
            pos = nx.shell_layout(self.graph)
        else:
            pos = nx.spring_layout(self.graph)
        
        # Draw the graph on the provided axis
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_size=300, font_size=8)
        self.ax.set_title(self.title)

    def update_graph(self, new_graph: nx.Graph) -> None:
        """
        Updates the current graph to a new graph instance.
        
        Parameters:
            new_graph (nx.Graph): The new graph to visualize.
        """
        self.graph = new_graph

    def __repr__(self) -> str:
        return f"<InteractionGraphVisualization title='{self.title}' nodes={self.graph.number_of_nodes()}>"
