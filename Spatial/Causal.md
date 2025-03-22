def Spatial_Causal(x):
    """
    Unified Model Function from: Spatial → Causal
    Dominant Force: Gravity
    File: Spatial/Causal.md
    S_int: 0.055125
    Phi: 2.773228
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.85
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
