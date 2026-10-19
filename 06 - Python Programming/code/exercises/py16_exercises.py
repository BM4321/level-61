"""PY16 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py16.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from math import gcd

class BankAccount:
    """Balance in cents; invariant: balance >= 0."""
    interest_rate = 0.02

    def __init__(self, owner: str, balance: int=0):
        raise NotImplementedError

    def deposit(self, amount: int) -> None:
        """Add a positive amount."""
        raise NotImplementedError

    def withdraw(self, amount: int) -> None:
        """Remove a positive amount not exceeding the balance."""
        raise NotImplementedError

    @property
    def balance(self) -> int:
        """Current balance (read-only)."""
        raise NotImplementedError

    def history(self) -> list[tuple[str, int]]:
        """A COPY of the transaction history."""
        raise NotImplementedError

    def transfer_to(self, other: BankAccount, amount: int) -> None:
        """Move money to another account, compensating if the deposit fails."""
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

class Rectangle:
    """Rectangle with positive sides."""

    def __init__(self, width: float, height: float):
        raise NotImplementedError

    @classmethod
    def square(cls, side: float) -> Rectangle:
        """Alternative constructor."""
        raise NotImplementedError

    @property
    def area(self) -> float:
        raise NotImplementedError

    @property
    def perimeter(self) -> float:
        raise NotImplementedError

class Fraction:
    """Immutable fraction in lowest terms with positive denominator."""

    def __init__(self, numerator: int, denominator: int=1):
        raise NotImplementedError

    @property
    def numerator(self) -> int:
        raise NotImplementedError

    @property
    def denominator(self) -> int:
        raise NotImplementedError

    @staticmethod
    def _coerce(other):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError
    __radd__ = __add__

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError
    __rmul__ = __mul__

    def __eq__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

@dataclass(frozen=True)
class Student:
    """Frozen student record; id must start with 'S'."""
    student_id: str
    name: str
    marks: tuple[float, ...] = field(default_factory=tuple)

    def __post_init__(self):
        raise NotImplementedError

    @property
    def average(self) -> float:
        raise NotImplementedError

    @property
    def grade(self) -> str:
        """Illustrative scale A>=70, B>=60, C>=50, D>=40, else F."""
        raise NotImplementedError

class Inventory:
    """Invariant: every stored quantity is a positive int."""

    def __init__(self):
        raise NotImplementedError

    def add(self, sku: str, qty: int) -> None:
        raise NotImplementedError

    def remove(self, sku: str, qty: int) -> None:
        raise NotImplementedError

    def quantity(self, sku: str) -> int:
        raise NotImplementedError

    def low_stock(self, threshold: int) -> list[str]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

@dataclass(frozen=True)
class Money:
    """Amount in integer minor units (e.g. cents) plus ISO currency code."""
    minor: int
    currency: str

    def _same_currency(self, other: Money) -> None:
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def allocate(self, ratios: list[int]) -> list[Money]:
        """Split by ratios so the parts sum exactly to the whole."""
        raise NotImplementedError
