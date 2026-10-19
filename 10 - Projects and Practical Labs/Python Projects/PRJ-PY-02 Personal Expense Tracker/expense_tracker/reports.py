"""Pure reporting functions over lists of Expense (no file access)."""
from collections import defaultdict
from datetime import date

from .models import Expense, format_cents


def month_key(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def filter_expenses(expenses: list[Expense], month: str | None = None, category: str | None = None) -> list[Expense]:
    return [e for e in expenses
            if (month is None or month_key(e.spent_on) == month)
            and (category is None or e.category == category)]


def totals_by_category(expenses: list[Expense]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for e in expenses:
        totals[e.category] += e.amount_cents
    return dict(sorted(totals.items(), key=lambda kv: (-kv[1], kv[0])))


def budget_status(expenses: list[Expense], budgets: dict[tuple[str, str], int], month: str) -> list[dict]:
    spent = totals_by_category(filter_expenses(expenses, month=month))
    rows = []
    for (category, m), limit in sorted(budgets.items()):
        if m != month:
            continue
        used = spent.get(category, 0)
        rows.append({"category": category, "limit": limit, "spent": used, "remaining": limit - used,
                     "over": used > limit})
    return rows


def format_list(expenses: list[Expense]) -> str:
    lines = [f"{'ID':>4}  {'Date':<10}  {'Category':<12} {'Amount':>12}  Note"]
    for e in sorted(expenses, key=lambda e: (e.spent_on, e.id)):
        lines.append(f"{e.id:>4}  {e.spent_on.isoformat():<10}  {e.category:<12} {format_cents(e.amount_cents):>12}  {e.note}")
    total = sum(e.amount_cents for e in expenses)
    lines.append(f"{'':>4}  {'':<10}  {'TOTAL':<12} {format_cents(total):>12}")
    return "\n".join(lines)


def format_summary(expenses: list[Expense]) -> str:
    totals = totals_by_category(expenses)
    grand = sum(totals.values()) or 1
    lines = [f"{'Category':<12} {'Total':>12} {'Share':>6}"]
    for cat, cents in totals.items():
        lines.append(f"{cat:<12} {format_cents(cents):>12} {cents / grand:>6.1%}")
    return "\n".join(lines)
