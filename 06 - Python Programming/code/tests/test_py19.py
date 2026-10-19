import math
import random
import sys
from pathlib import Path

import pytest

from _target import load

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from py19_refactor_before import r as original_report  # noqa: E402

m = load("py19")


def test_weighted_average():
    assert m.weighted_average([60, 80], [1, 3]) == 75.0
    for bad in (([1], [1, 2]), ([1], [-1]), ([1, 2], [0, 0])):
        with pytest.raises(ValueError):
            m.weighted_average(*bad)


@pytest.mark.parametrize("mark, letter", [(0, "F"), (39.5, "F"), (40, "D"), (55, "C"), (69, "B"), (70, "A")])
def test_letter_grade(mark, letter):
    assert m.letter_grade(mark) == letter


def test_characterisation_matches_original():
    rng = random.Random(19)
    for _ in range(200):
        marks = {f"s{i}": rng.randint(0, 100) for i in range(rng.randint(1, 8))}
        assert m.grade_report(marks) == original_report(marks, False)
        assert m.grade_report(marks, str.upper) == original_report(marks, True)


def test_grade_report_empty_is_deliberate_error():
    with pytest.raises(ValueError):
        m.grade_report({})


def test_custom_bands():
    bands = [(70, "Distinction"), (60, "Merit"), (40, "Pass"), (0, "Fail")]
    assert m.grade_report({"ali": 65}, bands=bands) == "ali: 65 Merit\nAVG: 65.0"


def test_can_register():
    course = {"enrolled": ["S1"]}
    assert m.can_register({"id": "S2", "fees_paid": True}, course)
    assert not m.can_register({"id": "S1", "fees_paid": True}, course)
    assert not m.can_register({"id": "S3", "fees_paid": False}, course)
    assert not m.can_register(None, course)
    assert not m.can_register({"id": "S9", "fees_paid": True}, {"enrolled": [f"S{i}" for i in range(40)]})


def test_vat_totals():
    txs = [{"amount": 100, "currency": "TZS"}, {"amount": 50, "currency": "USD"},
           {"amount": 0, "currency": "TZS"}, {"amount": 2_000_000, "currency": "TZS"}]
    assert m.total_without_vat(txs) == 100
    assert math.isclose(m.total_with_vat(txs), 118)
