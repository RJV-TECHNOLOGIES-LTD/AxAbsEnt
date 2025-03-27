# tools/validators/experimental_prediction.py

"""
Experimental Prediction Validator

Validates whether simulated or theorized predictions conform to empirical limits.
Ensures theoretical outputs remain within accepted physical boundaries, or are flagged
as requiring experimental falsifiability or publication review.
"""

import numpy as np

# Reference bounds (can be extended from /data/experimental/experimental_limits.json)
COUPLING_BOUNDS = {
    "gravity": (6.67e-11 * 0.9, 6.67e-11 * 1.1),
    "electromagnetic": (1 / 137.036, 1 / 137.000),
    "strong": (0.1181 * 0.95, 0.1181 * 1.05),
    "weak": (1.1663787e-5 * 0.95, 1.1663787e-5 * 1.05)
}

VACUUM_FLUCTUATION_VARIANCE_THRESHOLD = 1e-27  # Planck-scale fluctuations

CMB_PREDICTION_BOUNDS_K = (2.7250 - 0.0020, 2.7250 + 0.0020)  # Kelvin

def validate_coupling_constants(predicted_constants: dict) -> list:
    """
    Validate predicted force coupling constants against empirical bounds.
    """
    violations = []
    for force, (lower, upper) in COUPLING_BOUNDS.items():
        predicted = predicted_constants.get(force)
        if predicted is None:
            violations.append(f"Missing prediction for {force}")
            continue
        if not (lower <= predicted <= upper):
            violations.append(
                f"{force} constant {predicted:.4e} outside empirical range [{lower:.4e}, {upper:.4e}]"
            )
    return violations


def validate_vacuum_fluctuations(predicted_variance: float) -> bool:
    """
    Check if vacuum energy variance exceeds the Planck-scale tolerance.
    """
    return predicted_variance < VACUUM_FLUCTUATION_VARIANCE_THRESHOLD


def validate_cmb_temperature(predicted_temperature: float) -> bool:
    """
    Validate predicted CMB temperature against measured range.
    """
    return CMB_PREDICTION_BOUNDS_K[0] <= predicted_temperature <= CMB_PREDICTION_BOUNDS_K[1]


def validate_prediction_consistency(predictions: dict) -> dict:
    """
    Top-level validator that aggregates all prediction checks.

    Args:
        predictions (dict): Prediction results with keys like:
            - "coupling_constants": dict of force: value
            - "vacuum_variance": float
            - "cmb_temperature": float

    Returns:
        dict: {
            "valid": bool,
            "errors": list of strings
        }
    """
    errors = []

    # Coupling constant validation
    cc_errors = validate_coupling_constants(predictions.get("coupling_constants", {}))
    errors.extend(cc_errors)

    # Vacuum energy variance
    vacuum_ok = validate_vacuum_fluctuations(predictions.get("vacuum_variance", np.inf))
    if not vacuum_ok:
        errors.append("Vacuum fluctuation variance exceeds acceptable threshold.")

    # CMB temperature
    cmb_ok = validate_cmb_temperature(predictions.get("cmb_temperature", -1.0))
    if not cmb_ok:
        errors.append("Predicted CMB temperature is outside accepted range.")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
