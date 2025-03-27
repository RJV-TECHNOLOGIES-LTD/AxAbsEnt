// web/tests/components/SimulationRunner.test.js

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SimulationRunner from '../../src/components/SimulationRunner';
import * as api from '../../src/services/api';

jest.mock('../../src/services/api');

describe('SimulationRunner Component', () => {
  const mockResponse = {
    expansion_tensor: [[1.1, 0.1], [0.1, 0.9]],
    structure_map: [0.8, 0.6, 0.7],
    simulation_id: "SIM123456"
  };

  beforeEach(() => {
    api.runSimulation.mockResolvedValue(mockResponse);
  });

  it('renders simulation form with fields', () => {
    render(<SimulationRunner />);
    expect(screen.getByLabelText(/Simulation Type/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Parameters/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Run Simulation/i })).toBeInTheDocument();
  });

  it('runs simulation and displays results', async () => {
    render(<SimulationRunner />);

    const typeSelect = screen.getByLabelText(/Simulation Type/i);
    const paramField = screen.getByLabelText(/Parameters/i);

    fireEvent.change(typeSelect, { target: { value: 'cosmological' } });
    fireEvent.change(paramField, {
      target: {
        value: JSON.stringify({
          initial_scale: 1.0,
          steps: 3,
          dimension: 2
        })
      }
    });

    fireEvent.click(screen.getByRole('button', { name: /Run Simulation/i }));

    await waitFor(() =>
      expect(screen.getByText(/Simulation ID: SIM123456/i)).toBeInTheDocument()
    );

    expect(screen.getByText(/Expansion Tensor/i)).toBeInTheDocument();
    expect(screen.getByText(/Structure Map/i)).toBeInTheDocument();
  });

  it('shows error message on invalid JSON', async () => {
    render(<SimulationRunner />);

    fireEvent.change(screen.getByLabelText(/Parameters/i), {
      target: { value: "{invalid_json: true" }
    });

    fireEvent.click(screen.getByRole('button', { name: /Run Simulation/i }));

    expect(await screen.findByText(/Invalid parameter format/i)).toBeInTheDocument();
  });
});

