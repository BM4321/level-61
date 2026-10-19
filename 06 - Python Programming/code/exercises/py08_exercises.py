"""PY08 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py08.py
"""

def second_largest(marks: list[float]) -> float | None:
    """Second-highest DISTINCT value, or None."""
    raise NotImplementedError

def run_length_encode(s: str) -> str:
    """'aaabccdddd' -> 'a3b1c2d4'."""
    raise NotImplementedError

def run_length_decode(s: str) -> str:
    """'a12b1' -> 'aaaaaaaaaaaab' (counts may have several digits)."""
    raise NotImplementedError

def first_duplicate(xs: list):
    """First element seen a second time scanning left to right, else None."""
    raise NotImplementedError

def merge_sorted(a: list, b: list) -> list:
    """Merge two sorted lists in O(len(a) + len(b))."""
    raise NotImplementedError

def greedy_change(amount: int, coins: list[int]) -> list[int]:
    """Largest-coin-first change; ValueError if exact change impossible."""
    raise NotImplementedError

def min_coins(amount: int, coins: list[int]) -> int | None:
    """Optimal coin count by dynamic programming, None if impossible."""
    raise NotImplementedError

def to_binary(n: int) -> str:
    """Binary digits of n >= 0 via repeated division ('0' for n == 0)."""
    raise NotImplementedError
