"""PY-07: recursion, call counting and memoisation. Run: python examples/py07_recursion.py"""
import sys
from functools import cache

calls = 0


def fib_naive(n: int) -> int:
    global calls  # used only to count calls for this demonstration
    calls += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)


@cache
def fib_cached(n: int) -> int:
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)


for n in (5, 10, 20, 25):
    calls = 0
    value = fib_naive(n)
    print(f"fib({n}) = {value:>6}  naive calls = {calls}")
print("fib_cached(90) =", fib_cached(90))
print("recursion limit:", sys.getrecursionlimit())
