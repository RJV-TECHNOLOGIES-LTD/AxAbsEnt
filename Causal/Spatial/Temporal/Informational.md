def Causal_Spatial_Temporal_Informational(x):
    """
    Unified Model Function from: Causal → Spatial → Temporal → Informational
    Dominant Force: Gravity
    File: Causal/Spatial/Temporal/Informational.md
    S_int: 0.043375
    Phi: 2.708155
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.614125
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
