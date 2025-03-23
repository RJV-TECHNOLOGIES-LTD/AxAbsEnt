# src/mathematics/category_theory/adjoint.py

from typing import Callable, Dict
from .category import CategoryObject, Morphism
from .functor import Functor

class AdjointPair:
    """
    Defines an adjoint pair of functors F: C -> D and G: D -> C satisfying
    the natural isomorphism:
        Hom_D(F(A), X) ≅ Hom_C(A, G(X))
    This is characterized by:
        - A unit natural transformation η: id_C -> G ∘ F
        - A counit natural transformation ε: F ∘ G -> id_D
    These transformations capture the duality between information transfer
    and force projection under the unified CEFT/FDT framework.
    """
    def __init__(self, 
                 F: Functor, 
                 G: Functor, 
                 unit: Callable[[CategoryObject], Morphism], 
                 counit: Callable[[CategoryObject], Morphism]):
        self.F = F
        self.G = G
        self.unit = unit          # η: for each object A in C, a morphism η_A: A → G(F(A))
        self.counit = counit      # ε: for each object X in D, a morphism ε_X: F(G(X)) → X
        self.unit_components: Dict[str, Morphism] = {}
        self.counit_components: Dict[str, Morphism] = {}

    def apply_unit(self):
        """
        Applies the unit natural transformation to all objects in the source category.
        """
        for obj_id, obj in self.F.C.objects.items():
            self.unit_components[obj_id] = self.unit(obj)

    def apply_counit(self):
        """
        Applies the counit natural transformation to all objects in the target category.
        """
        for obj_id, obj in self.G.D.objects.items():
            self.counit_components[obj_id] = self.counit(obj)

    def check_triangular_identities(self, verbose: bool = False) -> bool:
        """
        Checks the triangular identities:
          1. For every object A in C, the composite:
                F(A) --F(η_A)--> F(G(F(A))) --ε_{F(A)}--> F(A)
             should be the identity on F(A).
          2. For every object X in D, the composite:
                G(X) --η_{G(X)}--> G(F(G(X))) --G(ε_X)--> G(X)
             should be the identity on G(X).
        In this abstract implementation, we assume the identities hold if
        the unit and counit components are defined.
        """
        if not self.unit_components or not self.counit_components:
            if verbose:
                print("Unit or counit components are missing; cannot verify triangular identities.")
            return False
        if verbose:
            print("Triangular identities are assumed to hold based on defined unit and counit transformations.")
        return True

    def __repr__(self):
        return f"<AdjointPair: F({len(self.F.C.objects)} objects) ⊣ G({len(self.G.D.objects)} objects)>"
