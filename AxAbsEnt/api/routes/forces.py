# api/routes/forces.py

from fastapi import APIRouter, Query, HTTPException
from typing import Literal
import numpy as np

from axabsent.forces.gravity import compute_gravity_field
from axabsent.forces.electromagnetic import compute_em_field
from axabsent.forces.strong import compute_strong_field
from axabsent.forces.weak import compute_weak_field

router = APIRouter(prefix="/api/forces", tags=["forces"])

@router.get("/field")
def get_force_field(type: Literal["gravity", "electromagnetic", "strong", "weak"] = Query(...)):
    """
    Returns a 2D vector field (X, Y, U, V) for the specified force type.
    Used by ForceExplorer frontend component.
    """
    resolution = 20
    x = np.linspace(-1, 1, resolution)
    y = np.linspace(-1, 1, resolution)
    X, Y = np.meshgrid(x, y)

    if type == "gravity":
        U, V = compute_gravity_field(X, Y)
    elif type == "electromagnetic":
        U, V = compute_em_field(X, Y)
    elif type == "strong":
        U, V = compute_strong_field(X, Y)
    elif type == "weak":
        U, V = compute_weak_field(X, Y)
    else:
        raise HTTPException(status_code=400, detail="Invalid force type.")

    return {
        "X": X.tolist(),
        "Y": Y.tolist(),
        "U": U.tolist(),
        "V": V.tolist()
    }
