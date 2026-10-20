import pytest

from mock_solutions import InsufficientStock, Stock, course_averages, first_index, grade, late_fee, total_fee
from notes import note, question_snippets, run

TEXT = note("MOCK-PY-01 Python Programming Mock Examination")
SNIPPETS = question_snippets(TEXT)

EXPECTED = {
    "A1": "[8, 9] [7, 9, 8] [64, 16]\n",
    "A2": "found 6\n12\n",
    "A3": "['pen', 'book'] ['pen', 'book']\n",
    "A4": "{'to': 2, 'be': 2, 'or': 1, 'not': 1} ['be', 'not', 'or', 'to']\n",
    "A5": "try\nelse\nfinally\n5.0\ntry\nexcept\nfinally\n-1\n",
}


@pytest.mark.parametrize("qid", sorted(EXPECTED))
def test_section_a_outputs_match_the_marking_guide(qid):
    assert run(SNIPPETS[qid]) == EXPECTED[qid]
    if qid != "A5":                                   # A5's output is shown as a block in the guide
        assert EXPECTED[qid].splitlines()[-1].strip() in TEXT


def test_b1_grade():
    assert [grade(m) for m in (100, 70, 69.9, 60, 59, 50, 49.5, 40, 39, 0)] == list("AABBCCDDFF")
    for bad in (-1, 100.1):
        with pytest.raises(ValueError):
            grade(bad)
    for bad in (True, "70", None):
        with pytest.raises(TypeError):
            grade(bad)


def test_b2_course_averages_example_from_the_paper():
    block = TEXT.split("```text\nstudent,course,mark", 1)[1].split("```", 1)[0]
    lines = ["student,course,mark"] + [ln for ln in block.strip().splitlines()]
    assert len(lines) == 8
    assert course_averages(lines) == ({"CST06102": 67.8, "GST06106": 53.5}, 3)


def test_b3_stock():
    s = Stock()
    s.add("CEM50", 10)
    s.add("NAIL3", 5)
    s.remove("NAIL3", 5)
    assert s.quantity("CEM50") == 10 and s.quantity("NAIL3") == 0 and len(s) == 1
    with pytest.raises(InsufficientStock) as e:
        s.remove("CEM50", 11)
    assert (e.value.sku, e.value.wanted, e.value.available) == ("CEM50", 11, 10) and s.quantity("CEM50") == 10
    with pytest.raises(ValueError):
        s.add("CEM50", 0)


def test_c1_refactor_preserves_behaviour():
    exec(compile(SNIPPETS["C1"], "<C1>", "exec"), ns := {})
    original = ns["fee"]
    for d in range(0, 101):
        assert total_fee(d, False) == original(d, False)
    assert total_fee(3, True) == original(3, True) == 25_000
    assert original(-1, False) == -500                  # the bug the reviewer should spot
    with pytest.raises(ValueError):
        late_fee(-1)


def test_c2_first_index():
    assert first_index([], 5) == -1
    assert first_index([5], 5) == 0
    assert first_index([1, 2, 2, 2, 3], 2) == 1
    assert first_index([1, 3, 5], 4) == -1
    assert first_index([2, 2, 2], 2) == 0
    data = sorted([7, 3, 3, 9, 1, 3, 8, 8])
    for t in range(0, 11):
        assert first_index(data, t) == (data.index(t) if t in data else -1)
