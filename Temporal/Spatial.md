def Temporal_Spatial(x):
    """
    Unified Model Function from: Temporal → Spatial
    Dominant Force: Gravity
    File: Temporal/Spatial.md
    S_int: 0.0252
    Phi: 2.533592
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.85
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
