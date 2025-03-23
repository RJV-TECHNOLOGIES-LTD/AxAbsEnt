# src/axabsent/core/absolute.py

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Union
import uuid
import numpy as np

class AbsoluteInvariantError(Exception):
    """Raised when an invalid transformation is attempted on an Absolute Entity."""
    pass

@dataclass
class AbsoluteEntity:
    """
    Represents an irreducible absolute entity as defined by the Enhanced Mathematical Ontology
    of Absolute Nothingness. Each entity is non-relational until invoked through mediator space
    interactions and carries its own invariant identity.
    """
    identifier: str = field(default_factory=lambda: str(uuid.uuid4()))
    signature: np.ndarray = field(default_factory=lambda: np.eye(1))  # Identity signature
    properties: Dict[str, Union[float, int, str, np.ndarray]] = field(default_factory=dict)
    state: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self._validate_signature()

    def _validate_signature(self):
        """Ensure the signature matrix is square and symmetric."""
        if not isinstance(self.signature, np.ndarray):
            raise TypeError("Signature must be a NumPy array.")
        if self.signature.shape[0] != self.signature.shape[1]:
            raise ValueError("Signature matrix must be square.")
        if not np.allclose(self.signature, self.signature.T):
            raise ValueError("Signature matrix must be symmetric.")

    def set_property(self, key: str, value: Union[float, int, str, np.ndarray]):
        """Set a scalar or tensorial property for the Absolute."""
        self.properties[key] = value

    def get_property(self, key: str) -> Union[float, int, str, np.ndarray]:
        """Get a property of the Absolute."""
        return self.properties.get(key)

    def project_state(self, projection_matrix: np.ndarray):
        """
        Projects the state into a transformed reference defined by a mediator space,
        without altering the core invariant identity.
        """
        if self.state is None:
            raise AbsoluteInvariantError("State is undefined for projection.")
        if projection_matrix.shape[1] != self.state.shape[0]:
            raise ValueError("Projection matrix and state dimension mismatch.")
        return projection_matrix @ self.state

    def encode_selection(self) -> np.ndarray:
        """
        Encodes the selection principle's scalar into the internal entropy representation,
        pending force interaction.
        """
        entropy_core = self.signature @ self.signature.T
        return np.trace(entropy_core)

    def __repr__(self):
        return f"<AbsoluteEntity id={self.identifier} signature={self.signature.shape} properties={len(self.properties)}>"
