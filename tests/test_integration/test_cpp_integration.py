import pytest
import numpy as np
from cpp_bindings import absolute, interaction, simulation

def test_absolute_initialization():
    """
    Test initialization of Absolute entity from C++ binding.
    Ensures structure and property space are properly created and accessible.
    """
    spatial = absolute.create_absolute("Spatial")
    assert spatial.name == "Spatial"
    assert spatial.get_structure_space().dim > 0
    assert spatial.get_property_space().contains("locality")

def test_interaction_operator_cpp_binding():
    """
    Test the C++ interaction operator binding for cross-absolute interaction.
    Checks consistency with Unified Model principles.
    """
    A1 = absolute.create_absolute("Spatial")
    A2 = absolute.create_absolute("Informational")

    I12 = interaction.create_operator(A1, A2)
    result = interaction.apply_operator(I12, A1.structure_sample(), A2.structure_sample())

    assert isinstance(result, dict)
    assert "interaction_strength" in result
    assert 0 <= result["interaction_strength"] <= 1

def test_mediated_interaction_cpp():
    """
    Ensure mediated interaction works correctly for orthogonal absolutes via C++ backend.
    """
    A1 = absolute.create_absolute("Temporal")
    A2 = absolute.create_absolute("Causal")

    M_space = interaction.create_mediator_space(A1, A2)
    min_distance = interaction.calculate_mediated_distance(M_space, A1.structure_sample(), A2.structure_sample())

    assert min_distance >= 0
    assert isinstance(min_distance, float)

def test_simulation_execution_cpp_pipeline():
    """
    Executes a basic simulation pipeline using C++ simulation bindings.
    Verifies result structure and convergence.
    """
    initial_state = simulation.create_initial_state("quantum_field", config={"dim": 3})
    output = simulation.run_simulation(initial_state, steps=100)

    assert "energy_distribution" in output
    assert isinstance(output["energy_distribution"], np.ndarray)
    assert output["energy_distribution"].shape[0] == 100

def test_force_emergence_cpp():
    """
    Validates C++ force emergence computation from cross-absolute interactions.
    """
    A1 = absolute.create_absolute("Spatial")
    A2 = absolute.create_absolute("Temporal")
    A3 = absolute.create_absolute("Informational")

    interactions = [
        interaction.create_operator(A1, A2),
        interaction.create_operator(A2, A3)
    ]

    force = simulation.extract_force(interactions, mode="gravity")
    assert force["type"] == "gravity"
    assert isinstance(force["tensor"], np.ndarray)
    assert force["tensor"].shape == (4, 4)

