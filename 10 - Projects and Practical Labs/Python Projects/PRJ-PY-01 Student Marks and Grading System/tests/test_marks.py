import statistics
from pathlib import Path

import pytest

from marks.cli import main
from marks.grading import final_mark, letter_grade
from marks.report import compute_results, summary
from marks.stats import median, rank, std_dev
from marks.storage import load_marks, save_results

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample_marks.csv"


@pytest.mark.parametrize("cw, ex, final", [(78, 72, 74.4), (0, 0, 0.0), (100, 100, 100.0), (50, 30, 38.0)])
def test_final_mark(cw, ex, final):
    assert final_mark(cw, ex) == final


@pytest.mark.parametrize("bad", [(-1, 50), (50, 101)])
def test_final_mark_rejects(bad):
    with pytest.raises(ValueError):
        final_mark(*bad)


@pytest.mark.parametrize("mark, g", [(39.9, "F"), (40, "D"), (49.9, "D"), (50, "C"), (60, "B"), (70, "A")])
def test_letter_grade_boundaries(mark, g):
    assert letter_grade(mark) == g


def test_stats_match_stdlib():
    data = [74.4, 50.2, 87.0, 32.0, 64.4]
    assert median(data) == statistics.median(data)
    assert std_dev(data) == pytest.approx(statistics.pstdev(data))


def test_rank_shares_ties():
    ranked = rank([{"name": "B", "final": 70}, {"name": "A", "final": 70}, {"name": "C", "final": 60}])
    assert [(r["name"], r["rank"]) for r in ranked] == [("A", 1), ("B", 1), ("C", 3)]


def test_load_sample_reports_bad_rows():
    records, errors = load_marks(SAMPLE)
    assert len(records) == 7
    assert errors == ["line 7: coursework is not a number: 'abc'",
                      "line 8: exam is missing",
                      "line 10: coursework must be between 0 and 100, got 101.0"]


def test_missing_columns(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("id,name\n1,A\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing columns"):
        load_marks(p)


def test_duplicate_ids(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("student_id,name,coursework,exam\nS1,A,50,50\nS1,B,60,60\n", encoding="utf-8")
    records, errors = load_marks(p)
    assert len(records) == 1 and "duplicate" in errors[0]


def test_summary_of_sample():
    records, _ = load_marks(SAMPLE)
    s = summary(compute_results(records))
    assert s["count"] == 7 and s["max"] == 87.0 and s["min"] == 32.0
    assert s["distribution"] == {"A": 3, "B": 1, "C": 1, "D": 1, "F": 1}


def test_round_trip_save(tmp_path):
    records, _ = load_marks(SAMPLE)
    out = tmp_path / "results.csv"
    save_results(out, compute_results(records))
    assert out.read_text(encoding="utf-8").splitlines()[1].startswith("1,S003,Chen Wei")


def test_cli_exit_codes(tmp_path, capsys):
    assert main(["report", str(SAMPLE)]) == 1          # bad rows present
    assert "Rejected rows (3)" in capsys.readouterr().out
    good = tmp_path / "g.csv"
    good.write_text("student_id,name,coursework,exam\nS1,A,50,50\n", encoding="utf-8")
    assert main(["report", str(good)]) == 0
    assert main(["report", str(tmp_path / "missing.csv")]) == 2
