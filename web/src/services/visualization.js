// web/src/services/visualization.js

import { FORCE_COLORS } from '../utils/constants';
import { formatNumber } from '../utils/formatters';

/**
 * Generate nodes and edges for an interaction graph layout.
 * @param {Array<Object>} absolutes - List of absolute entities.
 * @param {Array<Object>} interactions - List of interactions between them.
 * @returns {{ nodes: Array, edges: Array }}
 */
export function buildInteractionGraph(absolutes, interactions) {
  const nodes = absolutes.map(entity => ({
    id: entity.id,
    label: `𝔄-${entity.id.slice(0, 6).toUpperCase()}`,
    properties: entity.properties,
    signature: entity.signature,
    color: '#8884d8'
  }));

  const edges = interactions.map(interaction => ({
    id: interaction.interactionId,
    source: interaction.sourceId,
    target: interaction.targetId,
    label: interaction.operatorType.toUpperCase(),
    color: '#82ca9d'
  }));

  return { nodes, edges };
}

/**
 * Generate a 2D force field heatmap representation.
 * @param {Array<number>} curvatureFlux - Output from simulation.
 * @param {number} resolution - Number of points along each axis.
 * @returns {{ x: Array<number>, y: Array<number>, z: Array<Array<number>> }}
 */
export function buildForceFieldMap(curvatureFlux, resolution = 25) {
  const x = Array.from({ length: resolution }, (_, i) => i / resolution);
  const y = Array.from({ length: resolution }, (_, i) => i / resolution);
  const z = [];

  for (let i = 0; i < resolution; i++) {
    const row = [];
    for (let j = 0; j < resolution; j++) {
      const fluxValue = curvatureFlux[(i * resolution + j) % curvatureFlux.length] || 0;
      row.push(fluxValue);
    }
    z.push(row);
  }

  return { x, y, z };
}

/**
 * Map force type to color used in all visual plots.
 * @param {string} forceType
 * @returns {string}
 */
export function getForceColor(forceType) {
  return FORCE_COLORS[forceType.toUpperCase()] || '#CCCCCC';
}

/**
 * Generate entropy map for information flow visualizations.
 * @param {Array<number>} entropyArray - Raw scalar entropy across a region.
 * @param {number} width
 * @param {number} height
 * @returns {Array<Array<number>>}
 */
export function buildEntropyMap(entropyArray, width = 10, height = 10) {
  const matrix = [];
  let i = 0;
  for (let y = 0; y < height; y++) {
    const row = [];
    for (let x = 0; x < width; x++) {
      const value = entropyArray[i++] ?? 0;
      row.push(Number.parseFloat(value.toFixed(5)));
    }
    matrix.push(row);
  }
  return matrix;
}

/**
 * Format visualization tooltip content from raw data.
 * @param {Object} nodeOrEdge
 * @returns {string}
 */
export function formatTooltip(nodeOrEdge) {
  if (!nodeOrEdge) return '';
  const lines = [];
  for (const [key, value] of Object.entries(nodeOrEdge)) {
    if (typeof value === 'number') {
      lines.push(`${key}: ${formatNumber(value)}`);
    } else if (typeof value === 'string') {
      lines.push(`${key}: ${value}`);
    } else if (Array.isArray(value)) {
      lines.push(`${key}: [${value.length} values]`);
    }
  }
  return lines.join('\n');
}
