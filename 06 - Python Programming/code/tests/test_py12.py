import bisect
import itertools
import random

import pytest

from _target import load

m = load("py12")
rng = random.Random(12)
CASES = [[], [1], [2, 1], [5, 2, 4, 1], [3, 3, 1, 2, 3], list(range(20, 0, -1))] + \
        [[rng.randint(-50, 50) for _ in range(rng.randint(0, 60))] for _ in range(30)]


def test_linear_search():
    assert m.linear_search([4, 2, 2], 2) == 1
    assert m.linear_search([], 1) == -1


def test_binary_search():
    xs = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert m.binary_search(xs, 23) == 5
    for i, x in enumerate(xs):
        assert m.binary_search(xs, x) == i
    for missing in (0, 4, 99):
        assert m.binary_search(xs, missing) == -1
    assert m.binary_search([], 1) == -1


@pytest.mark.parametrize("xs", CASES)
def test_bounds_match_bisect(xs):
    s = sorted(xs)
    for t in range(-52, 53, 7):
        assert m.lower_bound(s, t) == bisect.bisect_left(s, t)
        assert m.upper_bound(s, t) == bisect.bisect_right(s, t)
        assert m.count_occurrences(s, t) == s.count(t)


@pytest.mark.parametrize("sort_name", ["selection_sort", "insertion_sort", "bubble_sort", "merge_sort"])
@pytest.mark.parametrize("xs", CASES)
def test_sorts(sort_name, xs):
    original = xs[:]
    assert getattr(m, sort_name)(xs) == sorted(xs)
    assert xs == original  # input not mutated


def test_stability():
    records = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]

    class K:  # compares only on the number
        def __init__(self, r):
            self.r = r

        def __lt__(self, o):
            return self.r[0] < o.r[0]

        def __gt__(self, o):
            return self.r[0] > o.r[0]

        def __le__(self, o):
            return self.r[0] <= o.r[0]

    for name in ("insertion_sort", "bubble_sort", "merge_sort"):
        out = [k.r for k in getattr(m, name)([K(r) for r in records])]
        assert out == [(0, "b"), (0, "d"), (1, "a"), (1, "c")], name


@pytest.mark.parametrize("xs", CASES[:12])
def test_count_inversions(xs):
    brute = sum(1 for i, j in itertools.combinations(range(len(xs)), 2) if xs[i] > xs[j])
    assert m.count_inversions(xs) == brute
    assert m.count_inversions([4, 3, 1, 2]) == 5


def test_insertion_sort_key_desc():
    data = [("Ali", 71), ("Bea", 88), ("Chen", 71)]
    assert m.insertion_sort_key_desc(data, key=lambda s: s[1]) == [("Bea", 88), ("Ali", 71), ("Chen", 71)]
