import math

import pytest

from _target import load

m = load("py04")


@pytest.mark.parametrize("mark, expected", [(0, "F"), (39, "F"), (39.9, "F"), (40, "D"), (49, "D"),
                                            (50, "C"), (59, "C"), (60, "B"), (69, "B"), (69.5, "B"),
                                            (70, "A"), (100, "A")])
def test_grade(mark, expected):
    assert m.grade(mark) == expected


@pytest.mark.parametrize("bad", [-1, 101, -0.5, 100.01])
def test_grade_invalid(bad):
    with pytest.raises(ValueError):
        m.grade(bad)


@pytest.mark.parametrize("year, leap", [(2023, False), (2024, True), (1900, False), (2000, True), (2100, False)])
def test_is_leap(year, leap):
    assert m.is_leap(year) is leap


def test_max_of_three():
    assert m.max_of_three(1, 2, 3) == 3
    assert m.max_of_three(3, 2, 1) == 3
    assert m.max_of_three(2, 3, 1) == 3
    assert m.max_of_three(-1, -1, -1) == -1


@pytest.mark.parametrize("sides, kind", [((3, 3, 3), "equilateral"), ((3, 3, 5), "isosceles"),
                                         ((5, 3, 3), "isosceles"), ((3, 4, 5), "scalene"),
                                         ((1, 2, 3), "invalid"), ((0, 1, 1), "invalid"), ((-1, 2, 2), "invalid")])
def test_classify_triangle(sides, kind):
    assert m.classify_triangle(*sides) == kind


@pytest.mark.parametrize("age, student, price", [(0, False, 0), (4, True, 0), (5, False, 2000), (17, True, 2000),
                                                 (18, False, 5000), (18, True, 2500), (60, True, 2500)])
def test_ticket_price(age, student, price):
    assert m.ticket_price(age, student) == price


def test_ticket_price_negative():
    with pytest.raises(ValueError):
        m.ticket_price(-1, False)


@pytest.mark.parametrize("pt, q", [((0, 0), "origin"), ((5, 0), "x-axis"), ((-5, 0), "x-axis"),
                                   ((0, 2), "y-axis"), ((1, 1), 1), ((-1, 1), 2), ((-1, -1), 3), ((1, -1), 4)])
def test_quadrant(pt, q):
    assert m.quadrant(*pt) == q


@pytest.mark.parametrize("total, member, gift, rate", [(150_000, False, False, 0.10), (150_000, True, False, 0.12),
                                                       (99_999, True, False, 0.05), (99_999, False, False, 0.0),
                                                       (100_000, False, False, 0.10), (500_000, True, True, 0.0)])
def test_discount_rate(total, member, gift, rate):
    assert math.isclose(m.discount_rate(total, member, gift), rate)


def test_grade_with_points():
    assert m.grade_with_points(72) == ("A", 5)
    assert m.grade_with_points(40) == ("D", 2)
    assert m.grade_with_points(0) == ("F", 0)
    with pytest.raises(ValueError):
        m.grade_with_points(120)
