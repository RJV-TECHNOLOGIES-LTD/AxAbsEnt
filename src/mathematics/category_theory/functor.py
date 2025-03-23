# src/mathematics/category_theory/functor.py

from typing import Callable, Dict
from .category import Category, CategoryObject, Morphism

class Functor:
    """
    Represents a functor F: C → D between two categories.
    It maps:
        - Objects: F(A) for every object A in C
        - Morphisms: F(f): F(A) → F(B) for each f: A → B
    Preserves composition and identity:
        F(id_A) = id_{F(A)}, and F(f ∘ g) = F(f) ∘ F(g)
    """

    def __init__(
        self,
        source_category: Category,
        target_category: Category,
        object_map: Callable[[CategoryObject], CategoryObject],
        morphism_map: Callable[[Morphism], Morphism]
    ):
        self.C = source_category
        self.D = target_category
        self.F_obj = object_map
        self.F_mor = morphism_map
        self.mapped_objects: Dict[str, CategoryObject] = {}
        self.mapped_morphisms: Dict[str, Morphism] = {}

    def apply(self):
        for obj_id, obj in self.C.objects.items():
            mapped_obj = self.F_obj(obj)
            self.D.add_object(mapped_obj)
            self.mapped_objects[obj_id] = mapped_obj

        for morphism in self.C.morphisms:
            mapped_mor = self.F_mor(morphism)
            self.D.add_morphism(mapped_mor)
            key = f"{morphism.source.identifier}->{morphism.target.identifier}"
            self.mapped_morphisms[key] = mapped_mor

    def __repr__(self):
        return f"<Functor {len(self.mapped_objects)} objects | {len(self.mapped_morphisms)} morphisms mapped>"
