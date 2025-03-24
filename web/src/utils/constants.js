// web/src/utils/constants.js

export const API_BASE_URL = '/api';

export const ROUTES = {
  INTERACTIONS: '/interaction',
  ABSOLUTES: '/absolute',
  SIMULATION_RUN: '/simulation/run',
  FORCES: '/forces',
  VISUALIZATION: '/visualization'
};

export const FORCE_TYPES = {
  GRAVITY: 'Gravity',
  ELECTROMAGNETIC: 'Electromagnetic',
  STRONG: 'Strong Nuclear',
  WEAK: 'Weak Nuclear'
};

export const FORCE_COLORS = {
  GRAVITY: '#4B8BBE',           // Blue
  ELECTROMAGNETIC: '#E69F00',   // Orange
  STRONG: '#D55E00',            // Red
  WEAK: '#009E73'               // Green
};

export const INTERACTION_STATES = {
  INITIALIZED: 'initialized',
  ENTANGLED: 'entangled',
  COLLAPSED: 'collapsed',
  RESONANT: 'resonant',
  DECOHERED: 'decohered'
};

export const DIMENSIONS = {
  MAX_ABSOLUTE_DIM: 6,
  MIN_ABSOLUTE_DIM: 1
};

export const UI = {
  DEFAULT_LANGUAGE: 'en',
  SUPPORTED_LANGUAGES: ['en', 'fr', 'de'],
  PLOT_BG_COLOR: '#f7f7f7',
  PRECISION: 5,
  MAX_ABSOLUTE_ENTITIES: 100,
  MAX_SIMULATION_STEPS: 10000
};

export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  TIMEOUT: 'TIMEOUT',
  INVALID_RESPONSE: 'INVALID_RESPONSE'
};

export const STATUS_MESSAGES = {
  FETCHING_DATA: 'Fetching data from AxAbsEnt engine...',
  SIMULATION_RUNNING: 'Simulation in progress...',
  VISUALIZING_RESULTS: 'Rendering quantum curvature projection...',
  ERROR_OCCURRED: 'An error occurred. Please check console or logs.'
};
