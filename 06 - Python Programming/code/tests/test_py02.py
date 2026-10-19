import math

import pytest

from _target import load

m = load("py02")


def test_celsius_to_fahrenheit():
    assert m.celsius_to_fahrenheit(0) == 32
    assert m.celsius_to_fahrenheit(100) == 212
    assert math.isclose(m.celsius_to_fahrenheit(-40), -40)
    assert math.isclose(m.celsius_to_fahrenheit(36.6), 97.88)


@pytest.mark.parametrize("total, expected", [(0, (0, 0, 0)), (59, (0, 0, 59)),
                                             (3600, (1, 0, 0)), (7384, (2, 3, 4))])
def test_split_seconds(total, expected):
    assert m.split_seconds(total) == expected


@pytest.mark.parametrize("n, expected", [(0, True), (7, False), (-4, True), (-3, False)])
def test_is_even(n, expected):
    assert m.is_even(n) is expected


def test_vat_inclusive_cents():
    assert m.vat_inclusive_cents(1999, 18) == 2359
    assert m.vat_inclusive_cents(100, 18) == 118
    assert m.vat_inclusive_cents(250, 18) == 295   # 45.0 exactly
    assert m.vat_inclusive_cents(0, 18) == 0


def test_digit_sum():
    assert m.digit_sum(0) == 0
    assert m.digit_sum(407) == 11
    assert m.digit_sum(99999) == 45
    with pytest.raises(ValueError):
        m.digit_sum(-1)


def test_format_duration():
    assert m.format_duration(7384) == "2h 03m 04s"
    assert m.format_duration(184) == "3m 04s"
    assert m.format_duration(4) == "4s"
    assert m.format_duration(0) == "0s"
    with pytest.raises(ValueError):
        m.format_duration(-5)
