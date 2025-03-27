import pytest
import numpy as np
from axabsent.core.absolute import create_absolute
from axabsent.core.interaction import create_interaction_operator, apply_interaction
from axabsent.core.mediator import create_mediator_space
from axabsent.forces.extraction import extract_forces_from_interactions
from axabsent.simulation.dynamics import run_dynamical_simulation
from axabsent.visualization.force_fields import generate_force_map_image

def test_full_axabsent_pipeline():
    """
    Full AxAbsEnt model pipeline integration test.
    Ensures that absolutes, interaction, force emergence, and simulation chain operate together.
    """

    # Step 1: Define Absolutes
    A_spatial = create_absolute("Spatial")
    A_temporal = create_absolute("Temporal")
    A_informational = create_absolute("Informational")

    assert A_spatial.name == "Spatial"
    assert A_temporal.structure_space.dim > 0

    # Step 2: Create Interactions
    I_st = create_interaction_operator(A_spatial, A_temporal)
    I_ti = create_interaction_operator(A_temporal, A_informational)

    interaction_result = apply_interaction(I_st, A_spatial.structure_sample(), A_temporal.structure_sample())
    assert "interaction_strength" in interaction_result

    # Step 3: Mediator Space Validation
    M_space = create_mediator_space(A_spatial, A_informational)
    assert M_space.is_valid()

    # Step 4: Force Extraction
    forces = extract_forces_from_interactions([I_st, I_ti])
    assert "gravity" in forces
    assert isinstance(forces["gravity"], np.ndarray)
    assert forces["gravity"].shape == (4, 4)

    # Step 5: Run Simulation
    sim_config = {
        "initial_forces": forces,
        "steps": 100,
        "space_grid": (64, 64)
    }

    sim_output = run_dynamical_simulation(sim_config)
    assert "field_state" in sim_output
    assert sim_output["field_state"].shape == (100, 64, 64)

    # Step 6: Visualization Generation
    img_array = generate_force_map_image(forces["gravity"])
    assert isinstance(img_array, np.ndarray)
    assert img_array.shape[-1] == 3  # RGB image

