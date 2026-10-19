"""Descriptive statistics, implemented by hand for learning (cross-checked against statistics module in tests)."""
import math


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of empty data")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("median of empty data")
    s = sorted(values)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2


def std_dev(values: list[float]) -> float:
    """Population standard deviation."""
    mu = mean(values)
    return math.sqrt(sum((x - mu) ** 2 for x in values) / len(values))


def distribution(grades: list[str], letters: str = "ABCDF") -> dict[str, int]:
    """Count of each letter (all letters present, possibly 0)."""
    counts = {letter: 0 for letter in letters}
    for g in grades:
        counts[g] += 1
    return counts


def rank(results: list[dict]) -> list[dict]:
    """Sort by final mark descending (ties by name) and add 'rank' with shared ranks for ties."""
    ordered = sorted(results, key=lambda r: (-r["final"], r["name"]))
    ranked, previous, current_rank = [], None, 0
    for position, r in enumerate(ordered, start=1):
        if r["final"] != previous:
            current_rank, previous = position, r["final"]
        ranked.append({**r, "rank": current_rank})
    return ranked
