import pytest

from fyp_tools import (adjust_for_response_rate, cochran_n0, cronbach_alpha, finite_correction, likert_summary,
                       sus_score, yamane)

ITEMS = [[4, 5, 3, 4, 2, 5, 4, 3], [4, 4, 3, 5, 2, 5, 4, 3], [3, 5, 2, 4, 1, 4, 4, 3], [5, 4, 3, 4, 2, 5, 5, 2]]


def test_sample_sizes():
    n0 = cochran_n0()
    assert round(n0, 1) == 384.1                   # z = 1.95996 (often rounded to 1.96 -> 384.16)
    assert finite_correction(n0, 6000) == 362 and finite_correction(n0, 400) == 197
    assert yamane(6000) == 375 and yamane(400) == 200
    assert adjust_for_response_rate(362, 0.6) == 604
    assert round(cochran_n0(0.95, 0.5, 0.10)) == 96 and round(cochran_n0(0.99)) == 663
    assert round(cochran_n0(0.95, 0.3)) == 323


def test_reliability_and_descriptives():
    assert round(cronbach_alpha(ITEMS), 3) == 0.938
    with pytest.raises(ValueError):
        cronbach_alpha([[1, 2, 3]])
    s = likert_summary([5, 4, 4, 3, 5, 2, 4, 4, 5, 1, 4, 3])
    assert (s["median"], s["mode"], s["mean"], s["pct_agree"]) == (4.0, 4, 3.67, 66.7)


def test_sus():
    assert sus_score([4, 2, 4, 1, 5, 2, 4, 2, 4, 3]) == 77.5
    assert sus_score([3] * 10) == 50.0
    with pytest.raises(ValueError):
        sus_score([6] * 10)


from fyp_tools import boolean_query, looks_like_doi  # noqa: E402


def test_boolean_query():
    q = boolean_query([["maintenance request", "facility management", "work order"],
                       ["university", "hostel", "student housing"],
                       ["system", "application", "mobile"]])
    assert q == ('("maintenance request" OR "facility management" OR "work order") AND '
                 '(university OR hostel OR "student housing") AND (system OR application OR mobile)')
    assert boolean_query([["usability"], ["SUS", "system usability scale"]]) == 'usability AND (SUS OR "system usability scale")'
    with pytest.raises(ValueError):
        boolean_query([[]])


def test_doi_syntax_only():
    assert looks_like_doi("10.1145/1273445.1273458")
    assert not looks_like_doi("https://example.com/paper") and not looks_like_doi("10.12/x")


def test_fyp07_running_example_numbers():
    n0 = cochran_n0()
    assert finite_correction(n0, 2400) == 332 and yamane(2400) == 343
    assert adjust_for_response_rate(332, 0.5) == 664
    assert finite_correction(cochran_n0(0.95, 0.5, 0.10), 2400) == 93


def test_fyp07_practice():
    assert finite_correction(cochran_n0(), 800) == 260 and yamane(800) == 267
    assert sus_score([5, 1] * 5) == 100.0
