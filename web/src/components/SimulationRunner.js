// web/src/components/SimulationRunner.js

import React, { useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import "./SimulationRunner.css";

const SimulationRunner = () => {
  const [loading, setLoading] = useState(false);
  const [simulationType, setSimulationType] = useState("transfinite_chain");
  const [result, setResult] = useState(null);

  const runSimulation = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post("/api/simulation/run", {
        type: simulationType,
        parameters: {
          resolution: 100,
          steps: 500,
        },
      });
      setResult(response.data);
    } catch (error) {
      console.error("Simulation failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const renderPlot = () => {
    if (!result || !result.data) return null;

    const { x, y, z, title } = result.data;

    return (
      <Plot
        data={[
          {
            type: "surface",
            x: x,
            y: y,
            z: z,
            colorscale: "Viridis",
          },
        ]}
        layout={{
          title: title || "Simulation Result Surface",
          scene: {
            xaxis: { title: "X" },
            yaxis: { title: "Y" },
            zaxis: { title: "Amplitude" },
          },
          autosize: true,
          width: 800,
          height: 600,
        }}
        config={{ responsive: true }}
      />
    );
  };

  return (
    <div className="simulation-runner">
      <h2>Simulation Runner</h2>

      <div className="sim-selector">
        <label>Select Simulation Type:</label>
        <select
          value={simulationType}
          onChange={(e) => setSimulationType(e.target.value)}
        >
          <option value="transfinite_chain">Transfinite Chain Dynamics</option>
          <option value="absolute_evolution">Absolute Entity Evolution</option>
          <option value="vacuum_fluctuation">Vacuum Fluctuation Mapping</option>
        </select>
        <button onClick={runSimulation} disabled={loading}>
          {loading ? "Running..." : "Run Simulation"}
        </button>
      </div>

      <div className="sim-result">{renderPlot()}</div>
    </div>
  );
};

export default SimulationRunner;
