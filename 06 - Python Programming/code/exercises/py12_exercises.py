"""PY12 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py12.py
"""

def linear_search(xs: list, target) -> int:
    """Index of first occurrence or -1."""
    raise NotImplementedError

def binary_search(xs: list, target) -> int:
    """Iterative binary search on sorted xs (inclusive bounds); index or -1."""
    raise NotImplementedError

def lower_bound(xs: list, target) -> int:
    """Smallest i with xs[i] >= target (len(xs) if none); like bisect_left."""
    raise NotImplementedError

def upper_bound(xs: list, target) -> int:
    """Smallest i with xs[i] > target (len(xs) if none); like bisect_right."""
    raise NotImplementedError

def count_occurrences(xs: list, target) -> int:
    """Occurrences of target in sorted xs in O(log n)."""
    raise NotImplementedError

def selection_sort(xs: list) -> list:
    """Selection sort (not stable)."""
    raise NotImplementedError

def insertion_sort(xs: list) -> list:
    """Stable insertion sort."""
    raise NotImplementedError

def bubble_sort(xs: list) -> list:
    """Bubble sort with early exit."""
    raise NotImplementedError

def merge(left: list, right: list) -> list:
    """Stable merge of two sorted lists."""
    raise NotImplementedError

def merge_sort(xs: list) -> list:
    """Top-down merge sort."""
    raise NotImplementedError

def count_inversions(xs: list) -> int:
    """Number of pairs i < j with xs[i] > xs[j], in O(n log n)."""
    raise NotImplementedError

def insertion_sort_key_desc(xs: list, key=lambda x: x) -> list:
    """Stable descending insertion sort by key."""
    raise NotImplementedError
