"""CSV input/output with per-row validation (never crash on one bad row)."""
import csv
from pathlib import Path

from .grading import validate_mark

REQUIRED = ("student_id", "name", "coursework", "exam")


def _parse_mark(text: str | None, field: str) -> float:
    if text is None or not text.strip():
        raise ValueError(f"{field} is missing")
    try:
        value = float(text)
    except ValueError:
        raise ValueError(f"{field} is not a number: {text!r}") from None
    return validate_mark(value, field)


def load_marks(path: Path) -> tuple[list[dict], list[str]]:
    """Return (valid records, error messages with line numbers)."""
    records, errors, seen = [], [], set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"CSV is missing columns: {', '.join(missing)}")
        for line_no, row in enumerate(reader, start=2):
            sid = (row["student_id"] or "").strip()
            name = (row["name"] or "").strip()
            try:
                if not sid or not name:
                    raise ValueError("student_id and name are required")
                if sid in seen:
                    raise ValueError(f"duplicate student_id {sid}")
                cw = _parse_mark(row["coursework"], "coursework")
                ex = _parse_mark(row["exam"], "exam")
            except ValueError as exc:
                errors.append(f"line {line_no}: {exc}")
                continue
            seen.add(sid)
            records.append({"student_id": sid, "name": name, "coursework": cw, "exam": ex})
    return records, errors


def save_results(path: Path, results: list[dict]) -> None:
    fields = ["rank", "student_id", "name", "coursework", "exam", "final", "grade"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
