"""PY-19 reference solutions (typed, documented, refactored code)."""
from collections.abc import Callable

GRADE_BANDS: list[tuple[float, str]] = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]
COURSE_CAPACITY = 40
VAT_RATE = 0.18
MAX_AMOUNT = 1_000_000


def weighted_average(marks: list[float], weights: list[float]) -> float:
    """Weighted mean of marks.

    Raises:
        ValueError: lengths differ, a weight is negative, or all weights are zero.
    """
    if len(marks) != len(weights):
        raise ValueError("marks and weights must have the same length")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("weights must not all be zero")
    return sum(m * w for m, w in zip(marks, weights)) / total_weight


def letter_grade(mark: float, bands: list[tuple[float, str]] = GRADE_BANDS) -> str:
    """Letter for mark using a (threshold, letter) table sorted high -> low."""
    for threshold, letter in bands:
        if mark >= threshold:
            return letter
    raise ValueError(f"mark below lowest band: {mark}")


def grade_report(marks: dict[str, float],
                 name_format: Callable[[str], str] = lambda s: s,
                 bands: list[tuple[float, str]] = GRADE_BANDS) -> str:
    """'name: mark letter' lines plus 'AVG: x'; ValueError if marks is empty."""
    if not marks:
        raise ValueError("no marks")
    lines = [f"{name_format(name)}: {mark} {letter_grade(mark, bands)}" for name, mark in marks.items()]
    average = sum(marks.values()) / len(marks)
    lines.append(f"AVG: {round(average, 1)}")
    return "\n".join(lines)


def can_register(student: dict | None, course: dict) -> bool:
    """Guard-clause version of the nested original."""
    if student is None or not student["fees_paid"]:
        return False
    if len(course["enrolled"]) >= COURSE_CAPACITY:
        return False
    return student["id"] not in course["enrolled"]


def is_valid_tzs_amount(tx: dict) -> bool:
    """TZS amount strictly between 0 and MAX_AMOUNT."""
    return tx["currency"] == "TZS" and 0 < tx["amount"] < MAX_AMOUNT


def valid_amounts(transactions: list[dict]) -> list[float]:
    """Amounts of valid TZS transactions."""
    return [tx["amount"] for tx in transactions if is_valid_tzs_amount(tx)]


def total_with_vat(transactions: list[dict]) -> float:
    """Sum of valid amounts including VAT (was mode 1)."""
    return sum(a * (1 + VAT_RATE) for a in valid_amounts(transactions))


def total_without_vat(transactions: list[dict]) -> float:
    """Sum of valid amounts (was mode 2)."""
    return sum(valid_amounts(transactions))
