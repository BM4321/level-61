"""PY-16 reference solutions (classes and objects)."""
from __future__ import annotations

from dataclasses import dataclass, field
from math import gcd


class BankAccount:
    """Balance in cents; invariant: balance >= 0."""

    interest_rate = 0.02

    def __init__(self, owner: str, balance: int = 0):
        if not owner.strip():
            raise ValueError("owner is required")
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self._balance = balance
        self._history: list[tuple[str, int]] = []

    def deposit(self, amount: int) -> None:
        """Add a positive amount."""
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount
        self._history.append(("deposit", amount))

    def withdraw(self, amount: int) -> None:
        """Remove a positive amount not exceeding the balance."""
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._history.append(("withdraw", amount))

    @property
    def balance(self) -> int:
        """Current balance (read-only)."""
        return self._balance

    def history(self) -> list[tuple[str, int]]:
        """A COPY of the transaction history."""
        return list(self._history)

    def transfer_to(self, other: BankAccount, amount: int) -> None:
        """Move money to another account, compensating if the deposit fails."""
        self.withdraw(amount)
        try:
            other.deposit(amount)
        except Exception:
            self.deposit(amount)
            raise

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"


class Rectangle:
    """Rectangle with positive sides."""

    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("sides must be positive")
        self.width, self.height = width, height

    @classmethod
    def square(cls, side: float) -> Rectangle:
        """Alternative constructor."""
        return cls(side, side)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Fraction:
    """Immutable fraction in lowest terms with positive denominator."""

    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ZeroDivisionError("denominator cannot be zero")
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        g = gcd(numerator, denominator)
        self._n = numerator // g
        self._d = denominator // g

    @property
    def numerator(self) -> int:
        return self._n

    @property
    def denominator(self) -> int:
        return self._d

    @staticmethod
    def _coerce(other):
        if isinstance(other, int):
            return Fraction(other)
        if isinstance(other, Fraction):
            return other
        return None

    def __add__(self, other):
        o = Fraction._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self._n * o._d + o._n * self._d, self._d * o._d)

    __radd__ = __add__

    def __sub__(self, other):
        o = Fraction._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self._n * o._d - o._n * self._d, self._d * o._d)

    def __mul__(self, other):
        o = Fraction._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self._n * o._n, self._d * o._d)

    __rmul__ = __mul__

    def __eq__(self, other):
        o = Fraction._coerce(other)
        if o is None:
            return NotImplemented
        return (self._n, self._d) == (o._n, o._d)

    def __lt__(self, other):
        o = Fraction._coerce(other)
        if o is None:
            return NotImplemented
        return self._n * o._d < o._n * self._d

    def __hash__(self):
        return hash((self._n, self._d))

    def __repr__(self):
        return f"Fraction({self._n}, {self._d})"

    def __str__(self):
        return str(self._n) if self._d == 1 else f"{self._n}/{self._d}"


@dataclass(frozen=True)
class Student:
    """Frozen student record; id must start with 'S'."""

    student_id: str
    name: str
    marks: tuple[float, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not self.student_id.startswith("S"):
            raise ValueError("student_id must start with 'S'")

    @property
    def average(self) -> float:
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

    @property
    def grade(self) -> str:
        """Illustrative scale A>=70, B>=60, C>=50, D>=40, else F."""
        avg = self.average
        for threshold, letter in ((70, "A"), (60, "B"), (50, "C"), (40, "D")):
            if avg >= threshold:
                return letter
        return "F"


class Inventory:
    """Invariant: every stored quantity is a positive int."""

    def __init__(self):
        self._stock: dict[str, int] = {}

    def add(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def remove(self, sku: str, qty: int) -> None:
        have = self._stock.get(sku, 0)
        if qty <= 0 or qty > have:
            raise ValueError(f"cannot remove {qty} of {sku}; have {have}")
        if qty == have:
            del self._stock[sku]
        else:
            self._stock[sku] = have - qty

    def quantity(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def low_stock(self, threshold: int) -> list[str]:
        return sorted(s for s, q in self._stock.items() if q < threshold)

    def __len__(self) -> int:
        return len(self._stock)


@dataclass(frozen=True)
class Money:
    """Amount in integer minor units (e.g. cents) plus ISO currency code."""

    minor: int
    currency: str

    def _same_currency(self, other: Money) -> None:
        if other.currency != self.currency:
            raise ValueError("currency mismatch")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.minor + other.minor, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.minor - other.minor, self.currency)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self.minor < other.minor

    def allocate(self, ratios: list[int]) -> list[Money]:
        """Split by ratios so the parts sum exactly to the whole."""
        total = sum(ratios)
        if not ratios or total <= 0 or any(r < 0 for r in ratios):
            raise ValueError("ratios must be non-negative with positive sum")
        shares = [self.minor * r // total for r in ratios]
        remainder = self.minor - sum(shares)
        for i in range(remainder):
            shares[i % len(shares)] += 1
        return [Money(s, self.currency) for s in shares]
