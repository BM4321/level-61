"""PY-02 exercises. Replace each `raise NotImplementedError` with your code.

Check with:  PY_TARGET=exercises python -m pytest tests/test_py02.py
"""


def celsius_to_fahrenheit(c: float) -> float:
    """Return c converted to Fahrenheit (F = 9/5*C + 32)."""
    raise NotImplementedError


def split_seconds(total: int) -> tuple[int, int, int]:
    """Return (hours, minutes, seconds) for a non-negative number of seconds."""
    raise NotImplementedError


def is_even(n: int) -> bool:
    """Return True if n is even (works for negative n too)."""
    raise NotImplementedError


def vat_inclusive_cents(price_cents: int, rate_percent: int) -> int:
    """Return price plus VAT, in integer cents, VAT rounded half up."""
    raise NotImplementedError


def digit_sum(n: int) -> int:
    """Sum of decimal digits of n >= 0 using only // and %. Raise ValueError if n < 0."""
    raise NotImplementedError


def format_duration(seconds: int) -> str:
    """'2h 03m 04s', '3m 04s' or '4s'. Raise ValueError for negative input."""
    raise NotImplementedError
