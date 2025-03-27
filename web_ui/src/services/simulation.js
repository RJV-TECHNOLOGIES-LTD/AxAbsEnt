// web/src/services/simulation.js

import { runSimulation } from './api';
import { formatEntropy, formatTime } from '../utils/formatters';
import { STATUS_MESSAGES } from '../utils/constants';

/**
 * Prepare and execute a simulation given current UI configuration.
 * @param {Array<string>} entityIds - Absolute Entity IDs
 * @param {string} interactionId - Interaction ID between entities
 * @param {function} onProgress - Callback for live status updates
 * @returns {Promise<Object>} - Formatted result package
 */
export async function executeSimulation(entityIds, interactionId, onProgress = () => {}) {
  if (!Array.isArray(entityIds) || entityIds.length === 0 || typeof interactionId !== 'string') {
    throw new Error('Invalid simulation parameters.');
  }

  onProgress(STATUS_MESSAGES.SIMULATION_RUNNING);

  const config = {
    config: {
      entities: entityIds,
      interaction: interactionId
    }
  };

  const start = Date.now();
  try {
    const result = await runSimulation(config);
    const end = Date.now();

    return {
      success: result.success || false,
      entropy: formatEntropy(result.entropy),
      curvatureFlux: result.curvatureFlux || [],
      raw: result,
      runtime: formatTime(end - start),
      debug: {
        input: config,
        response: result
      }
    };
  } catch (error) {
    onProgress(`Simulation failed: ${error.message}`);
    return {
      success: false,
      error: error.message,
      entropy: '—',
      curvatureFlux: [],
      runtime: '—'
    };
  }
}
