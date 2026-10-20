import ast
from pathlib import Path

import pytest

from notes import note, question_snippets
from sd_tools import cyclomatic_complexity, has_cycle, import_graph, instability, requirement_smells

TEXT = note("MOCK-SD-01 Software Design and Development Mock Examination")
SNIPPETS = question_snippets(TEXT)
HOSTEL = Path(__file__).resolve().parents[3] / (
    "10 - Projects and Practical Labs/Python Projects/PRJ-PY-05 Hostel Maintenance System/src/hostel")


def test_q2_requirement_smells():
    assert requirement_smells("The system should be fast and user-friendly.") == [
        "vague term 'user-friendly'", "vague term 'fast'", "weak/optional wording 'should'",
        "no 'shall'/'must': unclear whether this is mandatory"]
    assert requirement_smells("The system shall let a resident submit a fault report and/or upload a photo.") == [
        "'and/or' is ambiguous"]
    assert requirement_smells("The system shall display a resident's open requests within 2 seconds for 95% of "
                              "page loads.") == []


def test_q4_metrics_come_from_the_real_package():
    g = import_graph(str(HOSTEL), "hostel")
    table = {m: sorted(d) for m, d in g.items() if m != "__main__"}
    assert table == {"cli": ["errors", "insights", "models", "reports", "repository", "security", "services"],
                     "services": ["errors", "models", "repository", "security"], "repository": ["errors", "models"],
                     "insights": ["models"], "reports": ["models"], "models": ["errors"], "security": [], "errors": []}
    m = instability(g)
    assert {k: m[k] for k in ("cli", "services", "repository", "models", "errors")} == {
        "cli": (1, 7, 0.88), "services": (1, 4, 0.8), "repository": (2, 2, 0.5), "models": (5, 1, 0.17),
        "errors": (4, 0, 0.0)}
    assert not has_cycle(g)


def test_q5_snippet_parses():
    ast.parse(SNIPPETS["Q5"])


def test_q6_complexity_and_expected_values():
    assert cyclomatic_complexity(SNIPPETS["Q6"]) == {"shipping_cost": 7}
    ns: dict = {}
    exec(compile(SNIPPETS["Q6"], "<Q6>", "exec"), ns)
    f = ns["shipping_cost"]
    with pytest.raises(ValueError):
        f(0, False, "local", False)
    assert f(1, False, "local", False) == 2500
    assert f(10, False, "local", False) == 7300 and f(9.9, False, "local", False) == 6950
    assert f(2, True, "local", False) == 4000 and f(2, True, "coast", False) == 6000
    assert f(20, False, "local", True) == 11340.0
