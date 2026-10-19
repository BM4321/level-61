import math

import pytest

from _target import load

m = load("py10")


def test_running_total():
    assert m.running_total([5, 3, 2]) == [5, 8, 10]
    assert m.running_total([]) == []


def test_median_does_not_mutate():
    data = [4, 1, 3, 2]
    assert m.median(data) == 2.5
    assert data == [4, 1, 3, 2]
    assert m.median([3, 1, 2]) == 2
    with pytest.raises(ValueError):
        m.median([])


def test_dedupe():
    data = [1, 2, 1, 2, 1, 3]
    assert m.dedupe(data) == [1, 2, 3]
    assert data == [1, 2, 1, 2, 1, 3]
    assert m.dedupe([]) == []


@pytest.mark.parametrize("k, expected", [(2, [4, 5, 1, 2, 3]), (-1, [2, 3, 4, 5, 1]), (0, [1, 2, 3, 4, 5]),
                                         (7, [4, 5, 1, 2, 3])])
def test_rotate(k, expected):
    xs = [1, 2, 3, 4, 5]
    out = m.rotate(xs, k)
    assert out == expected and out is not xs
    assert m.rotate([], 3) == []


def test_chunk():
    assert m.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert m.chunk([], 3) == []
    with pytest.raises(ValueError):
        m.chunk([1], 0)


def test_matrix_ops():
    t = [[70, 65, 80], [55, 75, 60], [90, 85, 95]]
    avg = m.column_averages(t)
    assert all(math.isclose(a, b) for a, b in zip(avg, [215 / 3, 75.0, 235 / 3]))
    assert m.transpose(t) == [[70, 55, 90], [65, 75, 85], [80, 60, 95]]
    with pytest.raises(ValueError):
        m.transpose([[1, 2], [3]])


def test_top_n():
    s = [("Chen", 71), ("Bea", 88), ("Ali", 71), ("Dan", 50)]
    assert m.top_n(s, 3) == [("Bea", 88), ("Ali", 71), ("Chen", 71)]


def test_reshape_round_trip():
    grid = [[1, 2, 3], [4, 5, 6]]
    assert m.reshape(m.flatten_matrix(grid), 2, 3) == grid
    with pytest.raises(ValueError):
        m.reshape([1, 2, 3], 2, 2)


def test_sliding_window():
    assert m.sliding_window([1, 2, 3, 4], 2) == [[1, 2], [2, 3], [3, 4]]
    assert m.sliding_window([1], 3) == []
