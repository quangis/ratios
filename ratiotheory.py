from transforge.type import Type, Constraint, \
    TypeInstance, TypeAlias, TypeOperator, \
    with_parameters, _, Top
from transforge.lang import Language
from transforge.expr import Operator

#Quantity domains
Quantity = TypeOperator()
Amount = TypeOperator(supertype=Quantity, param=1)
Magnitude = TypeOperator(supertype=Quantity, param=1)
ArchimedeanMagnitude = TypeAlias(lambda x: Magnitude(x) [x <= Amount])
Number = TypeOperator()
Proportion = TypeOperator(params=2, supertype=Magnitude)
ProportionalMagnitude = TypeAlias(lambda x, y: Proportion(x,y) [x, y <= Magnitude])

#------------------------

Position = TypeOperator()
Moment = TypeOperator()
Object = TypeOperator()
Event = TypeOperator()
Bool = TypeOperator()

#-------------------
Region = TypeAlias(Amount(Position))
Period = TypeAlias(Amount(Moment))
ContentAmount = TypeAlias(supertype=Amount)
AmountofObject = TypeAlias(Amount(Object), supertype=ContentAmount)
AmountofEvent = TypeAlias(Amount(Event), supertype=ContentAmount)


Size = TypeAlias(ArchimedeanMagnitude(Region))
#-----------------------------------------------
#operations
#---------



measurement = Operator(
    "measures some amount",
    type=lambda x: x ** ArchimedeanMagnitude(x) [x <= Amount]
)
enumerate = Operator(
    "gives back the number of a magnitude",
    type=Magnitude ** Number
)

ratio = Operator(
    "building ratios",
    type=x ** y ** ProportionalMagnitude(x,y) [x <= Magnitude, y <= Magnitude]
)

quotient = Operator (
    "building quotient",
    type=Number ** Number ** Number
)

## x:Region y:AmountofObject
## enumerate(ratio(measurement(x),measurement(y)))

partOf =Operator (
    type= x ** x ** Bool [x<Amount]
)

