def Temporal_Spatial_Causal(x):
    """
    Unified Model Function from: Temporal → Spatial → Causal
    Dominant Force: Gravity
    File: Temporal/Spatial/Causal.md
    S_int: 0.040163
    Phi: 2.65341
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.7225
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
