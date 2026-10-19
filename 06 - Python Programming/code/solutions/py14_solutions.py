"""PY-14 reference solutions (files, CSV, JSON)."""
import csv
import json
import os
import tempfile
from pathlib import Path

DEFAULTS = {"currency": "TZS", "decimals": 2, "categories": ["food", "transport"]}


def write_lines(path: Path, lines: list[str]) -> None:
    """Write each string followed by a newline (UTF-8)."""
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path: Path) -> list[str]:
    """Return the file's lines without newline characters."""
    with open(path, encoding="utf-8") as f:
        return f.read().splitlines()


def file_stats(path: Path) -> tuple[int, int]:
    """(line count, word count), reading lazily."""
    lines = words = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            lines += 1
            words += len(line.split())
    return lines, words


def load_marks(path: Path) -> tuple[dict[str, float], list[str]]:
    """Read a name,mark CSV -> (valid marks, error messages with line numbers)."""
    marks: dict[str, float] = {}
    errors: list[str] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = {"name", "mark"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        for line_no, row in enumerate(reader, start=2):
            name = (row["name"] or "").strip()
            try:
                mark = float(row["mark"])
            except (TypeError, ValueError):
                errors.append(f"line {line_no}: invalid mark {row['mark']!r}")
                continue
            if not name:
                errors.append(f"line {line_no}: empty name")
            elif not 0 <= mark <= 100:
                errors.append(f"line {line_no}: mark out of range {mark}")
            else:
                marks[name] = mark
    return marks, errors


def save_marks(path: Path, marks: dict[str, float]) -> None:
    """Write a name,mark CSV sorted by name."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "mark"])
        writer.writeheader()
        for name in sorted(marks):
            writer.writerow({"name": name, "mark": marks[name]})


def load_settings(path: Path) -> dict:
    """Defaults merged with a JSON object file; ValueError for unknown keys / non-objects."""
    if not path.exists():
        return dict(DEFAULTS)
    with path.open(encoding="utf-8") as f:
        user = json.load(f)
    if not isinstance(user, dict):
        raise ValueError("settings file must contain a JSON object")
    unknown = set(user) - set(DEFAULTS)
    if unknown:
        raise ValueError(f"unknown settings: {sorted(unknown)}")
    return {**DEFAULTS, **user}


def append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON object as a line."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    """Read JSON Lines, skipping blanks; ValueError listing corrupt line numbers."""
    records, bad = [], []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                bad.append(n)
    if bad:
        raise ValueError(f"corrupt lines: {bad}")
    return records


def atomic_write_json(path: Path, data) -> None:
    """Write JSON via temp file + os.replace so the target is never half-written."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except BaseException:
        os.unlink(tmp)
        raise
