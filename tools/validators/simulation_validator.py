# tools/validators/simulation_validator.py

"""
Simulation Configuration Validator

Validates AxAbsEnt simulation setup before execution. Ensures:
- Entity and interaction consistency
- Numerical stability bounds
- Entropy constraints
- Mediator dimensional alignment
"""

from typing import Dict, Any, List
import numpy as np

REQUIRED_FIELDS = {
    "entities",         # List of absolute entity IDs
    "interaction",      # Interaction ID
    "timestep",         # dt for simulation
    "steps",            # Total steps
    "mediator_dim",     # Dimensionality of mediator space
}

DEFAULT_LIMITS = {
    "timestep_min": 1e-6,
    "timestep_max": 1.0,
    "steps_max": 100000,
    "entropy_ceiling": 1e6,
    "mediator_dim_max": 8
}

def validate_simulation_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates a full simulation configuration dictionary.

    Returns:
        dict: {
            "valid": bool,
            "errors": list of strings
        }
    """
    errors: List[str] = []

    # Field presence
    for field in REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"Missing required simulation field: '{field}'")

    if errors:
        return {"valid": False, "errors": errors}

    # Type and value checks
    entities = config["entities"]
    if not isinstance(entities, list) or len(entities) < 2:
        errors.append("Simulation must include at least 2 absolute entities.")

    if not isinstance(config["interaction"], str) or not config["interaction"].strip():
        errors.append("Interaction ID must be a non-empty string.")

    timestep = config["timestep"]
    if not (DEFAULT_LIMITS["timestep_min"] <= timestep <= DEFAULT_LIMITS["timestep_max"]):
        errors.append(f"Timestep {timestep} out of bounds [{DEFAULT_LIMITS['timestep_min']}, {DEFAULT_LIMITS['timestep_max']}]")

    steps = config["steps"]
    if steps > DEFAULT_LIMITS["steps_max"]:
        errors.append(f"Simulation steps exceed maximum allowed ({DEFAULT_LIMITS['steps_max']})")

    mediator_dim = config["mediator_dim"]
    if mediator_dim > DEFAULT_LIMITS["mediator_dim_max"]:
        errors.append(f"Mediator dimensionality {mediator_dim} exceeds allowed maximum ({DEFAULT_LIMITS['mediator_dim_max']})")

    # Optional: check entropy if provided
    if "initial_entropy" in config:
        entropy = config["initial_entropy"]
        if not isinstance(entropy, (int, float)) or entropy < 0:
            errors.append("Initial entropy must be a non-negative scalar.")
        elif entropy > DEFAULT_LIMITS["entropy_ceiling"]:
            errors.append(f"Initial entropy {entropy} exceeds ceiling ({DEFAULT_LIMITS['entropy_ceiling']})")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
