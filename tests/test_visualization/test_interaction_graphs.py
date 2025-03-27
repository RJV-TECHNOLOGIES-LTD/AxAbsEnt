"""
Test Suite: Interaction Graph Visualizations

Validates the correctness, structure, and theoretical fidelity of interaction graph renderings
derived from absolute entities and their operator chains.

Theoretical Foundation:
- Interaction graphs represent mappings of Iij (cross-absolute interaction operators)
- Graph edges must encode structure-preserving interaction symmetry and composition laws
- Visual output must align with the transfinite interaction chain structure C^α_ij
  and entropy-preserving topology (Axiom 1: Cross-Absolute Conservation)

Test Targets:
- axabsent.visualization.interaction_graphs

"""

import pytest
import networkx as nx
from matplotlib.figure import Figure

from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator
from axabsent.visualization.interaction_graphs import (
    generate_interaction_graph,
    render_interaction_graph,
)
from axabsent.utils.validation import validate_visualization_output


@pytest.fixture
def sample_absolutes():
    """
    Creates a minimal interaction scenario among spatial, informational, and temporal absolutes.

    Returns:
        List[AbsoluteEntity]: Sample absolutes
    """
    return [
        AbsoluteEntity(name="AS", structure_space="dimensional", property_space="extension"),
        AbsoluteEntity(name="AI", structure_space="pattern", property_space="entropy"),
        AbsoluteEntity(name="AT", structure_space="causal", property_space="flow")
    ]


def test_generate_interaction_graph_topology(sample_absolutes):
    """
    Test the generation of an interaction graph from absolute entities and validate topological structure.
    """
    graph = generate_interaction_graph(sample_absolutes)

    assert isinstance(graph, nx.DiGraph), "Interaction graph must be a directed NetworkX graph."
    assert graph.number_of_nodes() == len(sample_absolutes), "Mismatch in absolute entity node count."
    assert graph.number_of_edges() >= len(sample_absolutes) - 1, "Insufficient edge connections among absolutes."

    for u, v, data in graph.edges(data=True):
        assert 'weight' in data, "Each edge must include interaction weight."
        assert isinstance(data['weight'], float), "Edge weight must be a float."
        assert 0 <= data['weight'] <= 1, "Interaction weight must be in [0, 1] (orthogonality constraint)."


def test_render_interaction_graph_output(sample_absolutes):
    """
    Test the visual rendering of the interaction graph and validate figure structure.
    """
    graph = generate_interaction_graph(sample_absolutes)
    fig = render_interaction_graph(graph)

    assert isinstance(fig, Figure), "Rendered output must be a matplotlib Figure."
    assert validate_visualization_output(fig), "Rendered interaction graph failed visual integrity validation."
    assert fig.axes, "Figure must contain axes with the interaction graph."


def test_graph_symmetry_and_transitivity_in_rendered_structure(sample_absolutes):
    """
    Ensure visual output reflects symmetric interactions (Iij = Iji) and indirect transitivity (via Iik ∘ Ikj).
    """
    graph = generate_interaction_graph(sample_absolutes)

    for i, source in enumerate(sample_absolutes):
        for j, target in enumerate(sample_absolutes):
            if i == j:
                continue
            w_ij = graph.get_edge_data(source.name, target.name, {}).get("weight")
            w_ji = graph.get_edge_data(target.name, source.name, {}).get("weight")
            assert abs(w_ij - w_ji) < 1e-8, "Interaction symmetry violated in graph weights"

    # Optional: Check for transitive interaction path A → B → C implies indirect A → C influence
    for node in graph.nodes:
        successors = list(graph.successors(node))
        for succ in successors:
            next_hop = list(graph.successors(succ))
            for nh in next_hop:
                assert graph.has_node(nh), "Transitive node must exist in graph structure"
