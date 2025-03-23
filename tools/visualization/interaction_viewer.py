# tools/visualization/interaction_viewer.py

import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator, compose_interactions

class InteractionViewer:
    """
    Visualizes the directed interaction graph of Absolute Entities connected via
    InteractionOperators. This reveals topological structure, dependency chains,
    and potential symmetry collapses in cross-absolute systems.

    Nodes represent absolute entities.
    Edges represent directional interaction flows.
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.entities = {}
        self.interactions = []

    def add_entity(self, entity: AbsoluteEntity):
        """Add an AbsoluteEntity as a node in the interaction graph."""
        self.entities[entity.identifier] = entity
        self.graph.add_node(entity.identifier, label="Absolute")

    def add_interaction(self, source_id: str, target_id: str, operator: InteractionOperator):
        """
        Add a directional interaction (edge) from source to target with the given operator.
        """
        if source_id not in self.entities or target_id not in self.entities:
            raise ValueError("Source or target entity ID not found.")
        self.graph.add_edge(source_id, target_id, label=operator.name)
        self.interactions.append((source_id, target_id, operator))

    def visualize(self, layout: str = "spring"):
        """Render the interaction graph using the specified layout."""
        if layout == "spring":
            pos = nx.spring_layout(self.graph)
        elif layout == "circular":
            pos = nx.circular_layout(self.graph)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(self.graph)
        else:
            raise ValueError("Unsupported layout type.")

        plt.figure(figsize=(10, 8))
        edge_labels = nx.get_edge_attributes(self.graph, "label")
        node_labels = {n: n[:8] for n in self.graph.nodes()}  # Shortened UUIDs

        nx.draw_networkx_nodes(self.graph, pos, node_color="skyblue", node_size=800)
        nx.draw_networkx_edges(self.graph, pos, arrowstyle="->", arrowsize=15)
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels, font_size=9)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Cross-Absolute Interaction Graph")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    def export_topology(self) -> List[Tuple[str, str, str]]:
        """
        Return a list of interaction edges with operator names for external analysis or export.
        Format: [(source_id, target_id, operator_name), ...]
        """
        return [(src, tgt, op.name) for src, tgt, op in self.interactions]
