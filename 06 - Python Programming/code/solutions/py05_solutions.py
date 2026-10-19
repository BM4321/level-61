"""PY-05 reference solutions."""


def sum_to(n: int) -> int:
    """Return 1 + 2 + ... + n using a loop (0 for n <= 0)."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def factorial(n: int) -> int:
    """Iterative n!; factorial(0) == 1; ValueError for negative n."""
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def count_multiples(n: int, k: int) -> int:
    """How many of 1..n are divisible by k (use a loop)."""
    count = 0
    for i in range(1, n + 1):
        if i % k == 0:
            count += 1
    return count


def is_prime(n: int) -> bool:
    """True if n is prime (trial division up to sqrt(n))."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def fizzbuzz(n: int) -> list[str]:
    """List of 'Fizz'/'Buzz'/'FizzBuzz'/number strings for 1..n."""
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out


def multiplication_table(n: int) -> str:
    """n x n table, each cell formatted with width 4, rows joined by newlines."""
    rows = []
    for i in range(1, n + 1):
        cells = []
        for j in range(1, n + 1):
            cells.append(f"{i * j:4d}")
        rows.append("".join(cells))
    return "\n".join(rows)


def collatz_steps(n: int) -> int:
    """Steps to reach 1 under the Collatz rule; ValueError if n < 1."""
    if n < 1:
        raise ValueError("n must be >= 1")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def right_triangle(h: int) -> str:
    """Rows of 1..h stars, no trailing spaces."""
    return "\n".join("*" * i for i in range(1, h + 1))


def pyramid(h: int) -> str:
    """Centred pyramid: row i has h-i spaces and 2i-1 stars."""
    rows = []
    for i in range(1, h + 1):
        rows.append(" " * (h - i) + "*" * (2 * i - 1))
    return "\n".join(rows)


def primes_up_to(n: int) -> list[int]:
    """All primes <= n via the Sieve of Eratosthenes."""
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    p = 2
    while p * p <= n:
        if is_p[p]:
            for multiple in range(p * p, n + 1, p):
                is_p[multiple] = False
        p += 1
    return [i for i in range(n + 1) if is_p[i]]


def fizzbuzz_rules(n: int, rules: list[tuple[int, str]]) -> list[str]:
    """Generalised FizzBuzz: concatenate words for every divisor that divides i."""
    out = []
    for i in range(1, n + 1):
        word = "".join(w for d, w in rules if i % d == 0)
        out.append(word or str(i))
    return out
