// web/src/components/ForceExplorer.js

import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import axios from "axios";
import "./ForceExplorer.css";

const ForceExplorer = () => {
  const [fieldData, setFieldData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [forceType, setForceType] = useState("gravity");

  useEffect(() => {
    fetchForceField(forceType);
  }, [forceType]);

  const fetchForceField = async (type) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/forces/field?type=${type}`);
      setFieldData(response.data);
    } catch (error) {
      console.error("Failed to fetch force field data:", error);
    } finally {
      setLoading(false);
    }
  };

  const renderFieldPlot = () => {
    if (!fieldData) return null;

    const { X, Y, U, V } = fieldData;

    return (
      <Plot
        data={[
          {
            type: "scatter",
            mode: "lines",
            x: X.flat(),
            y: Y.flat(),
            line: { color: "rgba(0,0,0,0.2)" },
            hoverinfo: "skip",
            showlegend: false,
          },
          {
            type: "quiver",
            x: X.flat(),
            y: Y.flat(),
            u: U.flat(),
            v: V.flat(),
            scale: 0.2,
            line: { width: 1, color: "blue" },
            name: `${forceType} vector field`,
          },
        ]}
        layout={{
          title: `Emergent Force Field: ${forceType.toUpperCase()}`,
          xaxis: { title: "X", zeroline: false },
          yaxis: { title: "Y", zeroline: false },
          width: 700,
          height: 600,
          showlegend: false,
        }}
        config={{ responsive: true }}
      />
    );
  };

  return (
    <div className="force-explorer">
      <h2>Force Explorer</h2>
      <div className="force-selector">
        <label>Select Force Type:</label>
        <select value={forceType} onChange={(e) => setForceType(e.target.value)}>
          <option value="gravity">Gravity</option>
          <option value="electromagnetic">Electromagnetic</option>
          <option value="strong">Strong</option>
          <option value="weak">Weak</option>
        </select>
      </div>
      {loading ? <p>Loading field...</p> : renderFieldPlot()}
    </div>
  );
};

export default ForceExplorer;
