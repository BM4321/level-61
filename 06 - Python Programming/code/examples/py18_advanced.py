"""PY-18: generators, decorators, context managers. Run: python examples/py18_advanced.py"""
import functools


def evens(limit):
    n = 0
    while n < limit:
        yield n
        n += 2


g = evens(5)
print(next(g), next(g), next(g), next(g, "done"))

squares = (x * x for x in range(5))
print(sum(squares), list(squares), "<- exhausted generator")


def logged(func):  # deliberately missing functools.wraps
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def logged_ok(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@logged
def area(w, h):
    """Rectangle area."""
    return w * h


@logged_ok
def area2(w, h):
    """Rectangle area."""
    return w * h


print(area.__name__, area.__doc__, "|", area2.__name__, area2.__doc__)
