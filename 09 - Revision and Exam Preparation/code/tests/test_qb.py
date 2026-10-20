import re

import pytest

from notes import note, question_snippets, run

BANKS = ["QB-PY Python Question Bank"]


def answer_code_blocks(text: str) -> list[str]:
    """Python fences inside folded answers (lines prefixed with '> ')."""
    blocks = re.findall(r"> ```python\n(.*?)> ```", text, re.S)
    return ["\n".join(line[2:] if line.startswith("> ") else line[1:] for line in b.splitlines()) for b in blocks]


@pytest.mark.parametrize("bank", BANKS)
def test_snippet_outputs_appear_in_the_answers(bank):
    text = note(bank)
    snippets = question_snippets(text)
    assert snippets, "no snippets found"
    for qid, code in snippets.items():
        for line in run(code).splitlines():
            assert f"> {line}" in text, f"{qid}: output line {line!r} missing from the answer"


@pytest.mark.parametrize("bank", BANKS)
def test_answer_code_runs(bank):
    for code in answer_code_blocks(note(bank)):
        run(code)


def test_qb_py_claimed_outputs():
    outs = [run(c) for c in answer_code_blocks(note("QB-PY Python Question Bank"))]
    assert "10.5\n" in outs and "True False False\n" in outs
    assert "[{'room': 'A-101', 'category': 'plumbing'}]\n" in outs


def test_qb_dm_numbers():
    import math
    from itertools import product
    B = [False, True]
    imp = lambda a, b: (not a) or b  # noqa: E731
    assert all(imp(p, q) == imp(not q, not p) for p, q in product(B, B))
    assert not all(imp(p, q) == imp(q, p) for p, q in product(B, B))
    assert all(((not (p or not q)) or ((not p) and (not q))) == (not p) for p, q in product(B, B))
    assert math.gcd(84, 36) == 12
    A, C = {1, 2, 3}, {2, 3, 4}
    assert (A & C, A - C, A ^ C) == ({2, 3}, {1}, {1, 4})
    assert (4 ** 3, math.perm(4, 3)) == (64, 24)
    assert sum((-1) ** k * math.comb(3, k) * (3 - k) ** 4 for k in range(4)) == 36
    assert (sum(range(1, 101)), sum(i * i for i in range(1, 11)), sum(2 ** i for i in range(11))) == (5050, 385, 2047)
    assert [n for n in range(1, 60) if not 2 ** n > n * n] == [2, 3, 4]
    S = [1, 2, 3, 4, 6, 12]
    cover = [(a, b) for a in S for b in S if a != b and b % a == 0
             and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in S)]
    assert len(cover) == 7
    assert (math.factorial(5), math.comb(7, 3), math.factorial(5)) == (120, 35, 120)
    assert sum(1 for i in range(1, 101) if i % 3 == 0 or i % 5 == 0) == 47
    assert [math.comb(5, k) for k in range(6)] == [1, 5, 10, 10, 5, 1]
    h = [0]
    for _ in range(6):
        h.append(2 * h[-1] + 1)
    assert h[6] == 63 == 2 ** 6 - 1
    a = [1, 4]
    for _ in range(10):
        a.append(5 * a[-1] - 6 * a[-2])
    assert a == [2 * 3 ** n - 2 ** n for n in range(12)]
    assert sum([2, 2, 3, 3, 4, 4]) // 2 == 9 and 2 ** 2 ** 3 == 256
    assert all(bool(((not x) and (not y)) or ((not x) and y) or (x and not y)) == ((not x) or (not y))
               for x, y in product(B, B))
    assert (6 / 36, 1 - 0.5 ** 3, sum(range(1, 7)) / 6) == (1 / 6, 0.875, 3.5)


def test_qb_cs_numbers():
    from cs_examples import ale, cvss31_base, edit_distance, hotp, symbolic
    assert (hotp(b"12345678901234567890", 0), hotp(b"12345678901234567890", 1)) == ("755224", "287082")
    assert cvss31_base("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H") == (9.8, "Critical")
    assert edit_distance("university.example", "univercity.example") == 1
    assert symbolic(0o640) == "rw-r-----"
    assert ale(50e6, 0.2, 2) == (10e6, 20e6)


def test_qb_sd_numbers():
    from sd_tools import instability, requirement_smells
    assert len(requirement_smells("The system should be fast and user-friendly.")) == 4
    assert instability({"m": {"x"}, "a": {"m"}, "b": {"m"}, "c": {"m"}, "d": {"m"}, "e": {"m"}, "x": set()})["m"] == (
        5, 1, 0.17)


def test_qb_pm_numbers():
    from pm_tools import (EVM, Activity, communication_channels, control_limits, cpm, emv, fpif_final_price, fpif_pta,
                          npv, payback_period, pert, prob_complete_by, sprints_needed)
    assert round(npv(0.10, [-100, 60, 60]), 2) == 4.13
    s = cpm([Activity("A", 2), Activity("B", 3, ("A",)), Activity("C", 1, ("A",)), Activity("D", 2, ("B", "C"))])
    assert s.duration == 7 and s.critical == ["A", "B", "D"] and s.total_float["C"] == 2
    assert (pert(2, 4, 12)[0], round(pert(2, 4, 12)[1], 2)) == (5.0, 1.67)
    assert round(prob_complete_by(22, 20, 2), 2) == 0.84
    e = EVM(100, 40, 36, 45)
    assert (e.spi, e.cpi, e.eac_cpi, e.vac) == (0.9, 0.8, 125.0, -25.0)
    assert emv({"R": (0.2, 25e6)}) == {"R": 5e6}
    assert (communication_channels(5), communication_channels(8)) == (10, 28)
    lcl, mean, ucl = control_limits([10, 12, 11, 9, 13])
    assert (round(lcl, 2), mean, round(ucl, 2)) == (6.26, 11, 15.74)
    assert round(fpif_pta(100e6, 10e6, 120e6, 0.7) / 1e6, 2) == 114.29
    assert round(fpif_final_price(110e6, 100e6, 10e6, 120e6, 0.7)) == 117_000_000
    assert sprints_needed(80, [18, 22, 20]) == (4, 4, 5)
    assert payback_period([-100, 30, 40, 50]) == 2.6


def test_qb_fyp_numbers():
    from fyp_tools import (adjust_for_response_rate, boolean_query, cochran_n0, finite_correction, likert_summary,
                           looks_like_doi, sus_score, yamane)
    assert (finite_correction(cochran_n0(), 800), yamane(800), adjust_for_response_rate(260, 0.4)) == (260, 267, 650)
    assert sus_score([4, 2, 4, 2, 4, 2, 4, 2, 4, 2]) == 75.0
    s = likert_summary([5, 4, 4, 3, 2, 4, 5, 1, 4, 3])
    assert (s["median"], s["mode"], s["pct_agree"], s["mean"]) == (4.0, 4, 60.0, 3.5)
    assert boolean_query([["hostel", "student housing"], ["maintenance", "repair*"], ["system", "app"]]) == (
        '(hostel OR "student housing") AND (maintenance OR repair*) AND (system OR app)')
    assert looks_like_doi("10.1000/xyz123")
