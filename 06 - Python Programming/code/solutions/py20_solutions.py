"""PY-20 reference solutions (TDD katas and fixed bug)."""

ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
         (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def int_to_roman(n: int, lowercase: bool = False) -> str:
    """1..3999 -> canonical Roman numeral; ValueError outside the range."""
    if not 1 <= n <= 3999:
        raise ValueError("roman numerals cover 1..3999")
    out = []
    for value, symbol in ROMAN:
        count, n = divmod(n, value)
        out.append(symbol * count)
    result = "".join(out)
    return result.lower() if lowercase else result


def roman_to_int(s: str) -> int:
    """Canonical Roman numeral -> int; ValueError for invalid or non-canonical input."""
    if not s or any(ch not in VALUES for ch in s):
        raise ValueError(f"invalid roman numeral {s!r}")
    total = 0
    for i, ch in enumerate(s):
        v = VALUES[ch]
        if i + 1 < len(s) and v < VALUES[s[i + 1]]:
            total -= v
        else:
            total += v
    if not 1 <= total <= 3999 or int_to_roman(total) != s:
        raise ValueError(f"non-canonical roman numeral {s!r}")
    return total


def average_passing(marks: list[float], pass_mark: float = 50) -> float:
    """Mean of marks >= pass_mark; ValueError if none pass."""
    passing = [m for m in marks if m >= pass_mark]
    if not passing:
        raise ValueError("no passing marks")
    return sum(passing) / len(passing)


def password_issues(pw: str, common: set[str]) -> list[str]:
    """List of problems: 'too short' (<12), 'no digit', 'no letter', 'too common'."""
    issues = []
    if len(pw) < 12:
        issues.append("too short")
    if not any(c.isdigit() for c in pw):
        issues.append("no digit")
    if not any(c.isalpha() for c in pw):
        issues.append("no letter")
    if pw.lower() in common:
        issues.append("too common")
    return issues
