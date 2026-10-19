"""PY-03 reference solutions."""


def format_money(amount: float) -> str:
    return f"TZS {amount:,.2f}"


def format_row(name: str, qty: int, price: float) -> str:
    return f"{name:<14}{qty:>5}{price:>10.2f}"


def format_receipt(items: list[tuple[str, int, float]]) -> str:
    lines = [f"{'Item':<14}{'Qty':>5}{'Total':>10}"]
    grand = 0.0
    for name, qty, price in items:
        line_total = qty * price
        grand += line_total
        lines.append(f"{name:<14}{qty:>5}{line_total:>10.2f}")
    lines.append(f"{'TOTAL':<19}{grand:>10.2f}")
    return "\n".join(lines)


def progress_bar(done: int, total: int, width: int = 20) -> str:
    if total <= 0:
        raise ValueError("total must be positive")
    done = max(0, min(done, total))
    fraction = done / total
    filled = int(fraction * width)
    return f"[{'#' * filled}{'.' * (width - filled)}] {fraction:6.1%}"


def parse_mark(text: str) -> float:
    cleaned = text.strip()
    try:
        value = float(cleaned)
    except ValueError:
        raise ValueError(f"not a number: {text!r}") from None
    if not 0 <= value <= 100:
        raise ValueError(f"mark out of range 0-100: {value}")
    return value


def format_table(rows: list[list], headers: list[str]) -> str:
    table = [headers] + rows
    widths = [max(len(str(r[c])) for r in table) for c in range(len(headers))]

    def fmt(cell, w):
        return f"{cell:>{w}}" if isinstance(cell, (int, float)) else f"{str(cell):<{w}}"

    return "\n".join("  ".join(fmt(cell, w) for cell, w in zip(row, widths)) for row in table)
