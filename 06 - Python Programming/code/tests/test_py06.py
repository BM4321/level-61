import math

import pytest

from _target import load

m = load("py06")


def test_average():
    assert m.average([70, 80]) == 75
    assert m.average([5]) == 5
    with pytest.raises(ValueError):
        m.average([])


def test_clamp():
    assert m.clamp(5, 0, 10) == 5
    assert m.clamp(-3, 0, 10) == 0
    assert m.clamp(30, 0, 10) == 10
    with pytest.raises(ValueError):
        m.clamp(1, 10, 0)


def test_add_item_does_not_share_default():
    assert m.add_item("pen") == ["pen"]
    assert m.add_item("book") == ["book"]
    mine = ["x"]
    assert m.add_item("y", mine) is mine and mine == ["x", "y"]


def test_min_max_mean():
    lo, hi, mean = m.min_max_mean([4, 9, 1])
    assert (lo, hi) == (1, 9) and math.isclose(mean, 14 / 3)
    with pytest.raises(ValueError):
        m.min_max_mean([])


def test_apply_discount():
    assert m.apply_discount(100, percent=10) == 90
    assert m.apply_discount(100, percent=10, fixed=5) == 85
    assert m.apply_discount(10, fixed=50) == 0
    with pytest.raises(TypeError):
        m.apply_discount(100, 10)  # keyword-only


def test_make_counter():
    c1, c2 = m.make_counter(), m.make_counter(10, 5)
    assert [c1(), c1(), c1()] == [1, 2, 3]
    assert [c2(), c2()] == [15, 20]
    assert c1() == 4  # independent state


def test_compose():
    inc = lambda x: x + 1  # noqa: E731
    dbl = lambda x: x * 2  # noqa: E731
    assert m.compose(inc, dbl)(5) == 11  # inc(dbl(5))
    assert m.compose(dbl, inc)(5) == 12
    assert m.compose()(7) == 7


def test_validate():
    rules = [(lambda p: len(p) >= 12, "len"), (lambda p: any(c.isdigit() for c in p), "digit")]
    assert m.validate("hello", rules) == ["len", "digit"]
    assert m.validate("correct-horse-battery-9", rules) == []
