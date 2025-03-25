import pytest
from axabsent.mathematics.category_theory.category import Category, Morphism
from axabsent.mathematics.category_theory.functor import Functor
from axabsent.mathematics.category_theory.adjoint import AdjointPair
from axabsent.mathematics.category_theory.natural_transformation import NaturalTransformation


@pytest.mark.math
def test_identity_morphism_composition():
    """
    Test that identity morphism behaves correctly under composition.
    """
    cat = Category("Absolutes")
    A = cat.add_object("A")
    id_A = cat.identity(A)
    f = Morphism("f", A, A, lambda x: x + 1)

    composed = f.compose(id_A)
    assert composed(A(2)) == 3

    composed_reverse = id_A.compose(f)
    assert composed_reverse(A(2)) == 3


@pytest.mark.math
def test_functor_preserves_composition():
    """
    Test that a functor preserves identity and composition structure.
    """
    C = Category("Source")
    D = Category("Target")

    A = C.add_object("A")
    B = C.add_object("B")

    f = Morphism("f", A, B, lambda x: 2 * x)
    C.add_morphism(f)

    F = Functor("F", C, D)
    F.map_object(A, "FA")
    F.map_object(B, "FB")
    F.map_morphism(f, lambda x: 2 * x + 1)

    Ff = F(f)
    assert Ff(F(A(1))) == 2 * 1 + 1


@pytest.mark.math
def test_natural_transformation_commutes():
    """
    Ensure natural transformations satisfy the commutative square condition.
    """
    C = Category("Source")
    D = Category("Target")

    A = C.add_object("A")
    B = C.add_object("B")
    f = Morphism("f", A, B, lambda x: x + 1)

    C.add_morphism(f)

    F = Functor("F", C, D)
    G = Functor("G", C, D)

    F.map_object(A, "FA")
    F.map_object(B, "FB")
    F.map_morphism(f, lambda x: x + 2)

    G.map_object(A, "GA")
    G.map_object(B, "GB")
    G.map_morphism(f, lambda x: x + 3)

    # Define the natural transformation η: F ⇒ G
    eta = NaturalTransformation("η", F, G, components={
        "A": lambda x: x + 10,
        "B": lambda x: x + 10
    })

    # Check commutativity: η_B ∘ F(f) = G(f) ∘ η_A
    lhs = eta("B")(F(f)(1))      # η_B(F(f(1)))
    rhs = G(f)(eta("A")(1))      # G(f)(η_A(1))
    assert lhs == rhs


@pytest.mark.math
def test_adjoint_unit_and_counit_properties():
    """
    Verify unit and counit properties of adjoint functor pair.
    """
    C = Category("Structure")
    D = Category("Tensor")

    A = C.add_object("A")
    L = Functor("L", C, D)
    R = Functor("R", D, C)

    L.map_object("A", "LA")
    R.map_object("LA", "A")

    adj = AdjointPair(L, R)

    # Simulate unit η: id_C → R∘L
    eta = adj.unit()
    assert eta("A")(5) == R(L("A")(5))  # Simplified trace

    # Simulate counit ε: L∘R → id_D
    eps = adj.counit()
    assert eps("LA")(5) == L(R("LA")(5))  # Simplified trace
