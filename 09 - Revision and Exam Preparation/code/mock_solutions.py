"""Model solutions for the coding questions in MOCK-PY-01 (verified by tests/test_mock_py.py)."""
from __future__ import annotations


# B1 ---------------------------------------------------------------
BANDS = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]      # a designed scheme, not an official one


def grade(mark: float) -> str:
    if isinstance(mark, bool) or not isinstance(mark, (int, float)):
        raise TypeError("mark must be a number")
    if not 0 <= mark <= 100:
        raise ValueError("mark must be between 0 and 100")
    for floor, letter in BANDS:
        if mark >= floor:
            return letter
    raise AssertionError("unreachable")


# B2 ---------------------------------------------------------------
def course_averages(lines: list[str]) -> tuple[dict[str, float], int]:
    """Lines of 'student,course,mark' (first line is a header). Skip malformed lines; return (averages, skipped)."""
    totals: dict[str, list[float]] = {}
    skipped = 0
    for line in lines[1:]:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3 or not parts[0] or not parts[1]:
            skipped += 1
            continue
        try:
            mark = float(parts[2])
        except ValueError:
            skipped += 1
            continue
        if not 0 <= mark <= 100:
            skipped += 1
            continue
        totals.setdefault(parts[1], []).append(mark)
    return {c: round(sum(m) / len(m), 1) for c, m in sorted(totals.items())}, skipped


# B3 ---------------------------------------------------------------
class InsufficientStock(Exception):
    def __init__(self, sku: str, wanted: int, available: int) -> None:
        super().__init__(f"{sku}: wanted {wanted}, only {available} available")
        self.sku, self.wanted, self.available = sku, wanted, available


class Stock:
    def __init__(self) -> None:
        self._qty: dict[str, int] = {}

    def add(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("quantity must be positive")
        self._qty[sku] = self._qty.get(sku, 0) + qty

    def remove(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("quantity must be positive")
        available = self._qty.get(sku, 0)
        if qty > available:
            raise InsufficientStock(sku, qty, available)
        self._qty[sku] = available - qty

    def quantity(self, sku: str) -> int:
        return self._qty.get(sku, 0)

    def __len__(self) -> int:
        return sum(1 for q in self._qty.values() if q > 0)


# C1 (refactored version of the question's `fee` function) ---------
LATE_FEE_PER_DAY = 500
LATE_FEE_CAP = 10_000
LOST_ITEM_FEE = 25_000


def late_fee(days_late: int) -> int:
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    return min(days_late * LATE_FEE_PER_DAY, LATE_FEE_CAP)


def total_fee(days_late: int, lost: bool) -> int:
    return LOST_ITEM_FEE if lost else late_fee(days_late)


# C2 ---------------------------------------------------------------
def first_index(items: list[int], target: int) -> int:
    """Index of the first occurrence of target in a sorted list, or -1. O(log n)."""
    lo, hi, found = 0, len(items) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        elif items[mid] > target:
            hi = mid - 1
        else:
            found, hi = mid, mid - 1        # keep searching to the left
    return found
