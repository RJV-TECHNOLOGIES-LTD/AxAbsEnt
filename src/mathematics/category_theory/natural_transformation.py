# src/mathematics/category_theory/natural_transformation.py

from typing import Dict, Callable
from .category import CategoryObject, Morphism
from .functor import Functor

class NaturalTransformation:
    """
    Represents a natural transformation η: F → G between two functors F, G: C → D.
    For every object A in C, η assigns a morphism η_A: F(A) → G(A) in D such that
    for every morphism f: A → B in C, the following naturality condition holds:
    
        η_B ∘ F(f) = G(f) ∘ η_A
    
    In the context of AxAbsEnt, natural transformations capture dynamic shifts
    between different mediator or force representations.
    """

    def __init__(
        self,
        source_functor: Functor,
        target_functor: Functor,
        transformation: Callable[[CategoryObject], Morphism]
    ):
        """
        Parameters:
            source_functor: The functor F from category C to D.
            target_functor: The functor G from category C to D.
            transformation: A function that, for each object A in C,
                            returns a morphism η_A: F(A) → G(A) in D.
        """
        self.F = source_functor
        self.G = target_functor
        self.transformation = transformation
        self.components: Dict[str, Morphism] = {}

    def apply(self):
        """
        Applies the natural transformation to all objects in the source category.
        Stores the resulting components η_A for each object A.
        """
        for obj_id, obj in self.F.mapped_objects.items():
            morphism = self.transformation(obj)
            self.components[obj_id] = morphism

    def verify_naturality(self) -> bool:
        """
        Verifies the naturality condition for all morphisms in the source category.
        For each morphism f: A → B in C:
            η_B ∘ F(f) ?= G(f) ∘ η_A
        Returns True if all conditions are satisfied (within numerical tolerance), False otherwise.
        """
        for morphism in self.F.C.morphisms:
            source_id = morphism.source.identifier
            target_id = morphism.target.identifier

            # Get the mapped morphisms from functors
            F_f = self.F.F_mor(morphism)
            G_f = self.G.F_mor(morphism)

            eta_source = self.components.get(source_id)
            eta_target = self.components.get(target_id)

            if eta_source is None or eta_target is None:
                return False

            # Compose morphisms: η_B ∘ F(f) and G(f) ∘ η_A
            comp1 = Morphism(eta_source.source, eta_target.target, lambda x: eta_target.operation(F_f.operation(x)))
            comp2 = Morphism(eta_source.source, eta_target.target, lambda x: G_f.operation(eta_source.operation(x)))

            # For verification, compare outputs on a test value (if applicable)
            test_value = eta_source.source.data
            if abs(comp1.operation(test_value) - comp2.operation(test_value)) > 1e-6:
                return False
        return True

    def summary(self, verbose: bool = False) -> dict:
        """
        Provides a summary of the natural transformation, including component mappings
        and whether the naturality condition holds.
        """
        natural = self.verify_naturality()
        if verbose:
            print(f"[NaturalTransformation] Components: {self.components}")
            print(f"[NaturalTransformation] Naturality condition satisfied: {natural}")
        return {
            "components": self.components,
            "naturality_satisfied": natural
        }

    def __repr__(self):
        return f"<NaturalTransformation from {self.F} to {self.G}, naturality_satisfied={self.verify_naturality()}>"
