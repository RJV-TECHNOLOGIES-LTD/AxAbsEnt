from .init import get_engine, init_db, get_session
from .models import Dimension

engine = get_engine()
init_db(engine)
session = get_session(engine)

# Seed example dimension
dim = Dimension(
    code="QC001",
    name="Quantum Cognition",
    description="Recursive simulation node for entangled memory and probabilistic inference.",
    formulation="f(x) = ⟨ψ|H|ψ⟩",
    metadata={"domain": "quantum_cognition"},
    parent_1=None,
    parent_2=None
)

session.add(dim)
session.commit()
print("Registry seeded.")
