// web/src/components/InteractionVisualizer.js

import React, { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import axios from "axios";
import "./InteractionVisualizer.css";

const InteractionVisualizer = () => {
  const [data, setData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGraphData();
  }, []);

  const fetchGraphData = async () => {
    try {
      const response = await axios.get("/api/interactions/topology");
      setData(response.data);
    } catch (error) {
      console.error("Failed to fetch interaction graph:", error);
    } finally {
      setLoading(false);
    }
  };

  const nodeLabel = (node) => `
    <div>
      <strong>ID:</strong> ${node.id}<br/>
      <strong>Entropy:</strong> ${node.entropy.toFixed(4)}<br/>
      <strong>Signature Rank:</strong> ${node.signature_rank}
    </div>
  `;

  return (
    <div className="visualizer-container">
      <h2>Cross-Absolute Interaction Graph</h2>
      {loading ? (
        <p>Loading graph...</p>
      ) : (
        <ForceGraph2D
          graphData={data}
          nodeId="id"
          nodeLabel={nodeLabel}
          nodeAutoColorBy="group"
          linkDirectionalArrowLength={6}
          linkDirectionalArrowRelPos={0.6}
          linkLabel={(link) => link.label}
          width={window.innerWidth - 100}
          height={600}
        />
      )}
    </div>
  );
};

export default InteractionVisualizer;
