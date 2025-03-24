// web/src/services/api.js

import axios from 'axios';
import { API_BASE_URL, ROUTES, ERROR_CODES } from '../utils/constants';
import {
  isValidAbsoluteEntity,
  isValidInteractionPayload,
  isValidSimulationConfig
} from '../utils/validators';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000 // 10 seconds timeout
});

/**
 * Fetch all absolute entities from the backend.
 * @returns {Promise<Array>}
 */
export async function getAbsoluteEntities() {
  try {
    const response = await client.get(ROUTES.ABSOLUTES);
    return Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    handleError(error);
  }
}

/**
 * Create a new absolute entity.
 * @param {Object} absolute
 * @returns {Promise<Object>}
 */
export async function createAbsoluteEntity(absolute) {
  if (!isValidAbsoluteEntity(absolute)) {
    throw new Error('Invalid Absolute Entity format.');
  }
  try {
    const response = await client.post(ROUTES.ABSOLUTES, absolute);
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Create a new interaction between absolutes.
 * @param {Object} interactionPayload
 * @returns {Promise<Object>}
 */
export async function createInteraction(interactionPayload) {
  if (!isValidInteractionPayload(interactionPayload)) {
    throw new Error('Invalid Interaction Payload.');
  }
  try {
    const response = await client.post(ROUTES.INTERACTIONS, interactionPayload);
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Run a simulation based on selected absolutes and interactions.
 * @param {Object} simulationConfig
 * @returns {Promise<Object>}
 */
export async function runSimulation(simulationConfig) {
  if (!isValidSimulationConfig(simulationConfig.config)) {
    throw new Error('Invalid Simulation Configuration.');
  }
  try {
    const response = await client.post(ROUTES.SIMULATION_RUN, simulationConfig);
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Centralized API error handler.
 * @param {Object} error
 */
function handleError(error) {
  if (error.code === 'ECONNABORTED') {
    throw new Error(ERROR_CODES.TIMEOUT);
  }
  if (error.message === 'Network Error') {
    throw new Error(ERROR_CODES.NETWORK_ERROR);
  }
  if (error.response && error.response.data) {
    throw new Error(error.response.data.message || ERROR_CODES.INVALID_RESPONSE);
  }
  throw new Error('Unknown API error.');
}
