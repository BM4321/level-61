"""PY07 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py07.py
"""

def factorial(n: int) -> int:
    """Recursive n!; ValueError if n < 0."""
    raise NotImplementedError

def sum_list(xs: list, i: int=0):
    """Recursive sum of xs[i:] without slicing."""
    raise NotImplementedError

def is_palindrome(s: str) -> bool:
    """Recursive palindrome test (exact characters)."""
    raise NotImplementedError

def power(x: float, n: int) -> float:
    """x**n by fast exponentiation (O(log n)); negative n allowed."""
    raise NotImplementedError

def fib_memo(n: int, cache: dict | None=None) -> int:
    """n-th Fibonacci number (fib(0)=0, fib(1)=1) with a memo dictionary."""
    raise NotImplementedError

def binary_search(xs: list, target, lo: int=0, hi: int | None=None) -> int:
    """Recursive binary search on sorted xs; index or -1."""
    raise NotImplementedError

def flatten(nested: list) -> list:
    """Flatten arbitrarily nested lists."""
    raise NotImplementedError

def hanoi(n: int, src: str='A', aux: str='B', dst: str='C') -> list[tuple[str, str]]:
    """List of (from, to) moves solving Towers of Hanoi for n discs."""
    raise NotImplementedError

def permutations(s: str) -> list[str]:
    """Sorted list of all orderings of s (distinct characters assumed)."""
    raise NotImplementedError

def flatten_depth(nested: list, max_depth: int) -> list:
    """Flatten at most max_depth levels."""
    raise NotImplementedError
