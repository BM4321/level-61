"""PY19 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py19.py
"""

from collections.abc import Callable
GRADE_BANDS: list[tuple[float, str]] = [(70, 'A'), (60, 'B'), (50, 'C'), (40, 'D'), (0, 'F')]
COURSE_CAPACITY = 40
VAT_RATE = 0.18
MAX_AMOUNT = 1000000

def weighted_average(marks: list[float], weights: list[float]) -> float:
    """Weighted mean of marks.

Raises:
    ValueError: lengths differ, a weight is negative, or all weights are zero."""
    raise NotImplementedError

def letter_grade(mark: float, bands: list[tuple[float, str]]=GRADE_BANDS) -> str:
    """Letter for mark using a (threshold, letter) table sorted high -> low."""
    raise NotImplementedError

def grade_report(marks: dict[str, float], name_format: Callable[[str], str]=lambda s: s, bands: list[tuple[float, str]]=GRADE_BANDS) -> str:
    """'name: mark letter' lines plus 'AVG: x'; ValueError if marks is empty."""
    raise NotImplementedError

def can_register(student: dict | None, course: dict) -> bool:
    """Guard-clause version of the nested original."""
    raise NotImplementedError

def is_valid_tzs_amount(tx: dict) -> bool:
    """TZS amount strictly between 0 and MAX_AMOUNT."""
    raise NotImplementedError

def valid_amounts(transactions: list[dict]) -> list[float]:
    """Amounts of valid TZS transactions."""
    raise NotImplementedError

def total_with_vat(transactions: list[dict]) -> float:
    """Sum of valid amounts including VAT (was mode 1)."""
    raise NotImplementedError

def total_without_vat(transactions: list[dict]) -> float:
    """Sum of valid amounts (was mode 2)."""
    raise NotImplementedError
