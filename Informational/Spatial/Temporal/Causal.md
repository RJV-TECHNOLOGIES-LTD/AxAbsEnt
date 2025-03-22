def Informational_Spatial_Temporal_Causal(x):
    """
    Unified Model Function from: Informational → Spatial → Temporal → Causal
    Dominant Force: Gravity
    File: Informational/Spatial/Temporal/Causal.md
    S_int: 0.045325
    Phi: 2.708155
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.614125
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
