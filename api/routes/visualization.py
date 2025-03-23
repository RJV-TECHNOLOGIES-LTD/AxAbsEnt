# api/routes/visualization.py

from fastapi import APIRouter
from axabsent.core.registry import get_registered_entities, get_registered_interactions

router = APIRouter(prefix="/api/visualization", tags=["visualization"])

@router.get("/graph")
def get_interaction_graph():
    """
    Returns the cross-absolute interaction graph for visualization purposes.
    
    Structure:
    {
        "nodes": [
            {
                "id": "uuid-1",
                "entropy": 1.23,
                "signature_rank": 128,
                "label": "gravity-node"
            },
            ...
        ],
        "edges": [
            {
                "source": "uuid-1",
                "target": "uuid-2",
                "operator": "Selection∘M→A"
            },
            ...
        ]
    }
    """
    entities = get_registered_entities()
    interactions = get_registered_interactions()

    nodes = []
    for e in entities:
        label = getattr(e, "labels", ["entity"])[0]
        nodes.append({
            "id": e.identifier,
            "entropy": round(float(e.encode_selection()), 5),
            "signature_rank": e.signature.shape[0],
            "label": label
        })

    edges = []
    for i in interactions:
        edges.append({
            "source": i.source.identifier,
            "target": i.target.identifier,
            "operator": i.operator.name
        })

    return { "nodes": nodes, "edges": edges }
