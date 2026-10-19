import json

import pytest

from _target import load

m = load("py14")

SAMPLE = 'name,mark\nAmina,78\n"Baraka, J.",64\nChen,abc\nDan,120\n'


def test_lines_round_trip(tmp_path):
    p = tmp_path / "x.txt"
    m.write_lines(p, ["alpha", "beta", ""])
    assert m.read_lines(p) == ["alpha", "beta", ""]


def test_file_stats(tmp_path):
    p = tmp_path / "s.txt"
    p.write_text("a b\n\nc\n", encoding="utf-8")
    assert m.file_stats(p) == (3, 3)


def test_load_marks(tmp_path):
    p = tmp_path / "marks.csv"
    p.write_text(SAMPLE, encoding="utf-8")
    marks, errors = m.load_marks(p)
    assert marks == {"Amina": 78.0, "Baraka, J.": 64.0}
    assert errors == ["line 4: invalid mark 'abc'", "line 5: mark out of range 120.0"]


def test_load_marks_missing_column(tmp_path):
    p = tmp_path / "bad.csv"
    p.write_text("student,score\nA,1\n", encoding="utf-8")
    with pytest.raises(ValueError):
        m.load_marks(p)


def test_save_load_round_trip(tmp_path):
    p = tmp_path / "out.csv"
    data = {"Zawadi": 55, "Baraka, J.": 64.5, "Amina": 78}
    m.save_marks(p, data)
    assert p.read_text(encoding="utf-8").splitlines()[1] == "Amina,78"
    assert m.load_marks(p) == ({k: float(v) for k, v in data.items()}, [])


def test_load_settings(tmp_path):
    p = tmp_path / "settings.json"
    assert m.load_settings(p)["currency"] == "TZS"
    p.write_text(json.dumps({"decimals": 0}), encoding="utf-8")
    assert m.load_settings(p)["decimals"] == 0
    p.write_text(json.dumps({"curency": "USD"}), encoding="utf-8")
    with pytest.raises(ValueError):
        m.load_settings(p)
    p.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(ValueError):
        m.load_settings(p)


def test_defaults_not_mutated(tmp_path):
    s = m.load_settings(tmp_path / "none.json")
    s["currency"] = "XXX"
    assert m.load_settings(tmp_path / "none.json")["currency"] == "TZS"


def test_jsonl(tmp_path):
    p = tmp_path / "log.jsonl"
    m.append_jsonl(p, {"event": "login", "user": "amina"})
    m.append_jsonl(p, {"event": "logout"})
    assert m.read_jsonl(p) == [{"event": "login", "user": "amina"}, {"event": "logout"}]
    with open(p, "a", encoding="utf-8") as f:
        f.write("\n{broken\n")
    with pytest.raises(ValueError, match=r"\[4\]"):
        m.read_jsonl(p)


def test_atomic_write_preserves_original(tmp_path):
    p = tmp_path / "data.json"
    m.atomic_write_json(p, {"ok": 1})
    with pytest.raises(TypeError):
        m.atomic_write_json(p, {"bad": {1, 2}})
    assert json.loads(p.read_text(encoding="utf-8")) == {"ok": 1}
    assert list(tmp_path.glob("*.tmp")) == []
