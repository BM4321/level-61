import pytest

from _target import load

m = load("py03")


def test_format_money():
    assert m.format_money(1234.5) == "TZS 1,234.50"
    assert m.format_money(0) == "TZS 0.00"
    assert m.format_money(1_000_000) == "TZS 1,000,000.00"


def test_format_row():
    row = m.format_row("Pen", 3, 1.5)
    assert row == "Pen               3      1.50"
    assert len(row) == 29


def test_format_receipt():
    expected = (
        "Item            Qty     Total\n"
        "Pen               3      4.50\n"
        "Notebook         12    300.00\n"
        "TOTAL                  304.50"
    )
    assert m.format_receipt([("Pen", 3, 1.5), ("Notebook", 12, 25)]) == expected


def test_progress_bar():
    assert m.progress_bar(7, 20) == "[#######.............]  35.0%"
    assert m.progress_bar(25, 20) == "[####################] 100.0%"
    assert m.progress_bar(-3, 20) == "[....................]   0.0%"
    with pytest.raises(ValueError):
        m.progress_bar(1, 0)


@pytest.mark.parametrize("text, expected", [("  78 ", 78.0), ("78.5", 78.5), ("0", 0.0), ("100", 100.0)])
def test_parse_mark_valid(text, expected):
    assert m.parse_mark(text) == expected


@pytest.mark.parametrize("text", ["seventy", "", "101", "-1"])
def test_parse_mark_invalid(text):
    with pytest.raises(ValueError):
        m.parse_mark(text)


def test_format_table():
    out = m.format_table([["Pen", 3], ["Notebook", 12]], ["Item", "Qty"])
    assert out.splitlines() == ["Item      Qty", "Pen         3", "Notebook   12"]
