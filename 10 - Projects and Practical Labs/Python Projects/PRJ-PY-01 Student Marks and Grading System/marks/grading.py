"""Grading rules. ILLUSTRATIVE scale and weights: replace with your institution's official rules."""

COURSEWORK_WEIGHT = 0.4
EXAM_WEIGHT = 0.6
GRADE_BANDS: list[tuple[float, str]] = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]
PASS_MARK = 40


def validate_mark(value: float, field: str) -> float:
    """Return value if 0 <= value <= 100, else raise ValueError naming the field."""
    if not 0 <= value <= 100:
        raise ValueError(f"{field} must be between 0 and 100, got {value}")
    return value


def final_mark(coursework: float, exam: float) -> float:
    """Weighted final mark rounded to 1 decimal place."""
    validate_mark(coursework, "coursework")
    validate_mark(exam, "exam")
    return round(COURSEWORK_WEIGHT * coursework + EXAM_WEIGHT * exam, 1)


def letter_grade(mark: float) -> str:
    """Letter grade for a final mark using GRADE_BANDS."""
    validate_mark(mark, "mark")
    for threshold, letter in GRADE_BANDS:
        if mark >= threshold:
            return letter
    raise AssertionError("unreachable: bands cover 0-100")


def has_passed(mark: float) -> bool:
    return mark >= PASS_MARK
