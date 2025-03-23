// web/tests/components/InteractionVisualizer.test.js

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import InteractionVisualizer from '../../src/components/InteractionVisualizer';
import * as api from '../../src/services/api';

jest.mock('../../src/services/api');

describe('InteractionVisualizer Component', () => {
  const mockData = {
    nodes: ['A', 'B', 'C'],
    edges: [
      { source: 'A', target: 'B', weight: 0.8 },
      { source: 'B', target: 'C', weight: 0.6 }
    ]
  };

  const mockResponse = {
    image_base64: 'data:image/png;base64,FAKE_IMAGE_DATA',
    type: 'interaction_graph'
  };

  beforeEach(() => {
    api.visualizeInteraction.mockResolvedValue(mockResponse);
  });

  it('renders upload form and submit button', () => {
    render(<InteractionVisualizer />);
    expect(screen.getByText(/Visualize Interaction/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit/i })).toBeInTheDocument();
  });

  it('submits data and renders result image', async () => {
    render(<InteractionVisualizer />);

    const textarea = screen.getByLabelText(/Interaction JSON/i);
    fireEvent.change(textarea, {
      target: { value: JSON.stringify(mockData) }
    });

    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));

    await waitFor(() =>
      expect(screen.getByAltText(/Interaction Graph/i)).toBeInTheDocument()
    );

    const img = screen.getByAltText(/Interaction Graph/i);
    expect(img).toHaveAttribute('src', expect.stringContaining('FAKE_IMAGE_DATA'));
  });

  it('handles malformed JSON input gracefully', async () => {
    render(<InteractionVisualizer />);

    const textarea = screen.getByLabelText(/Interaction JSON/i);
    fireEvent.change(textarea, {
      target: { value: "{invalid_json: true" }
    });

    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));

    expect(await screen.findByText(/Invalid JSON format/i)).toBeInTheDocument();
  });
});
