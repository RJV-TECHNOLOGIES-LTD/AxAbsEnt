import tensorflow as tf

def axabsent_potentiality_to_informational(x, name="axabsent_potentiality_to_informational"):
    """
    TensorFlow-compatible implementation of the AxAbsEnt entropic projection function:
    Domain: Potentiality → Informational
    Force Dominance: EM
    Φ: 3.1538
    S_int: 0.2956
    Decay factor: 0.85
    Weights: [0.1, 0.75, 0.25, 0.1] (EM)
    """
    with tf.name_scope(name):
        decay = tf.constant(0.85, dtype=tf.float32)
        weights = tf.constant([0.1, 0.75, 0.25, 0.1], dtype=tf.float32)
        x = tf.convert_to_tensor(x, dtype=tf.float32)
        return decay * x * weights