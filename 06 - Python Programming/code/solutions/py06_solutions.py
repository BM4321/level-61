"""PY-06 reference solutions."""


def average(values: list[float]) -> float:
    """Arithmetic mean of a non-empty list; ValueError if empty."""
    if not values:
        raise ValueError("average of empty list")
    return sum(values) / len(values)


def clamp(x: float, low: float, high: float) -> float:
    """Limit x to [low, high]; ValueError if low > high."""
    if low > high:
        raise ValueError("low must be <= high")
    return max(low, min(x, high))


def add_item(item, basket=None) -> list:
    """Append item to basket (a NEW list when basket is omitted) and return it."""
    if basket is None:
        basket = []
    basket.append(item)
    return basket


def min_max_mean(values: list[float]) -> tuple[float, float, float]:
    """Return (min, max, mean); ValueError on empty input."""
    if not values:
        raise ValueError("empty input")
    return min(values), max(values), sum(values) / len(values)


def apply_discount(price: float, *, percent: float = 0, fixed: float = 0) -> float:
    """Apply percent off, then subtract fixed; never below 0. Keyword-only options."""
    return max(0.0, price * (1 - percent / 100) - fixed)


def make_counter(start: int = 0, step: int = 1):
    """Return a function that returns start+step, start+2*step, ... on successive calls."""
    count = start

    def counter() -> int:
        nonlocal count
        count += step
        return count

    return counter


def compose(*funcs):
    """compose(f, g)(x) == f(g(x)); compose() is the identity function."""
    def composed(x):
        result = x
        for f in reversed(funcs):
            result = f(result)
        return result

    return composed


def validate(value, rules) -> list[str]:
    """Return messages of all (check, message) rules whose check(value) is falsy."""
    return [message for check, message in rules if not check(value)]
