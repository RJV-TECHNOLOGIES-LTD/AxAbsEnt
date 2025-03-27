# api/routes/interaction.py

from fastapi import APIRouter
from axabsent.core.registry import get_registered_entities, get_registered_interactions

router = APIRouter(prefix="/api/interactions", tags=["interactions"])

@router.get("/topology")
def get_interaction_topology():
    """
    Returns a graph representation of all registered absolute entities
    and their directed interactions for visualization.

    Response Format:
    {
        "nodes": [
            { "id": "uuid-1", "entropy": 1.23, "signature_rank": 3 },
            ...
        ],
        "links": [
            { "source": "uuid-1", "target": "uuid-2", "label": "Selection∘Action" },
            ...
        ]
    }
    """
    nodes = []
    links = []

    entities = get_registered_entities()
    interactions = get_registered_interactions()

    for entity in entities:
        entropy = entity.encode_selection()
        rank = int(entity.signature.shape[0])
        nodes.append({
            "id": entity.identifier,
            "entropy": round(float(entropy), 4),
            "signature_rank": rank
        })

    for interaction in interactions:
        source = interaction.source.identifier
        target = interaction.target.identifier
        label = interaction.operator.name
        links.append({
            "source": source,
            "target": target,
            "label": label
        })

    return { "nodes": nodes, "links": links }
