from transforge.type import Type, Constraint, \
    TypeInstance, TypeAlias, TypeOperator, \
    with_parameters, _, Top
from transforge.lang import Language
from transforge.expr import Operator, Source


#------------------------------
#Quantity types
Quantity = TypeOperator()
Amount = TypeOperator(params=1) #supertype=Quantity
Magnitude = TypeAlias(lambda x: x[x << (ArchimedeanMagnitude(_), ProportionalMagnitude(_,_))])

Archimedean = TypeOperator(params=1) #upertype=Quantity
ArchimedeanMagnitude = TypeAlias(lambda x: Archimedean(x) [x <= Amount])
Proportion = TypeOperator(params=2) #, supertype=Magnitude
ProportionalMagnitude = TypeAlias(lambda x, y: Proportion(x,y) [x <= Magnitude, y <= Magnitude])

#------------------------
#Quantity Domains
Position = TypeOperator()
Moment = TypeOperator()
Object = TypeOperator()
Event = TypeOperator()
Bool = TypeOperator()
Substance = TypeOperator()

#-------------------
#Types of amounts
Region = TypeAlias(Amount(Position))
Period = TypeAlias(Amount(Moment))
ContentAmount = TypeAlias(lambda x: x[x << (AmountofObject,AmountofEvent,AmountofSubstance)])
AmountofObject = TypeAlias(Amount(Object))
AmountofEvent = TypeAlias(Amount(Event))
AmountofSubstance = TypeAlias(Amount(Substance))

#-------------------
#Types of magnitudes
Size = TypeAlias(Archimedean(Region))
Duration = TypeAlias(Archimedean(Period))
Value = TypeAlias(Archimedean(ContentAmount))
#-----------------------------------------------
#operations
#---------

measure = Operator(
    "measures some amount",
    type=lambda x: x ** Archimedean(x) [x <= Amount]
)
ratio = Operator(
    "building ratios of archimedean magnitudes",
    type=lambda x, y: x ** y ** Proportion(x,y)[x << Archimedean(_), y << Archimedean(_)]
)
multiply = Operator(
    "building archimedean magnitudes with ratios",
    type=lambda z, w: Proportion(z,w) ** w ** z
)
partOf = Operator(
    type= x ** x ** Bool[x <= Amount]
)

# Language ###################################################################

cct = Language(
    scope=locals(),
    namespace=("ratios", "https://github.com/quangis/ratios#"),
    canon={
    Top,
    Quantity,
    Amount,
    Magnitude,
    Archimedean,
    Proportion,
    Position,
    Moment,
    Object,
    Event,
    Bool,
    Substance
    })