import math
import re

from cs_examples import (ale, control_value, cvss31_base, failure_bursts, k_anonymity, parse_auth_log, risk_rating,
                         success_after_failures, symbolic)
from notes import note

TEXT = note("MOCK-CS-01 Cyber Security Mock Examination")


def test_a2_search_spaces():
    assert round(math.log2(62 ** 8), 1) == 47.6 and round(math.log2(26 ** 15), 1) == 70.5
    assert round(62 ** 8 / 1e10 / 3600, 1) == 6.1                         # hours
    assert round(26 ** 15 / 1e10 / (3600 * 24 * 365)) == 5319              # years


def test_a3_modes():
    assert [symbolic(m) for m in (0o640, 0o4750, 0o777)] == ["rw-r-----", "rwsr-x---", "rwxrwxrwx"]


def test_a5_cvss():
    assert cvss31_base("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N") == (6.5, "Medium")
    assert cvss31_base("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N") == (6.1, "Medium")
    assert cvss31_base("CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H") == (7.8, "High")


def test_b2_risk():
    assert ale(80e6, 0.3, 0.5) == (24e6, 12e6)
    assert control_value(12e6, 3e6, 4e6) == 5e6
    assert [risk_rating(4, 4), risk_rating(2, 3), risk_rating(5, 4)] == [(16, "High"), (6, "Medium"), (20, "Critical")]


def test_b3_log_excerpt_from_the_paper():
    block = re.search(r"```text\n(2026-03-02T09:10:01Z.*?)```", TEXT, re.S).group(1)
    events = parse_auth_log(block.splitlines())
    assert len(events) == 8
    assert failure_bursts(events, threshold=5) == {"203.0.113.77": 5}
    hits = success_after_failures(events, min_failures=3)
    assert [(u, ip) for u, ip, _ in hits] == [("deploy", "203.0.113.77")]


def test_b4_k_anonymity():
    rows = [{"block": b, "year": y} for b, y in [("A", 2), ("A", 2), ("A", 3), ("B", 2), ("B", 2)]]
    assert k_anonymity(rows, ["block", "year"]) == 1
    generalised = [{"block": r["block"], "year": "2-3"} for r in rows]
    assert k_anonymity(generalised, ["block", "year"]) == 2
