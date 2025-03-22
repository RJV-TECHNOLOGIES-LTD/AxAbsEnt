def Informational_Spatial_Causal_Temporal(x):
    """
    Unified Model Function from: Informational → Spatial → Causal → Temporal
    Dominant Force: Gravity
    File: Informational/Spatial/Causal/Temporal.md
    S_int: 0.0553
    Phi: 2.788033
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.614125
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
