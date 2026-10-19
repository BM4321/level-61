"""PY-07 reference solutions (recursion)."""


def factorial(n: int) -> int:
    """Recursive n!; ValueError if n < 0."""
    if n < 0:
        raise ValueError("n must be >= 0")
    return 1 if n == 0 else n * factorial(n - 1)


def sum_list(xs: list, i: int = 0):
    """Recursive sum of xs[i:] without slicing."""
    if i == len(xs):
        return 0
    return xs[i] + sum_list(xs, i + 1)


def is_palindrome(s: str) -> bool:
    """Recursive palindrome test (exact characters)."""
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and is_palindrome(s[1:-1])


def power(x: float, n: int) -> float:
    """x**n by fast exponentiation (O(log n)); negative n allowed."""
    if n < 0:
        return 1 / power(x, -n)
    if n == 0:
        return 1
    if n % 2 == 0:
        half = power(x, n // 2)
        return half * half
    return x * power(x, n - 1)


def fib_memo(n: int, cache: dict | None = None) -> int:
    """n-th Fibonacci number (fib(0)=0, fib(1)=1) with a memo dictionary."""
    if cache is None:
        cache = {0: 0, 1: 1}
    if n not in cache:
        cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]


def binary_search(xs: list, target, lo: int = 0, hi: int | None = None) -> int:
    """Recursive binary search on sorted xs; index or -1."""
    if hi is None:
        hi = len(xs) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if xs[mid] == target:
        return mid
    if xs[mid] < target:
        return binary_search(xs, target, mid + 1, hi)
    return binary_search(xs, target, lo, mid - 1)


def flatten(nested: list) -> list:
    """Flatten arbitrarily nested lists."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def hanoi(n: int, src: str = "A", aux: str = "B", dst: str = "C") -> list[tuple[str, str]]:
    """List of (from, to) moves solving Towers of Hanoi for n discs."""
    if n == 0:
        return []
    return hanoi(n - 1, src, dst, aux) + [(src, dst)] + hanoi(n - 1, aux, src, dst)


def permutations(s: str) -> list[str]:
    """Sorted list of all orderings of s (distinct characters assumed)."""
    if len(s) <= 1:
        return [s]
    result = []
    for i, c in enumerate(s):
        for rest in permutations(s[:i] + s[i + 1:]):
            result.append(c + rest)
    return sorted(result)


def flatten_depth(nested: list, max_depth: int) -> list:
    """Flatten at most max_depth levels."""
    result = []
    for item in nested:
        if isinstance(item, list) and max_depth > 0:
            result.extend(flatten_depth(item, max_depth - 1))
        else:
            result.append(item)
    return result
