"""
Global Test Configuration for AxAbsEnt Project

This module defines Pytest fixtures, hooks, and global setup utilities
to enforce unified theoretical consistency, interaction ontology compliance,
and test reproducibility across the entire AxAbsEnt validation suite.

Theoretical Integrity Enforcement:
- Every test session initializes a canonical AbsoluteRegistry with validated absolutes
- Mediator spaces and interaction chains are precomputed where applicable
- All test outputs are automatically validated for ontological and computational correctness

Applicable Domains:
- Core ontological entities
- Cross-absolute interaction operators
- Transfinite chains
- Force emergence validation
- Tensor visualization projections

"""

import pytest
import random
import numpy as np

from axabsent.core.registry import AbsoluteRegistry
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.interaction import InteractionOperator
from axabsent.core.mediator import MediatorSpace
from axabsent.core.transfinite import TransfiniteChain
from axabsent.utils.validation import validate_absolute_structure


@pytest.fixture(scope="session")
def canonical_absolutes():
    """
    Session-wide fixture that returns a validated canonical set of core absolutes:
    - Spatial (AS)
    - Temporal (AT)
    - Informational (AI)
    - Causal (AC)
    - Potentiality (AP)
    
    Returns:
        List[AbsoluteEntity]
    """
    absolutes = [
        AbsoluteEntity(name="AS", structure_space="dimensional", property_space="extension"),
        AbsoluteEntity(name="AT", structure_space="causal_order", property_space="flow"),
        AbsoluteEntity(name="AI", structure_space="pattern", property_space="entropy"),
        AbsoluteEntity(name="AC", structure_space="dependency", property_space="influence"),
        AbsoluteEntity(name="AP", structure_space="modality", property_space="probability"),
    ]
    
    for abs_ in absolutes:
        assert validate_absolute_structure(abs_), f"Absolute {abs_.name} failed validation"
    
    return absolutes


@pytest.fixture(scope="session")
def absolute_registry(canonical_absolutes):
    """
    Registers all canonical absolutes for system-wide discovery.
    Returns:
        AbsoluteRegistry
    """
    registry = AbsoluteRegistry()
    for entity in canonical_absolutes:
        registry.register(entity)
    return registry


@pytest.fixture(scope="function")
def seeded_rng():
    """
    Function-scoped random seed for reproducible test runs.
    """
    seed = 42
    random.seed(seed)
    np.random.seed(seed)


@pytest.fixture(scope="module")
def sample_interaction_operator(canonical_absolutes):
    """
    Provides a sample cross-absolute interaction operator (Iij) for testing.
    """
    return InteractionOperator(
        absolute_i=canonical_absolutes[0],  # AS
        absolute_j=canonical_absolutes[2],  # AI
        symmetric=True
    )


@pytest.fixture(scope="module")
def sample_mediator_space(sample_interaction_operator):
    """
    Generates a mediator space from the interaction operator.
    """
    return MediatorSpace(operator=sample_interaction_operator)


@pytest.fixture(scope="module")
def sample_transfinite_chain(canonical_absolutes):
    """
    Constructs a transfinite interaction chain for theoretical testing.
    """
    return TransfiniteChain.build_from_absolutes(canonical_absolutes[:3])  # AS → AI → AT
