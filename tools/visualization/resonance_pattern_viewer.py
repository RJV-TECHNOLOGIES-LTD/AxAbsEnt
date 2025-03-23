# tools/visualization/resonance_pattern_viewer.py

import numpy as np
import matplotlib.pyplot as plt
from axabsent.simulation.resonance import detect_resonance_cycles
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator
from typing import List, Dict

class ResonancePatternViewer:
    """
    Detects and visualizes resonance patterns arising from cyclic interaction chains
    between absolute entities. These cycles represent reinforcement loops in
    transfinite mediation and are mapped as energy convergence loci.

    Output: heatmap showing resonance intensity at each absolute node.
    """

    def __init__(self, entities: List[AbsoluteEntity], interactions: List[InteractionOperator]):
        self.entities = entities
        self.interactions = interactions
        self.resonance_map: Dict[str, float] = {}

    def analyze_resonance(self):
        """
        Run detection algorithm over entity-interaction system to calculate
        resonance intensity at each node.
        """
        self.resonance_map = detect_resonance_cycles(self.entities, self.interactions)

    def plot_resonance_heatmap(self):
        """
        Plot resonance intensity as a heatmap using node index and relative cycle strength.
        """
        if not self.resonance_map:
            raise RuntimeError("Resonance analysis not yet performed. Call analyze_resonance() first.")

        ids = list(self.resonance_map.keys())
        values = list(self.resonance_map.values())
        indices = np.arange(len(ids))

        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(indices, values, color="orangered")

        ax.set_title("Resonance Intensity Across Absolute Entities")
        ax.set_xlabel("Entity Index")
        ax.set_ylabel("Resonance Magnitude")
        ax.set_xticks(indices)
        ax.set_xticklabels([eid[:6] for eid in ids], rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.6)

        # Annotate each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.show()

    def get_resonance_report(self) -> Dict[str, float]:
        """
        Return a mapping of entity UUIDs to resonance strength for further analysis.
        """
        return self.resonance_map
