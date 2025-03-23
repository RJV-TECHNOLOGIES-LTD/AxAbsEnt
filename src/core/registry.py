# src/core/registry.py

_registered_entities = []
_registered_interactions = []

def register_entity(entity):
    _registered_entities.append(entity)

def register_interaction(source, target, operator):
    _registered_interactions.append(
        InteractionRecord(source=source, target=target, operator=operator)
    )

def get_registered_entities():
    return _registered_entities

def get_registered_interactions():
    return _registered_interactions

class InteractionRecord:
    def __init__(self, source, target, operator):
        self.source = source
        self.target = target
        self.operator = operator

