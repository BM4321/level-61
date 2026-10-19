"""PY13 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py13.py
"""

import importlib
import operator
_OPS = {'==': operator.eq, '!=': operator.ne, '>=': operator.ge, '<=': operator.le, '>': operator.gt, '<': operator.lt}

def parse_requirement(line: str) -> tuple[str, str] | None:
    """'requests==2.32.3' -> ('requests', '==2.32.3'); None for blank/comment lines."""
    raise NotImplementedError

def read_requirements(text: str) -> dict[str, str]:
    """Lower-cased name -> specifier; ValueError on duplicate names."""
    raise NotImplementedError

def import_by_name(dotted: str):
    """'math.sqrt' -> the object; ValueError if no module part."""
    raise NotImplementedError

def version_tuple(v: str) -> tuple[int, ...]:
    """'1.10.2' -> (1, 10, 2)."""
    raise NotImplementedError

def satisfies(version: str, spec: str) -> bool:
    """Single-operator check, e.g. satisfies('1.10', '>=1.9') -> True."""
    raise NotImplementedError
