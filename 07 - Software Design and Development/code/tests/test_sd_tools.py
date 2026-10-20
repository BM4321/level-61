import inspect

import clinic.flawed_god_class as god
import labbook.service as service
from sd_tools import cyclomatic_complexity, requirement_smells, trace_gaps


def test_requirement_smells():
    assert requirement_smells("The system shall allow a student to book a workstation for a slot of 30 to 240 minutes.") == []
    assert requirement_smells("The system should be user-friendly and fast.") == [
        "vague term 'user-friendly'", "vague term 'fast'", "weak/optional wording 'should'",
        "no 'shall'/'must': unclear whether this is mandatory"]
    assert "more than one 'shall' (split into separate requirements)" in requirement_smells(
        "The system shall notify users and shall log all changes.")
    assert requirement_smells("Bookings must be confirmed within TBD seconds.") == ["unresolved placeholder (TBD)"]
    assert requirement_smells("The system shall be secure.") == ["vague term 'secure'"]
    assert requirement_smells("Reports shall list bookings by lab and/or by user.") == ["'and/or' is ambiguous"]


def test_trace_gaps():
    reqs = {"FR-01": "book", "FR-02": "no overlap", "FR-03": "opening hours"}
    links = {"FR-01": ["test_book"], "FR-02": ["test_overlap", "test_missing"], "FR-09": ["test_x"]}
    tests = {"test_book", "test_overlap", "test_x", "test_cli"}
    assert trace_gaps(reqs, links, tests) == {
        "untested_requirements": ["FR-03"], "unknown_tests": ["test_missing"],
        "links_to_unknown_requirements": ["FR-09"], "tests_without_requirement": ["test_cli"]}


def test_cyclomatic_complexity():
    assert cyclomatic_complexity("def f(x):\n    return x\n") == {"f": 1}
    src = "def g(x, y):\n    if x and y:\n        return 1\n    for i in range(3):\n        pass\n    return 0\n"
    assert cyclomatic_complexity(src) == {"g": 4}
    assert cyclomatic_complexity(inspect.getsource(god))["LabManager.do_booking"] == 14
    assert max(cyclomatic_complexity(inspect.getsource(service)).values()) == 3


from sd_tools import has_cycle, import_graph, instability  # noqa: E402


def test_labbook_dependency_rules():
    g = import_graph("labbook", "labbook")
    assert not has_cycle(g)
    assert g["domain"] == {"errors"}                       # domain depends on nothing but its errors
    assert g["errors"] == set() and g["events"] == set()
    for inner in ("domain", "rules", "repository", "events", "errors"):
        assert not g[inner] & {"service", "app", "cli"}     # inner layers never import outer ones
    assert "sqlite3" not in open("labbook/service.py", encoding="utf-8").read()   # no infrastructure in service
    m = instability(g)
    assert m["errors"] == (5, 0, 0.0) and m["domain"] == (5, 1, 0.17) and m["service"] == (1, 5, 0.83)


def test_cycle_detection():
    assert has_cycle({"a": {"b"}, "b": {"a"}})
    assert not has_cycle({"a": {"b"}, "b": set()})
