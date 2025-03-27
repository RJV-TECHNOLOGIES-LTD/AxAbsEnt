# api/routes/simulation.py

from fastapi import APIRouter, HTTPException, Query, Path, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, Dict, Any, List, Union
import numpy as np
import os
import uuid
import time
from datetime import datetime

from api.errors import SimulationError, ResourceNotFoundError
from api.middleware.caching import cache_guard
from api.schemas.simulation import (
    SimulationRequest, 
    SimulationResponse,
    SimulationMetadata,
    SimulationResult,
    SimulationStatus
)

from axabsent.simulation.dynamics import simulate_transfinite_chain
from axabsent.simulation.vacuum_energy import simulate_vacuum_field
from axabsent.simulation.base import simulate_absolute_evolution
from axabsent.simulation.results import (
    save_simulation_result,
    list_simulation_results,
    load_simulation_result,
    delete_simulation_result
)

# Create router with proper prefix and tags
router = APIRouter(
    prefix="/api/simulation",
    tags=["simulation"],
    responses={
        404: {"description": "Simulation not found"},
        422: {"description": "Validation error in simulation parameters"},
        500: {"description": "Simulation processing error"}
    }
)

# Input validation models
class SimulationParameters(BaseModel):
    """Common simulation parameters"""
    resolution: int = Field(100, ge=10, le=1000, description="Grid resolution (points per dimension)")
    steps: int = Field(300, ge=1, le=10000, description="Number of simulation steps")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    
    class Config:
        schema_extra = {
            "example": {
                "resolution": 100,
                "steps": 300,
                "seed": 42
            }
        }

class EnhancedSimulationRequest(BaseModel):
    """Enhanced simulation request model with validation"""
    type: Literal["transfinite_chain", "absolute_evolution", "vacuum_fluctuation"]
    parameters: Optional[SimulationParameters] = Field(default_factory=SimulationParameters)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User-defined metadata")
    
    @validator('metadata')
    def validate_metadata(cls, v):
        if len(v) > 20:
            raise ValueError("Too many metadata fields (maximum 20)")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "type": "transfinite_chain",
                "parameters": {
                    "resolution": 100,
                    "steps": 300,
                    "seed": 42
                },
                "metadata": {
                    "user_reference": "experiment-123",
                    "description": "Testing phase transitions"
                }
            }
        }

# Background task to clean up old simulation results
async def cleanup_old_simulations():
    """Remove simulation results older than configured retention period"""
    files = list_simulation_results()
    # Implementation depends on how results are stored and timestamped
    # This is a placeholder

@router.post("/run", response_model=SimulationResponse)
@cache_guard
async def run_simulation(
    request: EnhancedSimulationRequest,
    background_tasks: BackgroundTasks,
):
    """
    Run a new simulation with the specified parameters.
    
    Returns the simulation results directly if fast enough,
    or a job ID to poll for completion on long-running jobs.
    
    Immutable results: Identical simulation parameters will return
    cached results to ensure ontological consistency.
    """
    # Schedule cleanup of old files
    background_tasks.add_task(cleanup_old_simulations)
    
    # Extract parameters with defaults
    sim_type = request.type
    params = request.parameters
    resolution = params.resolution
    steps = params.steps
    
    # Set random seed if provided
    if params.seed is not None:
        np.random.seed(params.seed)
    
    # Create coordinate grid
    x = np.linspace(-1, 1, resolution)
    y = np.linspace(-1, 1, resolution)
    X, Y = np.meshgrid(x, y)
    
    try:
        # Run the appropriate simulation
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
            # This should be caught by Pydantic validation, but just in case
            raise SimulationError(
                detail=f"Invalid simulation type: {sim_type}",
                simulation_type=sim_type,
                parameters=params.dict()
            )
    except Exception as e:
        # Catch computational errors
        raise SimulationError(
            detail=f"Simulation computation failed: {str(e)}",
            simulation_type=sim_type,
            parameters=params.dict()
        )
    
    # Prepare result data
    timestamp = datetime.utcnow().isoformat()
    simulation_id = str(uuid4())
    
    result_data = {
        "id": simulation_id,
        "timestamp": timestamp,
        "type": sim_type,
        "parameters": params.dict(),
        "metadata": request.metadata,
        "data": {
            "x": x.tolist(),
            "y": y.tolist(),
            "z": Z.tolist(),
            "title": title
        }
    }
    
    # Save result to storage
    filename = save_simulation_result(result_data, label=f"{sim_type}_{simulation_id}")
    
    return {
        "id": simulation_id,
        "type": sim_type,
        "status": "completed",
        "data": result_data["data"],
        "metadata": {
            "created_at": timestamp,
            "filename": filename,
            "parameters": params.dict()
        }
    }

@router.get("/results", response_model=List[SimulationMetadata])
async def get_simulation_results_list():
    """
    List all available simulation results with metadata.
    Results are sorted by creation date (newest first).
    """
    files = list_simulation_results()
    
    results = []
    for filename in files:
        try:
            data = load_simulation_result(filename)
            results.append({
                "id": data.get("id", filename),
                "type": data.get("type", "unknown"),
                "timestamp": data.get("timestamp", ""),
                "filename": filename,
                "title": data.get("data", {}).get("title", "Untitled Simulation"),
                "parameters": data.get("parameters", {})
            })
        except Exception:
            # Skip corrupted files
            continue
    
    # Sort by timestamp (newest first)
    results.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return results

@router.get("/results/{simulation_id}", response_model=SimulationResult)
async def get_simulation_result(
    simulation_id: str = Path(..., description="Simulation ID or filename")
):
    """
    Retrieve a specific simulation result by ID or filename.
    
    Returns the full simulation result data including grid values,
    parameters, and metadata.
    """
    try:
        # Try to load by ID first
        files = list_simulation_results()
        found = False
        
        for filename in files:
            try:
                data = load_simulation_result(filename)
                if data.get("id") == simulation_id or filename == simulation_id:
                    found = True
                    break
            except:
                continue
                
        if not found:
            raise ResourceNotFoundError(
                detail=f"Simulation result not found",
                resource_type="simulation",
                resource_id=simulation_id
            )
            
        return {
            "id": data.get("id", filename),
            "type": data.get("type", "unknown"),
            "status": "completed",
            "timestamp": data.get("timestamp", ""),
            "parameters": data.get("parameters", {}),
            "metadata": data.get("metadata", {}),
            "data": data.get("data", {})
        }
        
    except FileNotFoundError:
        raise ResourceNotFoundError(
            detail=f"Simulation result not found",
            resource_type="simulation",
            resource_id=simulation_id
        )

@router.delete("/results/{simulation_id}", status_code=204)
async def delete_simulation(
    simulation_id: str = Path(..., description="Simulation ID or filename")
):
    """
    Delete a specific simulation result.
    
    Permanently removes the simulation data from storage.
    """
    try:
        # Find the file by ID
        files = list_simulation_results()
        filename_to_delete = None
        
        for filename in files:
            try:
                data = load_simulation_result(filename)
                if data.get("id") == simulation_id or filename == simulation_id:
                    filename_to_delete = filename
                    break
            except:
                continue
                
        if not filename_to_delete:
            raise ResourceNotFoundError(
                detail=f"Simulation result not found",
                resource_type="simulation",
                resource_id=simulation_id
            )
            
        # Delete the file
        delete_simulation_result(filename_to_delete)
        return None
        
    except FileNotFoundError:
        raise ResourceNotFoundError(
            detail=f"Simulation result not found",
            resource_type="simulation",
            resource_id=simulation_id
        )
