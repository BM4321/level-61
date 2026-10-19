"""PY05 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py05.py
"""

def sum_to(n: int) -> int:
    """Return 1 + 2 + ... + n using a loop (0 for n <= 0)."""
    raise NotImplementedError

def factorial(n: int) -> int:
    """Iterative n!; factorial(0) == 1; ValueError for negative n."""
    raise NotImplementedError

def count_multiples(n: int, k: int) -> int:
    """How many of 1..n are divisible by k (use a loop)."""
    raise NotImplementedError

def is_prime(n: int) -> bool:
    """True if n is prime (trial division up to sqrt(n))."""
    raise NotImplementedError

def fizzbuzz(n: int) -> list[str]:
    """List of 'Fizz'/'Buzz'/'FizzBuzz'/number strings for 1..n."""
    raise NotImplementedError

def multiplication_table(n: int) -> str:
    """n x n table, each cell formatted with width 4, rows joined by newlines."""
    raise NotImplementedError

def collatz_steps(n: int) -> int:
    """Steps to reach 1 under the Collatz rule; ValueError if n < 1."""
    raise NotImplementedError

def right_triangle(h: int) -> str:
    """Rows of 1..h stars, no trailing spaces."""
    raise NotImplementedError

def pyramid(h: int) -> str:
    """Centred pyramid: row i has h-i spaces and 2i-1 stars."""
    raise NotImplementedError

def primes_up_to(n: int) -> list[int]:
    """All primes <= n via the Sieve of Eratosthenes."""
    raise NotImplementedError

def fizzbuzz_rules(n: int, rules: list[tuple[int, str]]) -> list[str]:
    """Generalised FizzBuzz: concatenate words for every divisor that divides i."""
    raise NotImplementedError
