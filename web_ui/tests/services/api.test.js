// web/tests/services/api.test.js

import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import { getAbsoluteEntities, createInteraction, runSimulation } from '../../src/services/api';

describe('AxAbsEnt API Service', () => {
  let mock;

  beforeAll(() => {
    mock = new MockAdapter(axios);
  });

  afterEach(() => {
    mock.reset();
  });

  afterAll(() => {
    mock.restore();
  });

  it('should fetch absolute entities successfully', async () => {
    const mockResponse = [
      { id: 'abs-1', signature: [[1]], properties: { mass: 1.0 } },
      { id: 'abs-2', signature: [[1]], properties: { charge: -1.0 } }
    ];

    mock.onGet('/api/absolute').reply(200, mockResponse);

    const result = await getAbsoluteEntities();
    expect(result).toHaveLength(2);
    expect(result[0].id).toBe('abs-1');
    expect(result[1].properties.charge).toBe(-1.0);
  });

  it('should create a new interaction between absolutes', async () => {
    const interactionPayload = {
      sourceId: 'abs-1',
      targetId: 'abs-2',
      operatorType: 'entanglement'
    };

    const responsePayload = {
      interactionId: 'int-101',
      status: 'initialized'
    };

    mock.onPost('/api/interaction').reply(config => {
      const data = JSON.parse(config.data);
      expect(data.operatorType).toBe('entanglement');
      return [200, responsePayload];
    });

    const result = await createInteraction(interactionPayload);
    expect(result.status).toBe('initialized');
  });

  it('should handle simulation run and return expected metrics', async () => {
    const simulationInput = {
      config: {
        entities: ['abs-1', 'abs-2'],
        interaction: 'int-101'
      }
    };

    const simulationOutput = {
      success: true,
      entropy: 0.041,
      curvatureFlux: [0.0001, 0.0003],
      timeElapsed: 120
    };

    mock.onPost('/api/simulation/run').reply(200, simulationOutput);

    const result = await runSimulation(simulationInput);
    expect(result.success).toBe(true);
    expect(result.entropy).toBeGreaterThan(0);
    expect(result.curvatureFlux).toHaveLength(2);
  });

  it('should return error on network failure', async () => {
    mock.onGet('/api/absolute').networkError();

    await expect(getAbsoluteEntities()).rejects.toThrow('Network Error');
  });

  it('should timeout if API takes too long', async () => {
    mock.onPost('/api/simulation/run').timeout();

    await expect(
      runSimulation({ config: { entities: ['abs-1'], interaction: 'int-x' } })
    ).rejects.toThrow(/timeout/i);
  });
});
