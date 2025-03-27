# tests/test_simulation/test_vacuum_energy.py

import numpy as np
import pytest
from axabsent.simulation.vacuum_energy import VacuumEnergySimulation
from axabsent.core.absolute import AbsoluteEntity
from axabsent.core.mediator import MediatorSpace

def create_identity_entity(dim: int = 3) -> AbsoluteEntity:
    return AbsoluteEntity(signature=np.eye(dim))

def create_identity_mediator(dim: int = 3) -> MediatorSpace:
    return MediatorSpace(dimension=dim, curvature_tensor=np.eye(dim))

def test_vacuum_energy_simulation_initialization():
    """Ensure simulation initializes with a valid mediator and entities."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = VacuumEnergySimulation([entity], mediator, fluctuation_range=(0.01, 0.05))
    assert isinstance(sim, VacuumEnergySimulation)
    assert sim.fluctuation_range == (0.01, 0.05)

def test_generate_fluctuation_spectrum_output_shape():
    """Check that the fluctuation spectrum is a 1D array of expected length."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = VacuumEnergySimulation([entity], mediator, fluctuation_range=(0.01, 0.05))
    spectrum = sim.generate_fluctuation_spectrum(samples=100)
    assert spectrum.shape == (100,)
    assert np.all(np.isfinite(spectrum))

def test_compute_energy_density_tensor_shape_and_values():
    """Ensure energy density tensor is finite and dimensionally correct."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = VacuumEnergySimulation([entity], mediator, fluctuation_range=(0.01, 0.05))
    tensor = sim.compute_energy_density_tensor()
    assert tensor.shape == (3, 3)
    assert np.all(np.isfinite(tensor))

def test_phase_evolution_returns_valid_matrix():
    """Verify that the computed phase evolution is a finite matrix of shape (3, 3)."""
    entity = create_identity_entity()
    mediator = create_identity_mediator()
    sim = VacuumEnergySimulation([entity], mediator, fluctuation_range=(0.01, 0.05))
    phase = sim.compute_phase_evolution()
    assert phase.shape == (3, 3)
    assert np.all(np.isfinite(phase))

