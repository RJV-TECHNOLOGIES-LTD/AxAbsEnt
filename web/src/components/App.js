// web/src/components/App.js

import React from "react";
import { Outlet, NavLink } from "react-router-dom";
import "./App.css";

const App = () => {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">AxAbsEnt – Cross-Absolute Execution Engine</h1>
        <nav className="app-nav">
          <NavLink to="/visualizer" activeclassname="active">Interactions</NavLink>
          <NavLink to="/forces" activeclassname="active">Forces</NavLink>
          <NavLink to="/simulate" activeclassname="active">Simulate</NavLink>
          <NavLink to="/results" activeclassname="active">Results</NavLink>
        </nav>
      </header>

      <main className="app-main">
        <Outlet />
      </main>

      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} RJV Technologies Ltd. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
