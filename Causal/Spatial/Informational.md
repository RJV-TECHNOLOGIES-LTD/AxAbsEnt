def Causal_Spatial_Informational(x):
    """
    Unified Model Function from: Causal → Spatial → Informational
    Dominant Force: Gravity
    File: Causal/Spatial/Informational.md
    S_int: 0.05145
    Phi: 2.737342
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.7225
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
