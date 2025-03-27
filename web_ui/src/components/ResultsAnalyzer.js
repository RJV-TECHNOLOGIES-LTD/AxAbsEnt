// web/src/components/ResultsAnalyzer.js

import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import "./ResultsAnalyzer.css";

const ResultsAnalyzer = () => {
  const [resultsList, setResultsList] = useState([]);
  const [selectedResult, setSelectedResult] = useState(null);
  const [plotData, setPlotData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAvailableResults();
  }, []);

  const fetchAvailableResults = async () => {
    try {
      const response = await axios.get("/api/simulation/results");
      setResultsList(response.data.files || []);
    } catch (error) {
      console.error("Failed to fetch results list:", error);
    }
  };

  const loadResultData = async (filename) => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/simulation/results/${filename}`);
      setSelectedResult(filename);
      setPlotData(response.data);
    } catch (error) {
      console.error("Failed to load result file:", error);
    } finally {
      setLoading(false);
    }
  };

  const renderPlot = () => {
    if (!plotData) return null;

    const { x, y, z, title } = plotData;

    return (
      <Plot
        data={[
          {
            type: "surface",
            x: x,
            y: y,
            z: z,
            colorscale: "Cividis",
          },
        ]}
        layout={{
          title: title || `Result: ${selectedResult}`,
          width: 800,
          height: 600,
          scene: {
            xaxis: { title: "X" },
            yaxis: { title: "Y" },
            zaxis: { title: "Metric" },
          },
        }}
        config={{ responsive: true }}
      />
    );
  };

  return (
    <div className="results-analyzer">
      <h2>Simulation Results Analyzer</h2>

      <div className="results-selector">
        <label>Select Result File:</label>
        <select
          onChange={(e) => loadResultData(e.target.value)}
          defaultValue=""
        >
          <option value="" disabled>Select a file...</option>
          {resultsList.map((file) => (
            <option key={file} value={file}>
              {file}
            </option>
          ))}
        </select>
      </div>

      <div className="result-plot">
        {loading ? <p>Loading result...</p> : renderPlot()}
      </div>
    </div>
  );
};

export default ResultsAnalyzer;
