"""Grading rules (illustrative scale: A>=70, B>=60, C>=50, D>=40, else F)."""

_BANDS = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]


def grade(mark: float) -> str:
    if not 0 <= mark <= 100:
        raise ValueError(f"mark out of range: {mark}")
    for threshold, letter in _BANDS:
        if mark >= threshold:
            return letter
    raise AssertionError("unreachable")


if __name__ == "__main__":  # python -m gradebook.grading
    print([grade(m) for m in (35, 55, 75)])
