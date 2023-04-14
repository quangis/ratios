from transforge.type import Type, Constraint, \
    TypeInstance, TypeAlias, TypeOperator, \
    with_parameters, _, Top
from transforge.lang import Language
from transforge.expr import Operator, Source

from cct import cct
#--------------------------
#cct
# Types ######################################################################

Val = TypeOperator()
Obj = TypeOperator(supertype=Val)  # O
Reg = TypeOperator(supertype=Val)  # S
Loc = TypeOperator(supertype=Val)  # L
Qlt = TypeOperator(supertype=Val)  # Q
Nom = TypeOperator(supertype=Qlt)
Bool = TypeOperator(supertype=Nom)
Ord = TypeOperator(supertype=Nom)
Itv = TypeOperator(supertype=Ord)
Ratio = TypeOperator(supertype=Itv)
Count = TypeOperator(supertype=Ratio)
# R = TypeOperator(params=2)
R1 = TypeOperator(params=1)
R2 = TypeOperator(params=2)
R3 = TypeOperator(params=3)
List = TypeOperator(params =1)

# Previously, we had types that looked like R1(x), R3(x, y, z), etcetera.
# Everything is now expressed in terms of the R relation and Product/Unit
# types, like R(x, Unit) and R(x * z, y). There are some issues that need to be
# addressed before this fully works, so in the meantime, we use this type
# alias.

R = TypeAlias(lambda x, y: R2(x, y))
C = TypeAlias(lambda x: R1(x))

# Type synonyms ##############################################################

# R1 = TypeAlias(lambda x: R(x, Unit), Val)
# R2 = TypeAlias(lambda x, y: R(x, y), Val, Val)
# R3 = TypeAlias(lambda x, y, z: R(x * z, y), Val, Val, Val)


def with_param(on: Type, x: TypeInstance, at: int = None) -> Constraint:
    return on << tuple(with_parameters(R1, R2, R3, lambda x, y, z: R2(x, y * z),
        param=x, at=at))
    # """
    # Generate a list of instances of relations. The generated relations must
    # contain a certain parameter (at some index, if given).
    # """

    # # This is really hacky due to the fact that we can't have
    # # constraints-in-constraints.
    # c: list[TypeInstance] = []
    # if at is None or at == 1:
    #     c.append(Val * R(x, _))
    #     c.append(R(_, _) * R(x, _))
    #     c.append(Val * R(x * _, _))
    # if at is None or at == 2:
    #     c.append(Val * R(_, x))
    #     c.append(R(_, _) * R(_, x))
    #     c.append(Val * R(_ * x, _))
    #     c.append(Val * R(_, x * _))
    # if at is None or at == 3:
    #     c.append(Val * R(_, _ * x))
    #     c.appene(Val * R(_ * _, x))
    # (x * on)[c]
    # return on


Field = TypeAlias(lambda x: R2(Loc, x))
Amounts = TypeAlias(lambda x: R2(Reg, x) [x <= Qlt])
FieldSample = TypeAlias(R2(Reg, Qlt))
AmountPatches = TypeAlias(R2(Reg, Nom))
PointMeasures = TypeAlias(R2(Reg, Itv))
Coverages = TypeAlias(lambda x: R2(x, Reg) [x <= Qlt])
Contour = TypeAlias(R2(Ord, Reg))
ContourLine = TypeAlias(R2(Itv, Reg))
ObjectExtent = TypeAlias(R2(Obj, Reg))
RelationalField = TypeAlias(lambda x: R3(Loc, x, Loc) [x <= Qlt])
Network = TypeAlias(lambda x: R3(Obj, x, Obj) [x <= Qlt])
ObjectInfo = TypeAlias(lambda x: R2(Obj, Reg * x))  # Associate objects with
# both their extent and some quality

in_ = Operator(type=Nom)
out = Operator(type=Nom)
true = Operator(type=Bool)




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
Position = TypeOperator(supertype=Loc)
Moment = TypeOperator()
Object = TypeOperator(supertype=Obj)
Event = TypeOperator()
#Bool = TypeOperator(supertype=Boo)
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
        R1(Val),
        R2(Reg, Qlt),
        R2(Qlt, Reg),
        R2(Qlt, Qlt),
        R2(Obj, Reg),
        R2(Obj, Qlt),
        R2(Loc, Qlt),
        R2(Obj, Reg * Qlt),
        R3(Obj, Qlt, Obj),
        R3(Loc, Qlt, Obj),
        R3(Loc, Qlt, Loc),
        R3(Obj, Obj, Obj)
    })