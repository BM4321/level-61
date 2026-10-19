import random

import pytest

from _target import load

m = load("py08")


@pytest.mark.parametrize("marks, expected", [([70, 85, 60], 70), ([85, 85, 70], 70), ([50], None),
                                             ([], None), ([40, 40], None), ([-5, -1, -3], -3)])
def test_second_largest(marks, expected):
    assert m.second_largest(marks) == expected


def test_rle():
    assert m.run_length_encode("aaabccdddd") == "a3b1c2d4"
    assert m.run_length_encode("") == ""
    assert m.run_length_encode("ab") == "a1b1"
    assert m.run_length_decode("a12b1") == "a" * 12 + "b"


def test_rle_round_trip():
    rng = random.Random(6)
    for _ in range(200):
        s = "".join(rng.choice("xyz") for _ in range(rng.randint(0, 30)))
        assert m.run_length_decode(m.run_length_encode(s)) == s


def test_first_duplicate():
    assert m.first_duplicate([3, 1, 4, 1, 5, 3]) == 1
    assert m.first_duplicate([1, 2, 3]) is None
    assert m.first_duplicate([]) is None


def test_merge_sorted():
    assert m.merge_sorted([1, 4, 9], [2, 3, 10, 11]) == [1, 2, 3, 4, 9, 10, 11]
    assert m.merge_sorted([], [1]) == [1]
    rng = random.Random(1)
    a = sorted(rng.sample(range(100), 20))
    b = sorted(rng.sample(range(100), 15))
    assert m.merge_sorted(a, b) == sorted(a + b)


def test_greedy_change():
    assert m.greedy_change(30, [1, 5, 10, 25]) == [25, 5]
    assert m.greedy_change(6, [1, 3, 4]) == [4, 1, 1]
    assert len(m.greedy_change(14, [1, 7, 10])) == 5
    with pytest.raises(ValueError):
        m.greedy_change(3, [2])


def test_min_coins():
    assert m.min_coins(6, [1, 3, 4]) == 2
    assert m.min_coins(14, [1, 7, 10]) == 2
    assert m.min_coins(3, [2]) is None
    assert m.min_coins(0, [1]) == 0


@pytest.mark.parametrize("n", [0, 1, 2, 13, 255, 1024])
def test_to_binary(n):
    assert m.to_binary(n) == bin(n)[2:]
