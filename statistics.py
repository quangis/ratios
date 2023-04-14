import transforge as tf
from ratiotheory import ratiotheory

def test(complex_string):
    return ratiotheory.parse(complex_string, *(tf.Source() for _ in range(10)))
expressions =[
""" 
1: AmountofObject;
2: Region;
multiply(ratio(measure(1),measure(2)), measure(2))
""",
    """
    1: ObjectInfo(Nom);
    
    
    """

    ]


for e in expressions:
    print(test(e).tree())
#Get the subtype structure (ontology) in rdf
g = tf.TransformationGraph(ratiotheory)
g.add_taxonomy()
g.add_operators()

#print(g.serialize())
