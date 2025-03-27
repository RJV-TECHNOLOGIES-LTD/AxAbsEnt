// web/src/index.js

import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import App from "@components/App";
import InteractionVisualizer from "@components/InteractionVisualizer";
import ForceExplorer from "@components/ForceExplorer";
import SimulationRunner from "@components/SimulationRunner";
import ResultsAnalyzer from "@components/ResultsAnalyzer";
import "./styles/global.css";

// StrictMode enables debugging, validation, and lifecycle enforcement
const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<Navigate to="/visualizer" replace />} />
          <Route path="visualizer" element={<InteractionVisualizer />} />
          <Route path="forces" element={<ForceExplorer />} />
          <Route path="simulate" element={<SimulationRunner />} />
          <Route path="results" element={<ResultsAnalyzer />} />
          <Route path="*" element={<h2>404 – Page Not Found</h2>} />
        </Route>
      </Routes>
    </Router>
  </React.StrictMode>
);
