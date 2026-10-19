"""PY20 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py20.py
"""

ROMAN = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
VALUES = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def int_to_roman(n: int, lowercase: bool=False) -> str:
    """1..3999 -> canonical Roman numeral; ValueError outside the range."""
    raise NotImplementedError

def roman_to_int(s: str) -> int:
    """Canonical Roman numeral -> int; ValueError for invalid or non-canonical input."""
    raise NotImplementedError

def average_passing(marks: list[float], pass_mark: float=50) -> float:
    """Mean of marks >= pass_mark; ValueError if none pass."""
    raise NotImplementedError

def password_issues(pw: str, common: set[str]) -> list[str]:
    """List of problems: 'too short' (<12), 'no digit', 'no letter', 'too common'."""
    raise NotImplementedError
