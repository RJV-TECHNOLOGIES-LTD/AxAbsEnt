// web/tests/components/ResultsAnalyzer.test.js

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ResultsAnalyzer from '../../src/components/ResultsAnalyzer';
import * as api from '../../src/services/api';

jest.mock('../../src/services/api');

describe('ResultsAnalyzer Component', () => {
  const mockResponse = {
    entropy_distribution: [0.1, 0.3, 0.5, 0.4, 0.2],
    resonance_peaks: [0.55, 0.89],
    stability_index: 0.91,
    image_base64: "data:image/png;base64,ANALYSIS_IMAGE"
  };

  beforeEach(() => {
    api.analyzeResults.mockResolvedValue(mockResponse);
  });

  it('renders result upload and analysis options', () => {
    render(<ResultsAnalyzer />);
    expect(screen.getByLabelText(/Result Data JSON/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Analyze/i })).toBeInTheDocument();
  });

  it('submits result data and shows analysis output', async () => {
    render(<ResultsAnalyzer />);

    const textarea = screen.getByLabelText(/Result Data JSON/i);
    fireEvent.change(textarea, {
      target: {
        value: JSON.stringify({
          output_tensor: [[1.0, 0.2], [0.2, 1.1]],
          resonance_vector: [0.1, 0.3, 0.5]
        })
      }
    });

    fireEvent.click(screen.getByRole('button', { name: /Analyze/i }));

    await waitFor(() =>
      expect(screen.getByText(/Stability Index: 0.91/i)).toBeInTheDocument()
    );

    expect(screen.getByAltText(/Analysis Visualization/i)).toHaveAttribute(
      'src',
      expect.stringContaining('ANALYSIS_IMAGE')
    );
    expect(screen.getByText(/Entropy Distribution/i)).toBeInTheDocument();
    expect(screen.getByText(/Resonance Peaks/i)).toBeInTheDocument();
  });

  it('handles malformed analysis data gracefully', async () => {
    render(<ResultsAnalyzer />);

    fireEvent.change(screen.getByLabelText(/Result Data JSON/i), {
      target: { value: 'incomplete json' }
    });

    fireEvent.click(screen.getByRole('button', { name: /Analyze/i }));

    expect(await screen.findByText(/Invalid result data/i)).toBeInTheDocument();
  });
});

