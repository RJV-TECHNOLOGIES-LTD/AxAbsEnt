# api/routes/simulation.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any
import numpy as np

from axabsent.simulation.dynamics import simulate_transfinite_chain
from axabsent.simulation.vacuum_energy import simulate_vacuum_field
from axabsent.simulation.base import simulate_absolute_evolution

router = APIRouter(prefix="/api/simulation", tags=["simulation"])

class SimulationRequest(BaseModel):
    type: Literal["transfinite_chain", "absolute_evolution", "vacuum_fluctuation"]
    parameters: Optional[Dict[str, Any]] = {}

@router.post("/run")
def run_simulation(request: SimulationRequest):
    """
    Runs a specified cross-absolute simulation and returns a surface plot dataset.
    Response format:
    {
        "data": {
            "x": [...],   // X-axis grid
            "y": [...],   // Y-axis grid
            "z": [[...]], // 2D surface metric
            "title": "Simulation Title"
        }
    }
    """
    sim_type = request.type
    params = request.parameters or {}
    resolution = int(params.get("resolution", 100))
    steps = int(params.get("steps", 300))

    x = np.linspace(-1, 1, resolution)
    y = np.linspace(-1, 1, resolution)
    X, Y = np.meshgrid(x, y)

    if sim_type == "transfinite_chain":
        Z = simulate_transfinite_chain(X, Y, steps=steps)
        title = "Transfinite Chain Dynamics"

    elif sim_type == "absolute_evolution":
        Z = simulate_absolute_evolution(X, Y, steps=steps)
        title = "Absolute Entity Evolution"

    elif sim_type == "vacuum_fluctuation":
        Z = simulate_vacuum_field(X, Y, fluctuation_scale=1.0)
        title = "Vacuum Fluctuation Map"

    else:
        raise HTTPException(status_code=400, detail="Invalid simulation type")

    return {
        "data": {
            "x": x.tolist(),
            "y": y.tolist(),
            "z": Z.tolist(),
            "title": title
        }
    }
