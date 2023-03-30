import transforge as tf

def test(complex_string):
    return cct.parse(complex_string, *(tf.Source() for _ in range(10)))