from transforge.type import Type, Constraint, \
    TypeInstance, TypeAlias, TypeOperator, \
    with_parameters, _, Top
from transforge.lang import Language
from transforge.expr import Operator

#Quantity domains
Quantity = TypeOperator()
Amount = TypeOperator(params=1) #supertype=Quantity
Magnitude = TypeAlias(lambda x: x[x << (ArchimedeanMagnitude(_), ProportionalMagnitude(_,_))])

Archimedean = TypeOperator(params=1) #upertype=Quantity
ArchimedeanMagnitude = TypeAlias(lambda x: Archimedean(x) [x <= Amount])
Proportion = TypeOperator(params=2) #, supertype=Magnitude
ProportionalMagnitude = TypeAlias(lambda x, y: Proportion(x,y) [x <= Magnitude, y <= Magnitude])

Number = TypeOperator()

#------------------------

Position = TypeOperator()
Moment = TypeOperator()
Object = TypeOperator()
Event = TypeOperator()
Bool = TypeOperator()

#-------------------
Region = TypeAlias(Amount(Position))
Period = TypeAlias(Amount(Moment))
ContentAmount = TypeAlias(lambda x: x[x << (AmountofObject,AmountofEvent)])
AmountofObject = TypeAlias(Amount(Object))
AmountofEvent = TypeAlias(Amount(Event))


Size = TypeAlias(ArchimedeanMagnitude(Region))
Duration = TypeAlias(ArchimedeanMagnitude(Period))
Value = TypeAlias(ArchimedeanMagnitude(ContentAmount))
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
    type=x ** y ** ProportionalMagnitude(x,y)[x <= Magnitude, y <= Magnitude]
)

quotient = Operator(
    "building quotient",
    type=Number ** Number ** Number
)

## x:Region y:AmountofObject
## enumerate(ratio(measurement(x),measurement(y)))

partOf = Operator(
    type= x ** x ** Bool[x <= Amount]
)

