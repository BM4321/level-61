import json
from datetime import date
from pathlib import Path

import pytest

from expense_tracker.cli import main
from expense_tracker.models import Expense, format_cents, parse_amount, parse_category
from expense_tracker.reports import budget_status, filter_expenses, totals_by_category
from expense_tracker.storage import JsonRepository, StorageError, export_csv, import_csv

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "bank_statement_sample.csv"


@pytest.mark.parametrize("text, cents", [("1500", 150000), ("1,500.50", 150050), ("0.5", 50), (" 12000 ", 1200000),
                                         ("12.05", 1205)])
def test_parse_amount(text, cents):
    assert parse_amount(text) == cents


@pytest.mark.parametrize("bad", ["-5", "0", "1.234", "12,00", "abc", "", "1e3"])
def test_parse_amount_rejects(bad):
    with pytest.raises(ValueError):
        parse_amount(bad)


def test_format_and_category():
    assert format_cents(150050) == "1,500.50"
    assert parse_category(" Food ") == "food"
    with pytest.raises(ValueError):
        parse_category("food; drop")


def test_repository_persists_and_ids(tmp_path):
    p = tmp_path / "e.json"
    r = JsonRepository(p)
    a = r.add(date(2026, 10, 1), "food", 1000, "x")
    b = r.add(date(2026, 10, 2), "transport", 500)
    assert (a.id, b.id) == (1, 2)
    r2 = JsonRepository(p)
    assert [e.id for e in r2.all()] == [1, 2]
    r2.delete(1)
    c = JsonRepository(p).add(date(2026, 10, 3), "food", 1)
    assert c.id == 3           # ids never reused
    with pytest.raises(KeyError):
        r2.delete(99)


def test_corrupt_file_reported(tmp_path):
    p = tmp_path / "e.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(StorageError):
        JsonRepository(p)


def test_atomic_save_keeps_old_file_on_failure(tmp_path, monkeypatch):
    p = tmp_path / "e.json"
    r = JsonRepository(p)
    r.add(date(2026, 10, 1), "food", 1000)
    before = p.read_text(encoding="utf-8")

    def boom(*a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(json, "dump", boom)
    with pytest.raises(OSError):
        r.add(date(2026, 10, 2), "food", 2000)
    assert p.read_text(encoding="utf-8") == before
    assert list(tmp_path.glob("*.tmp")) == []


def test_reports():
    es = [Expense(1, date(2026, 10, 1), "food", 1000), Expense(2, date(2026, 10, 5), "food", 500),
          Expense(3, date(2026, 9, 30), "rent", 9000), Expense(4, date(2026, 10, 2), "transport", 1500)]
    oct_ = filter_expenses(es, month="2026-10")
    assert [e.id for e in oct_] == [1, 2, 4]
    assert totals_by_category(oct_) == {"food": 1500, "transport": 1500}
    status = budget_status(es, {("food", "2026-10"): 1200, ("rent", "2026-10"): 10000}, "2026-10")
    assert status[0] == {"category": "food", "limit": 1200, "spent": 1500, "remaining": -300, "over": True}
    assert status[1]["spent"] == 0 and not status[1]["over"]


def test_import_reports_bad_lines(tmp_path):
    r = JsonRepository(tmp_path / "e.json")
    n, errors = import_csv(SAMPLE, r)
    assert n == 4
    assert [e.split(":")[0] for e in errors] == ["line 4", "line 6", "line 7"]
    assert "too many fields" in errors[0]
    assert {e.category for e in r.all()} == {"food", "transport", "rent", "airtime"}


def test_export_guards_formula_injection(tmp_path):
    out = tmp_path / "x.csv"
    export_csv(out, [Expense(1, date(2026, 10, 1), "food", 1000, "=HYPERLINK(\"http://evil\")")])
    import csv
    with open(out, newline="", encoding="utf-8") as f:
        note = list(csv.DictReader(f))[0]["note"]
    assert note.startswith("'=HYPERLINK")


def test_cli_flow(tmp_path, capsys):
    data = ["--data", str(tmp_path / "e.json")]
    today = date(2026, 10, 19)
    assert main(data + ["add", "12,000", "food", "lunch"], today=today) == 0
    assert main(data + ["add", "2500", "transport"], today=today) == 0
    assert main(data + ["budget", "food", "10000"], today=today) == 0
    assert main(data + ["status"], today=today) == 0
    out = capsys.readouterr().out
    assert "Added #1: 12,000.00 on food (2026-10-19)" in out and "[OVER]" in out
    assert main(data + ["add", "-5", "food"], today=today) == 1
    assert main(data + ["list", "--month", "2026-10"], today=today) == 0
    assert "14,500.00" in capsys.readouterr().out
