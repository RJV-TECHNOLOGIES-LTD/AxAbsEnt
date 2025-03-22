def Informational_Spatial_Temporal(x):
    """
    Unified Model Function from: Informational → Spatial → Temporal
    Dominant Force: Gravity
    File: Informational/Spatial/Temporal.md
    S_int: 0.036487
    Phi: 2.617525
    Projection Weights: [0.85, 0.15, 0.1, 0.05]
    """
    decay = 0.7225
    transform = [0.85, 0.15, 0.1, 0.05]
    return [decay * x[i] * transform[i] for i in range(4)]
