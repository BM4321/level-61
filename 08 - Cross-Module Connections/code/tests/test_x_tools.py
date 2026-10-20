import math

import pytest

from cs_examples import ale, control_value
from fyp_tools import sus_score
from pm_tools import Activity as A
from pm_tools import cpm, emv, resource_constrained, resource_profile
from x_tools import (cost_of_quality, defect_density, defect_removal_efficiency, dijkstra, eoq, equivalent,
                     find_cycle, kruskal, longest_path_dag, path_to, reorder_point, rosi, safety_stock,
                     truth_table, undirected)


def test_x01_requirement_vs_code():
    spec = lambda published, owner, lecturer: published and (owner or lecturer)   # noqa: E731
    code = lambda published, owner, lecturer: published and owner or lecturer     # noqa: E731
    ok, diffs = equivalent(spec, code, ["published", "owner", "lecturer"])
    assert not ok and diffs == [{"published": False, "owner": False, "lecturer": True},
                                {"published": False, "owner": True, "lecturer": True}]
    assert len(truth_table(spec, ["published", "owner", "lecturer"])) == 8
    assert sum(v for _, v in truth_table(spec, ["published", "owner", "lecturer"])) == 3
    fixed = lambda published, owner, lecturer: published and (lecturer or owner)  # noqa: E731
    assert equivalent(spec, fixed, ["published", "owner", "lecturer"]) == (True, [])
    registered, paid, disciplinary = {"S1", "S2", "S3", "S4", "S5"}, {"S1", "S2", "S4", "S6"}, {"S2"}
    assert (registered & paid) - disciplinary == {"S1", "S4"}


CAMPUS = [("Admin", "Library", 120), ("Admin", "ICT", 80), ("Library", "ICT", 60), ("ICT", "HostelA", 200),
          ("Library", "HostelA", 150), ("HostelA", "HostelB", 90), ("ICT", "HostelB", 260),
          ("Cafeteria", "HostelB", 70), ("Cafeteria", "Library", 180), ("Admin", "Cafeteria", 210)]

CASE02 = [A("A", 2), A("B", 3, ("A",)), A("C", 4, ("B",)), A("D", 6, ("A",)), A("E", 5, ("B",)),
          A("F", 3, ("C", "E")), A("G", 2, ("D",)), A("H", 2, ("F", "G")), A("I", 2, ("H",)), A("J", 2, ("I",)),
          A("K", 2, ("J",))]


def test_x02_graphs():
    mst, total = kruskal(CAMPUS)
    assert total == 450 and len(mst) == 5
    assert mst == [("Library", "ICT", 60), ("Cafeteria", "HostelB", 70), ("Admin", "ICT", 80),
                   ("HostelA", "HostelB", 90), ("Library", "HostelA", 150)]
    dist, prev = dijkstra(undirected(CAMPUS), "ICT")
    assert dist == {"ICT": 0, "Admin": 80, "Library": 60, "HostelA": 200, "HostelB": 260, "Cafeteria": 240}
    assert path_to(prev, "ICT", "Cafeteria") == ["ICT", "Library", "Cafeteria"]
    assert sum(w for _, _, w in CAMPUS) == 1420
    assert dijkstra(undirected(CAMPUS), "Admin")[0] == {"Admin": 0, "Library": 120, "ICT": 80, "Cafeteria": 210,
                                                       "HostelA": 270, "HostelB": 280}
    extra = CAMPUS + [("ICT", "Cafeteria", 100)]                       # practice question 5
    assert kruskal(extra)[1] == 400 and ("Library", "HostelA", 150) not in kruskal(extra)[0]
    d_extra = dijkstra(undirected(extra), "ICT")[0]
    assert (d_extra["Cafeteria"], d_extra["HostelB"]) == (100, 170)
    with pytest.raises(ValueError):
        dijkstra({"a": {"b": -1}}, "a")
    # CPM's forward pass is a longest path in a DAG: both give PM-CASE-02's 21 weeks
    d, path = longest_path_dag({a.name: a.duration for a in CASE02}, {a.name: list(a.predecessors) for a in CASE02})
    assert d == cpm(CASE02).duration == 21 and path == cpm(CASE02).critical == list("ABEFHIJK")
    layered = {"cli": ["services"], "services": ["repository", "models"], "repository": ["models"], "models": []}
    assert find_cycle(layered) == []
    layered["models"] = ["services"]
    assert find_cycle(layered) == ["services", "repository", "models", "services"]


def test_x04_quality_metrics():
    assert defect_removal_efficiency(46, 4) == 0.92
    assert defect_density(50, 6250) == 8.0
    assert cost_of_quality(2.0, 3.5, 4.0, 6.5) == {"conformance": 5.5, "nonconformance": 10.5, "total": 16.0}
    with pytest.raises(ValueError):
        defect_removal_efficiency(0, 0)
    from pm_tools import control_limits, pareto
    p = pareto({"validation": 14, "authorisation": 9, "ui_text": 6, "reports": 4, "performance": 2, "other": 3})
    assert [c for c, _, _ in p[:2]] == ["validation", "authorisation"] and p[1][2] == 60.5 and p[2][2] == 76.3
    lcl, mean, ucl = control_limits([5, 7, 4, 6, 8, 5, 6, 7, 5, 6])
    assert (round(lcl, 2), mean, round(ucl, 2)) == (2.31, 5.9, 9.49) and 15 > ucl


def test_x05_security_risk_in_pm_terms():
    sle, before = ale(160e6, 0.25, 0.25)
    _, after = ale(160e6, 0.25, 0.05)
    assert (sle, before, after) == (40e6, 10e6, 2e6)
    assert control_value(before, after, 3e6) == 5e6
    assert math.isclose(rosi(before, after, 3e6), 5 / 3)
    assert math.isclose(control_value(before, ale(160e6, 0.25, 0.175)[1], 3e6), 0, abs_tol=1e-6)   # break-even ARO
    assert ale(50e6, 0.4, 0.5) == (20e6, 10e6) and math.isclose(rosi(10e6, 2e6, 6e6), 1 / 3)       # practice 3-4
    risks = emv({"R1": (0.10, 40e6), "R2": (0.15, 20e6), "R3": (0.30, 8e6), "R4": (0.25, 12e6)})
    assert risks == {"R1": 4e6, "R2": 3e6, "R3": 2.4e6, "R4": 3e6} and math.isclose(sum(risks.values()), 12.4e6)


SEMESTER = [A("A", 2), A("B", 3, ("A",)), A("C", 1, ("B",)), A("D", 2), A("E", 1, ("D",)), A("F", 2),
            A("G", 2, ("F",)), A("H", 2), A("I", 1, ("H",)), A("K", 2), A("J", 3, ("K",)), A("L", 1, ("J",)),
            A("M", 3), A("N", 2, ("C", "E", "G", "I", "L", "M"))]
UNITS = {"A": 2, "B": 3, "C": 2, "D": 2, "E": 2, "F": 1, "G": 1, "H": 2, "I": 1, "J": 3, "K": 2, "L": 2, "M": 1, "N": 4}


def test_x07_semester_plan():
    s = cpm(SEMESTER)
    assert s.duration == 8 and s.critical == ["A", "B", "C", "K", "J", "L", "N"]
    assert {n: s.total_float[n] for n in "DEFGHIM"} == {"D": 3, "E": 3, "F": 2, "G": 2, "H": 3, "I": 3, "M": 3}
    assert resource_profile(s, SEMESTER, UNITS) == [10, 10, 11, 7, 6, 4, 4, 4]
    assert sum(a.duration * UNITS[a.name] for a in SEMESTER) == 56          # 56 x 5 h = 280 h of study
    assert resource_constrained(SEMESTER, UNITS, 4)[0] == 15                 # 20 h/week
    assert resource_constrained(SEMESTER, UNITS, 5)[0] == 12                 # 25 h/week
    assert resource_constrained(SEMESTER, UNITS, 7)[0] == 10
    _, starts, _ = resource_constrained(SEMESTER, UNITS, 5)
    assert {n for n, t in starts.items() if t == 0} == {"A", "K", "F"} and starts["M"] == 6
    lighter = {**UNITS, "B": 2}                                                # practice question 3
    assert resource_profile(s, SEMESTER, lighter) == [10, 10, 10, 6, 5, 4, 4, 4]


PORTAL = [A("A", 2), A("B", 2, ("A",)), A("C", 3, ("B",)), A("D", 2, ("B",)), A("E", 2, ("C",)), A("F", 1, ("C",)),
          A("G", 2, ("D", "E", "F")), A("H", 1, ("G",)), A("I", 1, ("B",)), A("J", 1, ("H", "I"))]


def test_xcase01_portal_plan():
    s = cpm(PORTAL)
    assert s.duration == 13 and s.critical == ["A", "B", "C", "E", "G", "H", "J"]
    assert (s.total_float["D"], s.total_float["F"], s.total_float["I"]) == (3, 1, 7)
    from x_tools import approve_mark_change, can_view_result, results_digest
    rows = [(r, p, o, t) for r in ("student", "lecturer", "exams_officer") for p in (False, True)
            for o in (False, True) for t in (False, True)]
    allowed = [row for row in rows if can_view_result(*row)]
    assert len(rows) == 24 and len(allowed) == 8 + 4 + 2
    spec = lambda role, published, own, teaches: (  # noqa: E731
        role == "exams_officer" or (role == "lecturer" and teaches) or (role == "student" and published and own))
    assert all(can_view_result(*r) == spec(*r) for r in rows)
    assert not can_view_result("guest", True, True, True)
    shortcut = lambda role, published, own, teaches: role == "student" and published and own or teaches  # noqa: E731
    wrong = [r for r in rows if bool(shortcut(*r)) != can_view_result(*r)]
    assert ("student", False, False, True) in wrong and ("exams_officer", False, False, False) in wrong
    assert approve_mark_change("L01", "H01", "head_of_department")
    assert not approve_mark_change("H01", "H01", "head_of_department")          # no self-approval
    assert not approve_mark_change("L01", "L02", "lecturer")
    marks = [("S1", "CST06102", 71.0), ("S2", "CST06102", 64.5), ("S3", "CST06102", 49.0)]
    d = results_digest(marks)
    assert d == results_digest(list(reversed(marks))) and len(d) == 64
    assert results_digest([("S1", "CST06102", 71.0), ("S2", "CST06102", 64.5), ("S3", "CST06102", 50.0)]) != d


def test_xcase02_inventory():
    ss = safety_stock(1.645, 12, 9)
    assert round(ss, 2) == 59.22
    assert math.ceil(reorder_point(40, 9, ss)) == 420
    ss99 = safety_stock(2.326, 12, 9)                                         # discussion question 1
    assert round(ss99, 1) == 83.7 and math.ceil(reorder_point(40, 9, ss99)) == 444
    assert round(eoq(40 * 360, 50_000, 600)) == 1549
    from x_tools import reorder_alerts
    stock = {("DAR", "CEM50"): 380, ("MWZ", "CEM50"): 900, ("ARU", "CEM50"): 420, ("DAR", "NAIL3"): 40,
             ("ARU", "NAIL3"): 15, ("MWZ", "OLDPAINT"): 2}
    rop = {"CEM50": 420, "NAIL3": 60, "OLDPAINT": 10}
    alerts = reorder_alerts(stock, rop, open_orders={("ARU", "NAIL3")}, active={"CEM50", "NAIL3"})
    assert alerts == [("ARU", "CEM50"), ("DAR", "CEM50"), ("DAR", "NAIL3")]
    below = lambda sku: {w for (w, k), q in stock.items() if k == sku and q <= rop[sku]}  # noqa: E731
    assert below("CEM50") | below("NAIL3") == {"DAR", "ARU"} and below("CEM50") & below("NAIL3") == {"DAR", "ARU"}
    from pm_tools import EVM
    e = EVM(56e6, 45.5e6, 37e6, 36.2e6)                                     # PM-CASE-02, end of week 12
    assert (round(e.spi, 3), round(e.cpi, 3), round(e.eac_cpi)) == (0.813, 1.022, 54_789_189)
    assert round(e.sv) == -8_500_000 and round(e.cv) == 800_000
    assert cpm(CASE02).duration == 21


CAPSTONE = [A("A", 2), A("B", 1, ("A",)), A("C", 1, ("B",)), A("D", 2, ("C",)), A("E", 2, ("D",)), A("F", 2, ("E",)),
            A("G", 1, ("E",)), A("H", 2, ("F", "G")), A("I", 1, ("H",)), A("J", 3, ("I",)), A("K", 1, ("J",))]
SUS = [[4, 2, 4, 1, 4, 2, 5, 2, 4, 2], [5, 1, 4, 2, 5, 1, 4, 1, 4, 2], [3, 2, 4, 2, 4, 3, 4, 2, 3, 3],
       [4, 2, 5, 1, 4, 2, 4, 2, 4, 1], [4, 3, 3, 2, 4, 2, 4, 3, 3, 2], [5, 1, 5, 1, 5, 1, 5, 1, 4, 1],
       [3, 3, 3, 2, 3, 3, 4, 2, 3, 3], [4, 2, 4, 2, 4, 2, 4, 2, 4, 2], [4, 1, 4, 1, 5, 2, 5, 1, 4, 2],
       [2, 3, 3, 3, 3, 3, 3, 3, 3, 4]]


def test_xcapstone_plan_and_evaluation():
    s = cpm(CAPSTONE)
    assert s.duration == 17 and s.total_float["G"] == 1 and len(s.critical) == 10
    scores = [sus_score(p) for p in SUS]
    assert scores == [80.0, 87.5, 65.0, 82.5, 65.0, 97.5, 57.5, 75.0, 87.5, 45.0]
    assert sum(scores) / len(scores) == 74.25
    assert sorted(scores)[4:6] == [75.0, 80.0]                               # median 77.5
    assert sum(s >= 68 for s in scores) == 6


def test_x03_security_requirements_trace_to_real_tests():
    import ast
    from pathlib import Path

    from sd_tools import trace_gaps
    hostel_tests = Path(__file__).resolve().parents[3] / (
        "10 - Projects and Practical Labs/Python Projects/PRJ-PY-05 Hostel Maintenance System/tests")
    names = {f.name for p in hostel_tests.glob("test_*.py") for f in ast.parse(p.read_text()).body
             if isinstance(f, ast.FunctionDef) and f.name.startswith("test_")}
    reqs = {"SR1": "passwords stored with a memory-hard KDF", "SR2": "generic authentication errors",
            "SR3": "login throttling", "SR4": "role and ownership checks", "SR5": "atomic audit trail",
            "SR6": "parameterised SQL and input validation", "SR7": "single-use expiring reset tokens",
            "SR8": "MFA for staff accounts"}
    links = {"SR1": ["test_hash_format_and_verify", "test_rehash_on_login_when_parameters_change"],
             "SR2": ["test_login_success_failure_and_generic_message"],
             "SR3": ["test_backoff_schedule", "test_throttling_with_fake_clock"],
             "SR4": ["test_permissions", "test_priority_and_visibility", "test_reopen_window_and_owner"],
             "SR5": ["test_happy_path_and_audit_trail", "test_update_and_history_are_atomic"],
             "SR6": ["test_input_validation"],
             "SR7": ["test_password_reset"]}
    gaps = trace_gaps(reqs, links, names)
    assert gaps["untested_requirements"] == ["SR8"] and gaps["unknown_tests"] == []
    assert gaps["tests_without_requirement"] == sorted(
        {"test_every_disallowed_transition_is_rejected", "test_optimistic_concurrency_between_two_connections",
         "test_password_policy", "test_register_rejects_weak_and_personal_passwords", "test_summary_numbers",
         "test_cli_end_to_end", "test_layering_rules", "test_repeat_rooms_window_threshold_and_order",
         "test_work_queue_urgent_then_oldest", "test_possible_duplicates"})
    assert len(names) == 22                     # 22 functions; parametrisation makes 45 collected tests
