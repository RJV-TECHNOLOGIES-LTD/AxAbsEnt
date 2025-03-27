// web/tests/components/ForceExplorer.test.js

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ForceExplorer from '../../src/components/ForceExplorer';
import * as api from '../../src/services/api';

jest.mock('../../src/services/api');

describe('ForceExplorer Component', () => {
  const tensor = [
    [1.0, 0.1, 0.0],
    [0.1, 1.2, 0.2],
    [0.0, 0.2, 0.9]
  ];

  const mockResponse = {
    image_base64: 'data:image/png;base64,FAKE_FORCE_IMAGE',
    metadata: {
      field_name: 'Gravitational'
    }
  };

  beforeEach(() => {
    api.visualizeForceField.mockResolvedValue(mockResponse);
  });

  it('renders force field selection and input form', () => {
    render(<ForceExplorer />);
    expect(screen.getByLabelText(/Force Tensor/i)).toBeInTheDocument();
    expect(screen.getByRole('combobox')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit/i })).toBeInTheDocument();
  });

  it('submits tensor and displays force field image', async () => {
    render(<ForceExplorer />);

    const textarea = screen.getByLabelText(/Force Tensor/i);
    const select = screen.getByRole('combobox');

    fireEvent.change(textarea, {
      target: { value: JSON.stringify(tensor) }
    });
    fireEvent.change(select, {
      target: { value: 'Gravitational' }
    });

    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));

    await waitFor(() =>
      expect(screen.getByAltText(/Gravitational Force Field/i)).toBeInTheDocument()
    );

    const img = screen.getByAltText(/Gravitational Force Field/i);
    expect(img).toHaveAttribute('src', expect.stringContaining('FAKE_FORCE_IMAGE'));
  });

  it('rejects invalid tensor input with user feedback', async () => {
    render(<ForceExplorer />);

    const textarea = screen.getByLabelText(/Force Tensor/i);
    fireEvent.change(textarea, {
      target: { value: 'invalid tensor' }
    });

    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));

    expect(await screen.findByText(/Invalid tensor format/i)).toBeInTheDocument();
  });
});

