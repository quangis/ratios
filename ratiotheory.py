from transforge.type import Type, Constraint, \
    TypeInstance, TypeAlias, TypeOperator, \
    with_parameters, _, Top
from transforge.lang import Language
from transforge.expr import Operator, Source


#cct
# Types ######################################################################

Val = TypeOperator()
#Obj = TypeOperator(supertype=Val)  # O
# Reg = TypeOperator(supertype=Val)  # S
# Loc = TypeOperator(supertype=Val)  # L
Qlt = TypeOperator(supertype=Val)  # Q
Nom = TypeOperator(supertype=Qlt)
Bool = TypeOperator(supertype=Nom)
# Ord = TypeOperator(supertype=Nom)
# Itv = TypeOperator(supertype=Ord)
# Ratio = TypeOperator(supertype=Itv)
# Count = TypeOperator(supertype=Ratio)
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

ObjectInfo = TypeAlias(lambda x: R2(Object, Region * x))

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
    "amounts can be part of each other",
    type= lambda x: x ** x ** Bool[x <= Amount(_)]
)
intersect = Operator(
    "intersect amounts (meet)",
    type=lambda x: x ** x ** x [x <= Amount(_)]
)
union = Operator(
    "unify amounts (join)",
    type=lambda x: x ** x ** x [x <= Amount(_)]
)

# consIntersect = Operator(
#     "constructs a quantified relation of intersections of regions (excluding empty intersections)",
#     type=lambda x,y: R2(x, Region) ** R2(y, Region) ** R3(x, Region, y),
#     body=lambda x, y: select (compose(notj,empty))(prod3(prod(intersect, x, y)))
# )

amount2rel = Operator(
    'convert amounts into relations',
    type=lambda x: Amount(x) ** R1(x)
)
rel2amount = Operator(
    'convert amounts into relations',
    type=lambda x: R1(x) ** Amount(x)
)
invert = Operator(
    "invert a field, generating a coverage",
    type=lambda x: R2(Position, x) ** R2(x, Region),
    body=lambda x: groupby(rel2amount, x)
)
revert = Operator(
    "revert a coverage into a field",
    type=lambda x: R2(x, Region) ** R2(Position, x)#,
    #body=lambda x:
)

consproportion = Operator(
    'construct proportions from an Amount - Archimedean relation',
    type=lambda x, y: R2(x,y) ** R2(x,Proportion(y,Archimedean(x))) [x << Amount(_), y << Archimedean(_)],
    body=lambda x: apply2(ratio,(apply(measure,pi1(x))),x)
)
consarchimed = Operator(
    "construct archimedean magnitudes from an Amount - Proportion relation",
    type=lambda x, y: R2(x,Proportion(y,Archimedean(x))) ** R2(x,y) [x << Amount(_), y << Archimedean(_)],
    body=lambda x: apply2(multiply,x,(apply(measure,pi1(x))))
)

arealinterpol = Operator(
    "areal interpolation",
    type=lambda x: R2(Region, x) ** R1(Region) ** R2(Region, x) [x <= Proportion(_,Size)]#,
    #body = lambda x, y: pi1(x)
)


# Language ###################################################################


###
from cct import cct
#--------------------------


in_ = Operator(type=Nom)
out = Operator(type=Nom)
true = Operator(type=Bool)
############Relational operators
add = Operator(
    "add value to unary relation",
    type=lambda x: R1(x) ** x ** R1(x),
)
get = Operator(
    "get some value from unary relation",
    type=lambda x: R1(x) ** x
)
getregionqualities = Operator(
    "get region-based qualities from object qualities",
    type=lambda x: ObjectInfo(x) ** R2(Region, x),
    body=lambda x: join(groupby(get, get_attrL(x)), get_attrR(x))
)


# Functional and relational transformations ###############################

conj = Operator(
    "conjunction",
    type=Bool ** Bool ** Bool
)
notj = Operator(
    "logical negation",
    type=Bool ** Bool
)
disj = Operator(
    "disjunction",
    type=Bool ** Bool ** Bool,
    body=lambda x: compose2(notj, conj, x)
)
empty = Operator(
    "empty relation",
    type=lambda rel: rel ** Bool
)
# Functional operators

compose = Operator(
    "compose unary functions",
    type=lambda α, β, γ: (β ** γ) ** (α ** β) ** (α ** γ),
    body=lambda f, g, x: f(g(x))
)
compose2 = Operator(
    "compose binary functions",
    type=lambda α, β, γ, δ: (β ** γ) ** (δ ** α ** β) ** (δ ** α ** γ),
    body=lambda f, g, x, y: f(g(x, y))
)
swap = Operator(
    "swap binary function inputs",
    type=lambda α, β, γ: (α ** β ** γ) ** (β ** α ** γ),
    body=lambda f, x, y: f(y, x)
)
id_ = Operator(
    "identity",
    type=lambda α: α ** α,
    body=lambda x: x
)
apply = Operator(
    "applying a function to a collection",
    type=lambda x, y: (x ** y) ** R1(x) ** R2(x, y)
)

# Set operations

# This should be a single operator, nest: R(x, y)
addlist=Operator(
    "construct a list",
    type=lambda x: List(x) ** x ** List(x)
)
emptylist = Operator(
    "empty list",
    type=lambda x:List(x)
)
nest = Operator(
    "put value in unary relation",
    type=lambda x: x ** R1(x)
)
nest2 = Operator(
    "put values in binary relation",
    type=lambda x, y: x ** y ** R2(x, y)
)
nest3 = Operator(
    "put values in ternary relation",
    type=lambda x, y, z: x ** y ** z ** R3(x, y, z)
)
consTuple = Operator(
    "put values in ternary relation",
    type=lambda x, y, z: R2(x, y) ** R2(x, z)** R2(x, y * z)
)
# There should be an empty relation operator
# This should have both key and value, and the relation should come last
add = Operator(
    "add value to unary relation",
    type=lambda x: R1(x) ** x ** R1(x),
)
get = Operator(
    "get some value from unary relation",
    type=lambda x: R1(x) ** x
)
inrel = Operator(
    "whether some value is in a relation",
    type=lambda x: x ** R1(x) ** Bool,
)
set_union = Operator(
    "union of two relations",
    type=lambda rel: rel ** rel ** rel,
    body=lambda x, y: relunion(add(nest(x), y))
)
set_diff = Operator(
    "difference of two relations",
    type=lambda rel: rel ** rel ** rel
)
set_inters = Operator(
    "intersection of two relations",
    type=lambda rel: rel ** rel ** rel,
    body=lambda x, y: set_diff(x, set_diff(x, y))
)
relunion = Operator(
    "union of a set of relations",
    type=lambda rel: R1(rel) ** rel [rel << {R1(_), R2(_, _), R3(_, _, _)}]
)
prod = Operator(
    "A constructor for quantified relations. Prod generates a cartesian "
    "product of two relations as a nested binary relation.",
    type=lambda x, y, z, u, w:
        (y ** z ** u) ** R2(x, y) ** R2(w, z) ** R2(x, R2(w, u)),
    body=lambda f, x, y: apply1(compose(swap(apply1, y), f), x)
)
prod3 = Operator(
    doc=("prod3 generates a quantified relation from two nested binary "
         "relations. The keys of the nested relations become two keys of "
         "the quantified relation."),
    type=lambda x, y, z: R2(z, R2(x, y)) ** R3(x, y, z),
)
prod_3 = Operator(
    doc=("prod_3 is the inverse of prod3."),
    type=lambda x, y, z: R3(x, y, z) ** R2(z, R2(x, y)),
)

# Projection (π)

pi1 = Operator(
    "projects a given relation to the first attribute, resulting in a "
    "collection",
    type=lambda rel, x: rel ** R1(x) [with_param(rel, x, at=1)]
)
pi2 = Operator(
    "projects a given relation to the second attribute, resulting in a "
    "collection",
    type=lambda rel, x: rel ** R1(x) [with_param(rel, x, at=2)],
)
pi3 = Operator(
    "projects a given ternary relation to the third attribute, resulting "
    "in a collection",
    type=lambda x: R3(_, _, x) ** R1(x)
)
pi12 = Operator(
    "projects a given ternary relation to the first two attributes",
    type=lambda x, y: R3(x, y, _) ** R2(x, y)
)
pi23 = Operator(
    "projects a given ternary relation to the last two attributes",
    type=lambda x, y: R3(_, x, y) ** R2(x, y)
)

# Selection (σ)

select = Operator(
    "Selects a subset of a relation using a constraint on one attribute, like "
    "equality (eq) or order (leq)",
    type=lambda x, y, rel:
        (x ** y ** Bool) ** rel ** y ** rel [with_param(rel, x)]
)
subset = Operator(
    "Subset a relation to those tuples having an attribute value contained in "
    "a collection",
    type=lambda x, rel: rel ** R1(x) ** rel [with_param(rel, x)],
    body=lambda r, c: select(inrel, r, c)
)

select2 = Operator(
    "Selects a subset of a relation using a constraint on two attributes, "
    "like equality (eq) or order (leq)",
    type=lambda x, y, rel:
        (x ** y ** Bool) ** rel ** rel [with_param(rel, y), with_param(rel, x)]
)

# remove nest
# empty: R(x, y)
# keys: R(x, y) -> R(x, ())
# values: R(x, y) -> R(y, ())
# map: (y -> z) -> R(x, y) -> R(x, z)
# left: x * _ -> x
# right: _ * x -> x

# Join (⨝)
join = Operator(
    "Join of two unary concepts, like a table join",
    type=lambda x, y, z: R2(x, y) ** R2(y, z) ** R2(x, z)
)

# functions to handle multiple attributes (with 1 key)
join_attr = Operator(
    type=lambda x, y, z: R2(x, y) ** R2(x, z) ** R2(x, y * z),
    # body=lambda x1, x2: prod3(pi12(select2(
    #     eq,
    #     prod3(apply1(compose(swap(apply1, x1), nest2), x2))
    # )))
)
get_attrL = Operator(
    type=lambda x, y, z: R2(x, y * z) ** R2(x, y),
    body=None
)
get_attrR = Operator(
    type=lambda x, y, z: R2(x, y * z) ** R2(x, z),
    body=None
)

join_key = Operator(
    "Substitute the quality of a quantified relation to some quality of one "
    "of its keys.",
    type=lambda x, q1, y, rel, q2:
        R3(x, q1, y) ** rel ** R3(x, q2, y) [rel << {R2(x, q2), R2(y, q2)}],
    # body=lambda x, y: prod3(apply1(subset(y), groupbyL(pi1, x)))
)

apply1 = Operator(
    "Join with unary function. Generates a unary concept from one other "
    "unary concept using a function",
    type=lambda x1, x2, y:
        (x1 ** x2) ** R2(y, x1) ** R2(y, x2),
    body=lambda f, y: join(y, apply(f, pi2(y)))
)
apply2 = Operator(
    "Join with binary function. Generates a unary concept from two other "
    "unary concepts of the same type",
    type=lambda x1, x2, x3, y:
        (x1 ** x2 ** x3) ** R2(y, x1) ** R2(y, x2) ** R2(y, x3),
    body=lambda f, x, y: pi12(select2(eq, prod3(prod(f, x, y))))
)

groupbyL = Operator(
    "Group quantified relations by the left key, summarizing lists of "
    "quality values with the same key value into a new value per key, "
    "resulting in a unary concept.",
    type=lambda rel, l, q1, q2, r:
        (rel ** q2) ** R3(l, q1, r) ** R2(l, q2) [rel << {R1(r), R2(r, q1)}],
)
groupbyR = Operator(
    "Group quantified relations by the right key, summarizing lists of "
    "quality values with the same key value into a new value per key, "
    "resulting in a unary concept.",
    type=lambda rel, q2, l, q1, r:
        (rel ** q2) ** R3(l, q1, r) ** R2(r, q2) [rel << {R1(l), R2(l, q1)}]
)
groupby = Operator(
    "Group by qualities of binary relations",
    type=lambda l, q, y:
        (R1(l) ** q) ** R2(l, y) ** R2(y, q),
)

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
ObjectDensity,
EventDensity,
MassDensity,
ObjectFrequency,
EventFrequency
        # R1(Val),
        # R2(Reg, Qlt),
        # R2(Qlt, Reg),
        # R2(Qlt, Qlt),
        # R2(Obj, Reg),
        # R2(Obj, Qlt),
        # R2(Loc, Qlt),
        # R2(Obj, Reg * Qlt),
        # R3(Obj, Qlt, Obj),
        # R3(Loc, Qlt, Obj),
        # R3(Loc, Qlt, Loc),
        # R3(Obj, Obj, Obj)
    })
