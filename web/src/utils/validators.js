// web/src/utils/validators.js

/**
 * Validate a signature matrix (must be square, symmetric, and numeric).
 * @param {Array<Array<number>>} matrix
 * @returns {boolean}
 */
export function isValidSignatureMatrix(matrix) {
  if (!Array.isArray(matrix) || matrix.length === 0) return false;
  const n = matrix.length;
  return matrix.every(
    (row, i) =>
      Array.isArray(row) &&
      row.length === n &&
      row.every((cell, j) =>
        typeof cell === 'number' && (cell === matrix[j][i])
      )
  );
}

/**
 * Check that a given absolute entity has a valid structure.
 * @param {Object} entity
 * @returns {boolean}
 */
export function isValidAbsoluteEntity(entity) {
  if (!entity || typeof entity !== 'object') return false;
  const hasId = typeof entity.id === 'string';
  const hasSignature = isValidSignatureMatrix(entity.signature);
  return hasId && hasSignature;
}

/**
 * Validate interaction payload before submission.
 * @param {Object} payload
 * @returns {boolean}
 */
export function isValidInteractionPayload(payload) {
  if (!payload || typeof payload !== 'object') return false;
  const { sourceId, targetId, operatorType } = payload;
  return (
    typeof sourceId === 'string' &&
    typeof targetId === 'string' &&
    sourceId !== targetId &&
    typeof operatorType === 'string' &&
    operatorType.length > 0
  );
}

/**
 * Validate a simulation configuration before sending to backend.
 * @param {Object} config
 * @returns {boolean}
 */
export function isValidSimulationConfig(config) {
  if (!config || typeof config !== 'object') return false;
  const { entities, interaction } = config;
  return (
    Array.isArray(entities) &&
    entities.length > 0 &&
    entities.every(id => typeof id === 'string') &&
    typeof interaction === 'string'
  );
}

/**
 * Validate matrix dimensions for projection or tensor inputs.
 * @param {Array<Array<number>>} matrix
 * @param {number} expectedCols
 * @returns {boolean}
 */
export function isValidMatrixShape(matrix, expectedCols) {
  if (!Array.isArray(matrix)) return false;
  return matrix.every(row => Array.isArray(row) && row.length === expectedCols);
}

/**
 * Ensure input is a numeric scalar or vector (used in tensor config).
 * @param {any} value
 * @returns {boolean}
 */
export function isNumericInput(value) {
  if (typeof value === 'number') return true;
  if (Array.isArray(value)) return value.every(cell => typeof cell === 'number');
  return false;
}
