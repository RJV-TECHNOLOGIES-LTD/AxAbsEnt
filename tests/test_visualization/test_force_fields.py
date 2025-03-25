"""
Test Suite: Force Field Visualizations

Validates the accuracy, ontological traceability, and rendering consistency of force field visualizations
derived from cross-absolute interactions.

Theoretical Basis:
- All rendered force fields must arise from a projection of Iij (interaction operator) via EFk (force extraction)
- Visualization must reflect σ⃗i contribution signatures and mediator chain influence (transfinite damping valid)
- Force fields must visually encode topological characteristics (e.g., curvature from absolute chains)

Modules Tested:
- axabsent.visualization.force_fields

"""

import pytest
import numpy as np
from matplotlib.figure import Figure

from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator
from axabsent.forces.extraction import extract_force_field
from axabsent.visualization.force_fields import render_force_field_vector_map, render_force_field_density_map
from axabsent.simulation.base import SimulationContext
from axabsent.utils.validation import validate_visualization_output
from axabsent.utils.constants import FORCE_SPACES


def generate_dummy_force_field(dim: int = 2, resolution: int = 20) -> np.ndarray:
    """
    Generate a synthetic but theory-aligned force field for testing visualization routines.
    Simulates a spatial-temporal informational interaction signature.

    Returns:
        np.ndarray: shape (resolution, resolution, dim)
    """
    x = np.linspace(-1, 1, resolution)
    y = np.linspace(-1, 1, resolution)
    X, Y = np.meshgrid(x, y)
    Fx = -Y * np.exp(-X**2 - Y**2)
    Fy = X * np.exp(-X**2 - Y**2)
    return np.stack([Fx, Fy], axis=-1)


@pytest.mark.parametrize("field_generator", [generate_dummy_force_field])
def test_vector_map_rendering(field_generator):
    """
    Test vector map rendering of a theoretical force field and validate output integrity.
    """
    force_field = field_generator()
    fig = render_force_field_vector_map(force_field)

    assert isinstance(fig, Figure), "Output must be a matplotlib Figure."
    assert validate_visualization_output(fig), "Rendered figure failed validation."
    assert fig.axes, "Figure must contain axes with vector fields."


@pytest.mark.parametrize("field_generator", [generate_dummy_force_field])
def test_density_map_rendering(field_generator):
    """
    Test density map rendering of a theoretical force field and validate output integrity.
    """
    force_field = field_generator()
    fig = render_force_field_density_map(force_field)

    assert isinstance(fig, Figure), "Output must be a matplotlib Figure."
    assert validate_visualization_output(fig), "Rendered density figure failed validation."
    assert fig.axes, "Figure must contain axes with density overlay."


def test_force_field_projection_theoretical_alignment():
    """
    Ensure force field visualizations derive from valid absolute interaction projections.
    """
    A_spatial = AbsoluteEntity(name="AS", structure_space="dimensional", property_space="extension")
    A_info = AbsoluteEntity(name="AI", structure_space="pattern", property_space="entropy")

    interaction = InteractionOperator(A_spatial, A_info)
    force_tensor = extract_force_field(interaction, force_type="gravity")

    fig = render_force_field_vector_map(force_tensor.data)
    assert validate_visualization_output(fig), "Projection of absolute interaction did not render correctly."

