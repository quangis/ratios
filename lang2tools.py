"""This module can be used to turn the operators of a transforge language into 
tools that can be passed to APE. At the time of writing, this is relevant only 
for the <https://github.com/quangis/ratios> project."""

import json
from rdflib.term import URIRef
from transforge import Language
from transforge.type import Type, TypeSchema, TypeInstance
from transforge.expr import Operator
from transforge.namespace import shorten

from ratiotheory import ratiotheory  # type: ignore


def lang2tools(lang: Language, **kwargs: tuple[TypeInstance, ...]) -> dict:
    """
    Convert the operators of a transforge language into a tool annotation 
    dictionary that APE understands.
    """
    functions: list[dict] = []

    if kwargs:
        operators = kwargs
    else:
        operators = {op: () for op in lang.operators.keys()}

    for name, args in operators.items():
        op: Operator = lang.operators[name]
        t: Type = op.type
        ti: TypeInstance
        if args:
            assert isinstance(t, TypeSchema)
            ti = t.schema(*args)
        else:
            ti = t.instance()
        tool: URIRef = lang.uri(op)
        inputs, output = ti.io()
        functions.append({
            'id': str(tool),
            'label': shorten(tool),
            'taxonomyOperations': [tool],
            'inputs': [{lang.namespace.Top: [lang.uri(input)]}
                for input in inputs],
            'outputs': [{lang.namespace.Top: [lang.uri(output)]}],
        })
    return {'functions': functions}


print(json.dumps(lang2tools(ratiotheory), indent=4))
