def Causal_Spatial(x):
    """
    Unified Model Function from: Causal → Spatial
    Dominant Force: Gravity
    File: Causal/Spatial.md
    S_int: 0.055125
    Phi: 2.773228
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.85
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
