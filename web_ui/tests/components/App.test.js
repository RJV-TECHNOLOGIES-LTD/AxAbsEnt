// web/tests/components/App.test.js

import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/components/App';

describe('AxAbsEnt App Component', () => {
  test('renders without crashing and shows title', () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );
    const title = screen.getByText(/AxAbsEnt/i);
    expect(title).toBeInTheDocument();
  });

  test('renders main navigation links', () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText(/Interactions/i)).toBeInTheDocument();
    expect(screen.getByText(/Simulation/i)).toBeInTheDocument();
    expect(screen.getByText(/Forces/i)).toBeInTheDocument();
  });

  test('initial route loads InteractionVisualizer by default', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('interaction-visualizer')).toBeInTheDocument();
  });

  test('routing to /simulation loads SimulationRunner', () => {
    render(
      <MemoryRouter initialEntries={['/simulation']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('simulation-runner')).toBeInTheDocument();
  });

  test('routing to /forces loads ForceExplorer', () => {
    render(
      <MemoryRouter initialEntries={['/forces']}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId('force-explorer')).toBeInTheDocument();
  });

  test('supports multilingual labels (i18n)', () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );
    // Expect one i18n label as rendered; assumes i18n default is English
    expect(screen.getByText(/Unified Physics Interface/i)).toBeInTheDocument();
  });
});
