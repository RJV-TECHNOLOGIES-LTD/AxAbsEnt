def Causal_Temporal_Spatial_Informational(x):
    """
    Unified Model Function from: Causal → Temporal → Spatial → Informational
    Dominant Force: Gravity
    File: Causal/Temporal/Spatial/Informational.md
    S_int: 0.045325
    Phi: 2.708155
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.614125
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
