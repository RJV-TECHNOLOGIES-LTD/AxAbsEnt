# tools/validators/theory_consistency.py

"""
Cross-Absolute Theory Consistency Validator

Ensures that the theoretical definitions and data structures in use:
- Conform to the core axioms of the Enhanced Mathematical Ontology of Absolute Nothingness
- Respect the directionality and irreducibility of absolutes
- Prevent invalid compositions and entropic contradictions
- Preserve the principle of cross-absolute selection minimization
"""

from typing import Dict, List, Any
import numpy as np

def validate_cross_absolute_theory(theory: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate whether a theoretical structure adheres to ontological, causal,
    and mathematical constraints.

    Args:
        theory (dict): Should include:
            - "absolutes": list of dicts with id, signature, properties
            - "interactions": list of dicts with sourceId, targetId, operatorType
            - "selection_function": callable or string identifier
            - "mediator_dimensions": int

    Returns:
        dict: {
            "valid": bool,
            "errors": list of str
        }
    """
    errors: List[str] = []

    # Check absolutes
    absolutes = theory.get("absolutes", [])
    if len(absolutes) < 2:
        errors.append("Theory must define at least two absolute entities.")

    ids = set()
    for abs_entity in absolutes:
        abs_id = abs_entity.get("id")
        if abs_id in ids:
            errors.append(f"Duplicate absolute ID found: {abs_id}")
        ids.add(abs_id)

        sig = abs_entity.get("signature")
        if sig is None or not isinstance(sig, (list, np.ndarray)):
            errors.append(f"Missing or invalid signature for absolute {abs_id}")
        else:
            sig_matrix = np.array(sig)
            if sig_matrix.shape[0] != sig_matrix.shape[1]:
                errors.append(f"Signature for absolute {abs_id} is not square.")
            if not np.allclose(sig_matrix, sig_matrix.T):
                errors.append(f"Signature for absolute {abs_id} is not symmetric.")

    # Validate interactions
    interactions = theory.get("interactions", [])
    for inter in interactions:
        src = inter.get("sourceId")
        tgt = inter.get("targetId")
        op = inter.get("operatorType", "")

        if src not in ids or tgt not in ids:
            errors.append(f"Interaction refers to undefined absolute(s): {src} → {tgt}")
        if src == tgt:
            errors.append(f"Invalid self-interaction detected for absolute {src}")
        if not op:
            errors.append(f"Interaction between {src} and {tgt} missing operatorType")

    # Check selection principle
    selection_fn = theory.get("selection_function")
    if not selection_fn:
        errors.append("Theory lacks a defined selection function.")
    elif not callable(selection_fn) and not isinstance(selection_fn, str):
        errors.append("Selection function must be callable or resolvable string.")

    # Mediator space dimensionality
    dim = theory.get("mediator_dimensions")
    if dim is None or not isinstance(dim, int) or dim < 1:
        errors.append("Mediator space must have valid positive dimensionality.")
    elif dim > 8:
        errors.append(f"Mediator space dimensionality {dim} exceeds the 8D causal envelope limit.")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
