def Spatial_Temporal(x):
    """
    Unified Model Function from: Spatial → Temporal
    Dominant Force: Gravity
    File: Spatial/Temporal.md
    S_int: 0.0252
    Phi: 2.533592
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.85
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
