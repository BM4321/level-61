"""PY06 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py06.py
"""

def average(values: list[float]) -> float:
    """Arithmetic mean of a non-empty list; ValueError if empty."""
    raise NotImplementedError

def clamp(x: float, low: float, high: float) -> float:
    """Limit x to [low, high]; ValueError if low > high."""
    raise NotImplementedError

def add_item(item, basket=None) -> list:
    """Append item to basket (a NEW list when basket is omitted) and return it."""
    raise NotImplementedError

def min_max_mean(values: list[float]) -> tuple[float, float, float]:
    """Return (min, max, mean); ValueError on empty input."""
    raise NotImplementedError

def apply_discount(price: float, *, percent: float=0, fixed: float=0) -> float:
    """Apply percent off, then subtract fixed; never below 0. Keyword-only options."""
    raise NotImplementedError

def make_counter(start: int=0, step: int=1):
    """Return a function that returns start+step, start+2*step, ... on successive calls."""
    raise NotImplementedError

def compose(*funcs):
    """compose(f, g)(x) == f(g(x)); compose() is the identity function."""
    raise NotImplementedError

def validate(value, rules) -> list[str]:
    """Return messages of all (check, message) rules whose check(value) is falsy."""
    raise NotImplementedError
