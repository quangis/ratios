"""This module can be used to turn the operators of a transforge language into 
tools that can be passed to APE. At the time of writing, this is relevant only 
for the <https://github.com/quangis/ratios> project."""

import json
from sys import stderr
from transforge import Language
from transforge.type import TypingError, TypeSchema, TypeInstance, Top, Bottom
from transforge.namespace import shorten
from itertools import product, chain
from typing import Iterator, Iterable

from ratiotheory import ratiotheory  # type: ignore


def variants(ts: TypeSchema, canon: set[TypeInstance])\
        -> Iterator[TypeInstance]:
    """Produce concrete variants of a function type schema, in such a way that 
    the inputs and outputs are canonical types."""
    for types in product(*(canon for _ in range(ts.n))):
        try:
            candidate = ts.schema(*types)
        except TypingError:
            continue
        if all(t in canon for t in chain(*candidate.io())):
            yield candidate


def lang2tools(lang: Language) -> dict:
    """Convert the operators of a transforge language into a tool annotation 
    dictionary that APE understands."""
    functions: list[dict] = []

    top, bottom = Top(), Bottom()
    canon: set[TypeInstance] = set(t for t in lang.canon
        if top not in t and bottom not in t)

    for name, op in lang.operators.items():
        tis: Iterable[TypeInstance]
        if isinstance(op.type, TypeSchema):
            tis = variants(op.type, canon)
        else:
            tis = (op.type.instance(),)
        any_variants = False
        for i, ti in enumerate(tis):
            any_variants = True
            tool = f"{lang.uri(op)}{i}"
            inputs, output = ti.io()
            functions.append({
                'id': tool,
                'label': shorten(tool),
                'taxonomyOperations': [tool],
                'inputs': [{lang.namespace.Top: [lang.uri(input)]}
                    for input in inputs],
                'outputs': [{lang.namespace.Top: [lang.uri(output)]}],
            })
        if not any_variants:
            print(f"Warning: {name} has no variants", file=stderr)
    return {'functions': functions}


if __name__ == "__main__":
    print(json.dumps(lang2tools(ratiotheory), indent=4))
