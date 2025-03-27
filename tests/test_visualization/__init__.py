"""
AxAbsEnt Visualization Test Initialization Module

This module initializes the test suite for the visualization subpackage.
It sets up the test environment, enforces theoretical compliance with the 
Enhanced Mathematical Ontology of Absolute Nothingness, and configures test-level
assertions for all static and dynamic rendering operations.

Theoretical Foundations:
- Each visualization function must map to a projection from a cross-absolute interaction operator
  (e.g., interaction Iij projected to force field F_k via E_Fk)
- All visual outputs must be empirically or ontologically traceable to components defined in the
  unified interaction framework (mediator spaces, transfinite chains, force decompositions)

Test Domains:
- Force Field Topologies (∂F/∂X projections)
- Information Flow Networks (Tij ∘ Pk)
- Transfinite Visualization Validity (limit ordinal chain convergence)
- Tensor Field Mapping (force signature contributions: σ⃗i → Fk)
- Quantum Visualization Consistency (entanglement projection fidelity)

"""

from typing import List
import pytest

from axabsent.visualization import (
    force_fields,
    interaction_graphs,
    multidimensional,
    information_flow,
    entropy_maps,
)

from axabsent.core.absolute import AbsoluteEntity
from axabsent.forces.extraction import extract_force_field
from axabsent.simulation.base import SimulationContext
from axabsent.utils.validation import validate_visualization_output
from axabsent.utils.constants import FORCE_SPACES

# Global constant: all visual modules must align to at least one ontological projection rule
ONTOLOGICAL_COMPLIANCE_REQUIRED = True

@pytest.fixture(scope="session", autouse=True)
def validate_visualization_modules():
    """
    Auto-executed fixture that ensures all visualization modules conform to the unified theory projections.
    Raises AssertionError if any visual module lacks projection lineage.
    """
    visualization_modules = [
        force_fields,
        interaction_graphs,
        multidimensional,
        information_flow,
        entropy_maps,
    ]

    for module in visualization_modules:
        assert hasattr(module, "__theoretical_projection__"), \
            f"Module {module.__name__} lacks `__theoretical_projection__` attribute."
        assert callable(module.__theoretical_projection__), \
            f"Module {module.__name__} must define `__theoretical_projection__()` to establish traceability."

    yield

def test_visualization_environment_sanity():
    """
    Verifies basic test harness integrity and AxAbsEnt visualization environment initialization.
    """
    assert ONTOLOGICAL_COMPLIANCE_REQUIRED is True
    assert FORCE_SPACES is not None
    assert isinstance(FORCE_SPACES, dict)
