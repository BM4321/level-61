import pytest

from fyp_tools import (adjust_for_response_rate, alignment_gaps, citation_crosscheck, cochran_n0, cronbach_alpha,
                       finite_correction, identifier_scan, likert_summary, sus_score, word_budget, yamane)

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


def test_fyp10_citation_crosscheck():
    body = ("Maintenance requests are often lost (Mwakyusa, 2021). Smith and Jones (2019) found delays; "
            "Okafor et al. (2020) proposed a ticketing model. Later work (Mwakyusa, 2021) agrees.")
    refs = ["Mwakyusa, A. (2021). Title. Journal.", "Smith, B., & Jones, C. (2019). Title. Publisher.",
            "Lee, D. (2018). Title. Journal."]
    assert citation_crosscheck(body, refs) == {"missing_from_references": ["Okafor 2020"],
                                               "never_cited": ["Lee 2018"]}
    with pytest.raises(ValueError):
        citation_crosscheck(body, ["no year here"])


def test_fyp10_identifier_scan():
    t = "Interviewee Neema (neema.k@student.example, 0712 345 678, reg ABC/21/01234) said Neema's room leaks."
    assert identifier_scan(t, ["Neema"]) == {"email": 1, "phone": 1, "student_id": 1, "known_names": 2}
    assert identifier_scan("P07 said the room in Block C leaks.", ["Neema"]) == {
        "email": 0, "phone": 0, "student_id": 0, "known_names": 0}


def test_fyp11_alignment_and_word_budget():
    rows = [dict(problem="Unknown current process", rq="RQ1", objective="SO1", method="Interviews, survey",
                 evaluation="Thematic summary"),
            dict(problem="Unclear needs", rq="RQ2", objective="SO2", method="Elicitation", evaluation=""),
            dict(problem="No tracking tool", rq="RQ3", objective="SO3", method="Design science build",
                 evaluation="Tests passing"),
            dict(problem="Unknown acceptability", rq="RQ3", objective="SO4", method="", evaluation="SUS")]
    assert alignment_gaps(rows) == ["RQ2: no evaluation", "RQ3: no method", "RQ3: appears in 2 rows"]
    w = word_budget(8000, {"Ch1": 15, "Ch2": 30, "Ch3": 30, "Ch4": 15, "Ch5": 10})
    assert w == {"Ch1": 1200, "Ch2": 2400, "Ch3": 2400, "Ch4": 1200, "Ch5": 800}
    w = word_budget(7000, {"Ch1": 1, "Ch2": 2, "Ch3": 2, "Ch4": 1, "Ch5": 0.7})
    assert w == {"Ch1": 1045, "Ch2": 2090, "Ch3": 2089, "Ch4": 1045, "Ch5": 731} and sum(w.values()) == 7000
    with pytest.raises(ValueError):
        word_budget(100, {"a": 0})


def test_fyp12_defence_timing():
    weights = {"Problem and RQs": 2, "Literature and gap": 2, "Methodology": 3, "Design plan": 2,
               "Work plan and ethics": 2, "Summary": 1}
    assert word_budget(900, weights) == {"Problem and RQs": 150, "Literature and gap": 150, "Methodology": 225,
                                         "Design plan": 150, "Work plan and ethics": 150, "Summary": 75}
    t = word_budget(600, weights)
    assert t["Methodology"] == 150 and t["Summary"] == 50 and sum(t.values()) == 600
