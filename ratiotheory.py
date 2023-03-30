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

Archimedean = TypeOperator(params=1) #upertype=Magnitude
ArchimedeanMagnitude = TypeAlias(lambda x: Archimedean(x) [x <= Amount(_)])
Proportion = TypeOperator(params=2) #, supertype=Magnitude
ProportionalMagnitude = TypeAlias(lambda x, y: Proportion(x,y) [x <= Magnitude(_), y <= Magnitude(_)])

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
ObjectCount = TypeAlias(Archimedean(AmountofObject))
EventCount = TypeAlias(Archimedean(AmountofEvent))
Mass = TypeAlias(Archimedean(AmountofSubstance))

#Types of Proportions
ObjectDensity = TypeAlias(Proportion(ObjectCount,Size))
EventDensity = TypeAlias(Proportion(EventCount,Size))
MassDensity = TypeAlias(Proportion(Mass,Size))
ObjectFrequency = TypeAlias(Proportion(ObjectCount,Duration))
EventFrequency = TypeAlias(Proportion(EventCount,Duration))


#-----------------------------------------------
#operations
#---------
reciprocal =Operator(
    "reciprocal of a ratio",
    type=lambda z, w: Proportion(z,w) ** Proportion(w,z)
)
measure = Operator(
    "measures some amount",
    type=lambda x: x ** Archimedean(x) [x <= Amount(_)]
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
    type= lambda x: x ** x ** Bool[x <= Amount(_)]
)

# Language ###################################################################

ratiotheory = Language(
    scope=locals(),
    namespace=("ratios", "https://github.com/quangis/ratios#"),
    canon={
    Top,
    Position,
 Moment,
 Object,
 Event,
 Bool,
 Substance,
 Amount(Position),
Amount(Moment),
Amount(Object),
Amount(Event),
Amount(Substance),
Archimedean(Region),
Archimedean(Period),
Archimedean(AmountofObject),
Archimedean(AmountofEvent),
Archimedean(AmountofSubstance),
# ObjectDensity,
# EventDensity,
# MassDensity,
# ObjectFrequency,
# EventFrequency
    })