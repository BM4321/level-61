import pytest

from _target import load

m = load("py20")


@pytest.mark.parametrize("n, r", [(1, "I"), (3, "III"), (4, "IV"), (5, "V"), (9, "IX"), (14, "XIV"),
                                  (40, "XL"), (90, "XC"), (400, "CD"), (1994, "MCMXCIV"), (3999, "MMMCMXCIX")])
def test_int_to_roman(n, r):
    assert m.int_to_roman(n) == r
    assert m.roman_to_int(r) == n


@pytest.mark.parametrize("bad", [0, 4000, -1])
def test_int_to_roman_range(bad):
    with pytest.raises(ValueError):
        m.int_to_roman(bad)


@pytest.mark.parametrize("bad", ["", "IIII", "VX", "IC", "ABC", "MMMM"])
def test_roman_to_int_rejects(bad):
    with pytest.raises(ValueError):
        m.roman_to_int(bad)


def test_round_trip_all():
    for n in range(1, 4000):
        assert m.roman_to_int(m.int_to_roman(n)) == n


def test_lowercase_variation():
    assert m.int_to_roman(14, lowercase=True) == "xiv"


def test_average_passing_regression():
    assert m.average_passing([50, 60, 70]) == 60.0
    with pytest.raises(ValueError):
        m.average_passing([10, 20])


@pytest.mark.parametrize("pw, issue", [("short1a", "too short"), ("abcdefghijkl", "no digit"),
                                       ("123456789012", "no letter"), ("password1234", "too common")])
def test_password_issue_detected(pw, issue):
    assert issue in m.password_issues(pw, common={"password1234"})


def test_password_good_and_boundary():
    assert m.password_issues("correct horse 42 battery", common=set()) == []
    assert "too short" not in m.password_issues("abcdefghij12", common=set())
    assert "too short" in m.password_issues("abcdefghi12", common=set())
