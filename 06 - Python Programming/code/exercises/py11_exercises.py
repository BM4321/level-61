"""PY11 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py11.py
"""

import string
from collections import Counter

def word_counts(text: str) -> dict[str, int]:
    """Lower-cased word frequencies with surrounding punctuation stripped."""
    raise NotImplementedError

def common(a: list, b: list) -> list:
    """Elements of a also in b, in a's order, without duplicates, O(n + m)."""
    raise NotImplementedError

def invert(d: dict) -> dict:
    """Map each value to a sorted list of the keys that had it."""
    raise NotImplementedError

def average_by_group(rows: list[tuple[str, str, float]]) -> dict[str, float]:
    """rows of (name, group, mark) -> {group: mean mark}."""
    raise NotImplementedError

def squares_of_evens(xs: list[int]) -> list[int]:
    """[x*x for even x], via a comprehension."""
    raise NotImplementedError

def passing(marks: dict[str, float], threshold: float=50) -> dict[str, float]:
    """Sub-dict of entries with mark >= threshold."""
    raise NotImplementedError

def most_frequent(xs: list):
    """Most common item, ties broken by first appearance; ValueError if empty."""
    raise NotImplementedError

def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Indices (i, j), i < j, with nums[i] + nums[j] == target, in O(n); else None."""
    raise NotImplementedError

def only_one_course(reg: dict[str, set[str]]) -> set[str]:
    """IDs that appear in exactly one course's set."""
    raise NotImplementedError

def _words(text: str) -> set[str]:
    raise NotImplementedError

def build_index(docs: dict[str, str]) -> dict[str, set[str]]:
    """Inverted index: word -> set of doc ids containing it."""
    raise NotImplementedError

def search(index: dict[str, set[str]], query: str) -> set[str]:
    """Doc ids containing ALL query words (case-insensitive)."""
    raise NotImplementedError
