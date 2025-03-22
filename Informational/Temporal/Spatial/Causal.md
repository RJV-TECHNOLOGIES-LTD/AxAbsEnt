def Informational_Temporal_Spatial_Causal(x):
    """
    Unified Model Function from: Informational → Temporal → Spatial → Causal
    Dominant Force: Gravity
    File: Informational/Temporal/Spatial/Causal.md
    S_int: 0.043375
    Phi: 2.708155
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.614125
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
