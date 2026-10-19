"""Domain model: amounts are integer cents (never floats)."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import date

CATEGORY_RE = re.compile(r"[a-z][a-z0-9_-]{0,29}")
AMOUNT_RE = re.compile(r"\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+(\.\d{1,2})?")
MAX_CENTS = 10**12


def parse_amount(text: str) -> int:
    """'12,000.5' -> 1200050 cents. ValueError for negatives, >2 decimals, junk, zero."""
    t = text.strip()
    if not AMOUNT_RE.fullmatch(t):
        raise ValueError(f"invalid amount {text!r} (use e.g. 1500 or 1,500.50)")
    whole, _, frac = t.replace(",", "").partition(".")
    cents = int(whole) * 100 + int((frac + "00")[:2])
    if cents <= 0 or cents > MAX_CENTS:
        raise ValueError("amount must be positive and realistic")
    return cents


def format_cents(cents: int) -> str:
    return f"{cents // 100:,}.{cents % 100:02d}"


def parse_category(text: str) -> str:
    c = text.strip().lower()
    if not CATEGORY_RE.fullmatch(c):
        raise ValueError(f"invalid category {text!r} (lowercase letters, digits, - or _)")
    return c


@dataclass(frozen=True)
class Expense:
    id: int
    spent_on: date
    category: str
    amount_cents: int
    note: str = ""

    def __post_init__(self):
        if self.amount_cents <= 0:
            raise ValueError("amount must be positive")
        if not CATEGORY_RE.fullmatch(self.category):
            raise ValueError("invalid category")

    def to_dict(self) -> dict:
        d = asdict(self)
        d["spent_on"] = self.spent_on.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Expense:
        return cls(id=int(d["id"]), spent_on=date.fromisoformat(d["spent_on"]),
                   category=d["category"], amount_cents=int(d["amount_cents"]), note=d.get("note", ""))
