import transforge as tf
import ratiotheory

def test(complex_string):
    return ratiotheory.parse(complex_string, *(tf.Source() for _ in range(10)))