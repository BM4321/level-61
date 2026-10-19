"""Entities and value objects."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    year: int
    copies: int = 1

    def __post_init__(self):
        if not self.book_id or not self.title.strip():
            raise ValueError("book_id and title are required")
        if self.copies < 1:
            raise ValueError("copies must be >= 1")


@dataclass
class Member:
    member_id: str
    name: str
    fines_cents: int = 0
    active: bool = True

    def __post_init__(self):
        if not self.member_id or not self.name.strip():
            raise ValueError("member_id and name are required")


@dataclass
class Loan:
    loan_id: int
    book_id: str
    member_id: str
    borrowed_on: date
    due_on: date
    returned_on: date | None = None

    @property
    def is_open(self) -> bool:
        return self.returned_on is None

    def days_overdue(self, today: date) -> int:
        end = self.returned_on or today
        return max(0, (end - self.due_on).days)


@dataclass
class Policy:
    """Lending rules in one place (illustrative values)."""
    max_loans: int = 3
    loan_days: int = 14
    fine_per_day_cents: int = 50_00       # 50.00 per overdue day
    max_fine_before_block_cents: int = 1_000_00
