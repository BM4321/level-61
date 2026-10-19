"""JSON repository with atomic writes, plus CSV import/export."""
from __future__ import annotations

import csv
import json
import os
import tempfile
from datetime import date
from pathlib import Path

from .models import Expense, parse_amount, parse_category

SCHEMA_VERSION = 1


class StorageError(Exception):
    """The data file exists but is unreadable or corrupt."""


class JsonRepository:
    """Stores {"version": 1, "next_id": n, "expenses": [...], "budgets": {...}} in one JSON file."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {"version": SCHEMA_VERSION, "next_id": 1, "expenses": [], "budgets": {}}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise StorageError(f"{self.path} is corrupt (line {exc.lineno}); restore from backup") from exc
        if data.get("version") != SCHEMA_VERSION:
            raise StorageError(f"unsupported data version {data.get('version')}")
        return data

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self.path)
        except BaseException:
            os.unlink(tmp)
            raise

    def add(self, spent_on: date, category: str, amount_cents: int, note: str = "") -> Expense:
        exp = Expense(self._data["next_id"], spent_on, category, amount_cents, note)
        self._data["expenses"].append(exp.to_dict())
        self._data["next_id"] += 1
        self._save()
        return exp

    def all(self) -> list[Expense]:
        return [Expense.from_dict(d) for d in self._data["expenses"]]

    def delete(self, expense_id: int) -> None:
        before = len(self._data["expenses"])
        self._data["expenses"] = [d for d in self._data["expenses"] if d["id"] != expense_id]
        if len(self._data["expenses"]) == before:
            raise KeyError(f"no expense with id {expense_id}")
        self._save()

    def set_budget(self, category: str, month: str, limit_cents: int) -> None:
        self._data["budgets"][f"{category}:{month}"] = limit_cents
        self._save()

    def budgets(self) -> dict[tuple[str, str], int]:
        return {tuple(k.split(":", 1)): v for k, v in self._data["budgets"].items()}


def export_csv(path: Path, expenses: list[Expense]) -> None:
    risky = ("=", "+", "-", "@")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "category", "amount", "note"])
        for e in expenses:
            note = "'" + e.note if e.note.startswith(risky) else e.note   # CSV formula-injection guard
            w.writerow([e.id, e.spent_on.isoformat(), e.category, f"{e.amount_cents / 100:.2f}", note])


def import_csv(path: Path, repo: JsonRepository) -> tuple[int, list[str]]:
    """Import rows date,category,amount,note. Returns (imported count, errors)."""
    imported, errors = 0, []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            try:
                if None in row:          # DictReader puts surplus fields under the key None
                    raise ValueError("too many fields (unquoted comma in an amount or note?)")
                spent_on = date.fromisoformat((row.get("date") or "").strip())
                category = parse_category(row.get("category") or "")
                cents = parse_amount(row.get("amount") or "")
            except ValueError as exc:
                errors.append(f"line {line_no}: {exc}")
                continue
            repo.add(spent_on, category, cents, (row.get("note") or "").strip())
            imported += 1
    return imported, errors
