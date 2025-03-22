import tensorflow as tf

def axabsent_causal_potentiality_to_informational(x, name="axabsent_causal_potentiality_to_informational"):
    """
    TensorFlow-compatible implementation of the AxAbsEnt entropic projection function:
    Domain: Causal → Potentiality → Informational
    Force Dominance: Strong
    Φ: 3.1897
    S_int: 0.2967
    Decay factor: 0.7225
    Weights: [0.2, 0.1, 0.7, 0.15] (Strong)
    """
    with tf.name_scope(name):
        decay = tf.constant(0.7224999999999999, dtype=tf.float32)
        weights = tf.constant([0.2, 0.1, 0.7, 0.15], dtype=tf.float32)
        x = tf.convert_to_tensor(x, dtype=tf.float32)
        return decay * x * weights