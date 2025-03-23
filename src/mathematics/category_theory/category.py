# src/mathematics/category_theory/category.py

from typing import Callable, Any, Dict, List, Optional

class CategoryObject:
    """
    Represents an object in the force-category framework.
    Typically corresponds to an Absolute Entity or an Entangled Configuration.
    """
    def __init__(self, identifier: str, data: Any):
        self.identifier = identifier
        self.data = data

    def __repr__(self):
        return f"<CategoryObject id={self.identifier}>"

class Morphism:
    """
    Represents a morphism (structure-preserving map) between two category objects.
    This typically reflects an InteractionOperator or InformationTransfer mechanism.
    """
    def __init__(self, source: CategoryObject, target: CategoryObject, operation: Callable[[Any], Any]):
        self.source = source
        self.target = target
        self.operation = operation

    def apply(self) -> Any:
        return self.operation(self.source.data)

    def __repr__(self):
        return f"<Morphism {self.source.identifier} → {self.target.identifier}>"

class Category:
    """
    Defines a mathematical category with objects and morphisms obeying:
    - Associativity: f ∘ (g ∘ h) = (f ∘ g) ∘ h
    - Identity: ∃ id_A: A → A for all A
    This forms the foundation for force functional composition and resonance mapping.
    """
    def __init__(self):
        self.objects: Dict[str, CategoryObject] = {}
        self.morphisms: List[Morphism] = []

    def add_object(self, obj: CategoryObject):
        self.objects[obj.identifier] = obj

    def add_morphism(self, morphism: Morphism):
        self.morphisms.append(morphism)

    def get_morphism(self, source_id: str, target_id: str) -> Optional[Morphism]:
        for m in self.morphisms:
            if m.source.identifier == source_id and m.target.identifier == target_id:
                return m
        return None

    def identity(self, obj_id: str) -> Morphism:
        obj = self.objects[obj_id]
        return Morphism(obj, obj, lambda x: x)

    def compose(self, f: Morphism, g: Morphism) -> Morphism:
        """
        Returns a composite morphism: f ∘ g
        Requires g.target == f.source
        """
        if g.target.identifier != f.source.identifier:
            raise ValueError("Cannot compose: target of g ≠ source of f")
        new_op = lambda x: f.operation(g.operation(x))
        return Morphism(g.source, f.target, new_op)

    def __repr__(self):
        return f"<Category objects={len(self.objects)} morphisms={len(self.morphisms)}>"
