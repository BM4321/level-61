import itertools
import math

import pytest

from _target import load

m = load("py07")


def test_factorial():
    assert [m.factorial(k) for k in range(6)] == [1, 1, 2, 6, 24, 120]
    with pytest.raises(ValueError):
        m.factorial(-2)


def test_sum_list():
    assert m.sum_list([]) == 0
    assert m.sum_list([4, 9, 1]) == 14
    assert m.sum_list(list(range(500))) == sum(range(500))


@pytest.mark.parametrize("s, ok", [("", True), ("a", True), ("abba", True), ("racecar", True), ("abca", False)])
def test_is_palindrome(s, ok):
    assert m.is_palindrome(s) is ok


def test_power():
    assert m.power(2, 10) == 1024
    assert m.power(3, 0) == 1
    assert math.isclose(m.power(2, -2), 0.25)
    assert m.power(7, 13) == 7 ** 13


def test_fib_memo():
    assert [m.fib_memo(k) for k in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert m.fib_memo(90) == 2880067194370816120


def test_binary_search():
    xs = [1, 3, 5, 7, 9, 11]
    for i, x in enumerate(xs):
        assert m.binary_search(xs, x) == i
    assert m.binary_search(xs, 4) == -1
    assert m.binary_search([], 1) == -1


def test_flatten():
    assert m.flatten([1, [2, [3, 4]], [], 5]) == [1, 2, 3, 4, 5]
    assert m.flatten([]) == []


@pytest.mark.parametrize("n", range(0, 11))
def test_hanoi_count(n):
    assert len(m.hanoi(n)) == 2 ** n - 1


def test_hanoi_valid_moves():
    pegs = {"A": [3, 2, 1], "B": [], "C": []}
    for src, dst in m.hanoi(3):
        disc = pegs[src].pop()
        assert not pegs[dst] or pegs[dst][-1] > disc
        pegs[dst].append(disc)
    assert pegs["C"] == [3, 2, 1]


def test_permutations():
    assert m.permutations("abc") == ["abc", "acb", "bac", "bca", "cab", "cba"]
    assert m.permutations("abcd") == sorted("".join(p) for p in itertools.permutations("abcd"))


def test_flatten_depth():
    assert m.flatten_depth([1, [2, [3, [4]]]], 1) == [1, 2, [3, [4]]]
    assert m.flatten_depth([1, [2, [3, [4]]]], 0) == [1, [2, [3, [4]]]]
