import transforge as tf
from ratiotheory import ratiotheory
#from lang2tools import lang2tools
import json

def test(complex_string):
    return ratiotheory.parse(complex_string, *(tf.Source() for _ in range(10))).primitive()
expressions =[
    """
    1: R2(MassDensity, Region);
    2: R1(Region);
    consarchimed(
        arealinterpol(
            coverage2lattice(1)
            ,
            2
        )
    )
    """,
    """
    1: R2(MassDensity, Region);
    2: R1(Region);
    consarchimed(
        field2lattice (
            revert 1
        ) 2
    )
    """,
    """
    1: R2(Region, EventCount);
    2: R1(Region);
    consarchimed(
        arealinterpol(
                consproportion(1),
                2
            )
        )
    """,
    """
    1: R2(Object, Region * EventCount) ;
    2: R1(Region);
    apply2 multiply
    (arealinterpol 
        (getregionqualities 
            (join_attr 
                (get_attrL 1) 
                    (apply2 ratio 
                        (get_attrR 1) 
                        (apply1(measure,get_attrL(1)))
                    )
            )
        ) 2
    ) 
    (apply measure 2)    
    """,
    """ 
    1: AmountofObject;
    2: Region;
    multiply(ratio(measure(1),measure(2)), measure(2))
    """
    ]


for e in expressions:
    print(test(e).tree())
#Get the subtype structure (ontology) in rdf
g = tf.TransformationGraph(ratiotheory)
g.add_taxonomy()
g.add_operators()

print(g.serialize())

#print(json.dumps(lang2tools(ratiotheory), indent=4))