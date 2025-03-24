// web/src/utils/formatters.js

/**
 * Format a numeric value with fixed decimal precision.
 * @param {number} value - The number to format.
 * @param {number} precision - Number of decimal places.
 * @returns {string}
 */
export function formatNumber(value, precision = 5) {
  if (isNaN(value)) return 'NaN';
  return Number.parseFloat(value).toFixed(precision);
}

/**
 * Format a timestamp (in milliseconds) into a human-readable time string.
 * @param {number} ms - Milliseconds.
 * @returns {string}
 */
export function formatTime(ms) {
  if (typeof ms !== 'number') return '–';
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const remaining = seconds % 60;
  return `${minutes}m ${remaining}s`;
}

/**
 * Format a small entropy value with units.
 * @param {number} entropy - Entropy scalar.
 * @returns {string}
 */
export function formatEntropy(entropy) {
  if (entropy === null || entropy === undefined) return '—';
  return `${formatNumber(entropy, 7)} 𝓗`;
}

/**
 * Convert a matrix (2D array) into a clean string representation.
 * @param {Array<Array<number>>} matrix
 * @returns {string}
 */
export function formatMatrix(matrix) {
  if (!Array.isArray(matrix)) return '—';
  return matrix.map(row =>
    row.map(cell => formatNumber(cell, 3)).join('\t')
  ).join('\n');
}

/**
 * Format absolute entity display name.
 * @param {Object} absolute
 * @returns {string}
 */
export function formatAbsoluteLabel(absolute) {
  if (!absolute || !absolute.id) return 'Unknown Absolute';
  return `𝔄-${absolute.id.slice(0, 6).toUpperCase()}`;
}

/**
 * Format interaction label based on operator type and involved absolutes.
 * @param {Object} interaction
 * @returns {string}
 */
export function formatInteractionLabel(interaction) {
  if (!interaction || !interaction.interactionId) return 'Unnamed Interaction';
  const { operatorType, sourceId, targetId } = interaction;
  const label = `${operatorType || 'Interaction'}`.toUpperCase();
  return `${label} [${sourceId?.slice(0, 4)} → ${targetId?.slice(0, 4)}]`;
}

/**
 * Capitalize the first letter of a string.
 * @param {string} s
 * @returns {string}
 */
export function capitalize(s) {
  if (typeof s !== 'string') return '';
  return s.charAt(0).toUpperCase() + s.slice(1);
}
