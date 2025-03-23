# api/routes/absolute.py

from fastapi import APIRouter
from typing import List, Dict, Any
from axabsent.core.registry import get_registered_entities

router = APIRouter(prefix="/api/absolute", tags=["absolute"])

@router.get("/list")
def list_absolute_entities() -> List[Dict[str, Any]]:
    """
    Returns a list of all registered AbsoluteEntities with their metadata.

    Example Response:
    [
        {
            "id": "uuid-123...",
            "entropy": 1.392,
            "signature_shape": [128, 1],
            "labels": ["entity_type", ...]
        },
        ...
    ]
    """
    entities = get_registered_entities()

    return [
        {
            "id": e.identifier,
            "entropy": round(float(e.encode_selection()), 5),
            "signature_shape": list(e.signature.shape),
            "labels": getattr(e, "labels", [])
        }
        for e in entities
    ]
