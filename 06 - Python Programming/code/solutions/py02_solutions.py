"""PY-02 reference solutions."""


def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def split_seconds(total: int) -> tuple[int, int, int]:
    hours, rest = divmod(total, 3600)
    minutes, seconds = divmod(rest, 60)
    return hours, minutes, seconds


def is_even(n: int) -> bool:
    return n % 2 == 0


def vat_inclusive_cents(price_cents: int, rate_percent: int) -> int:
    vat = (price_cents * rate_percent + 50) // 100
    return price_cents + vat


def digit_sum(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


def format_duration(seconds: int) -> str:
    if seconds < 0:
        raise ValueError("duration cannot be negative")
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    if m:
        return f"{m}m {s:02d}s"
    return f"{s}s"
