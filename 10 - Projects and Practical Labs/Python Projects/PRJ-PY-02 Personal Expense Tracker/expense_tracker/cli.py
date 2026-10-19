"""CLI: python -m expense_tracker [--data FILE] {add,list,summary,budget,delete,export,import} ..."""
import argparse
import sys
from datetime import date
from pathlib import Path

from .models import format_cents, parse_amount, parse_category
from .reports import budget_status, filter_expenses, format_list, format_summary, month_key
from .storage import JsonRepository, StorageError, export_csv, import_csv


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="expense_tracker", description="Personal expense tracker")
    p.add_argument("--data", type=Path, default=Path("expenses.json"), help="data file (default: expenses.json)")
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add")
    a.add_argument("amount")
    a.add_argument("category")
    a.add_argument("note", nargs="?", default="")
    a.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    ls = sub.add_parser("list")
    ls.add_argument("--month")
    ls.add_argument("--category")
    sm = sub.add_parser("summary")
    sm.add_argument("--month")
    b = sub.add_parser("budget")
    b.add_argument("category")
    b.add_argument("limit")
    b.add_argument("--month", default=None)
    st = sub.add_parser("status")
    st.add_argument("--month", default=None)
    d = sub.add_parser("delete")
    d.add_argument("id", type=int)
    e = sub.add_parser("export")
    e.add_argument("csv", type=Path)
    i = sub.add_parser("import")
    i.add_argument("csv", type=Path)
    return p


def main(argv: list[str] | None = None, today: date | None = None) -> int:
    args = build_parser().parse_args(argv)
    today = today or date.today()
    try:
        repo = JsonRepository(args.data)
        if args.command == "add":
            spent_on = date.fromisoformat(args.date) if args.date else today
            exp = repo.add(spent_on, parse_category(args.category), parse_amount(args.amount), args.note)
            print(f"Added #{exp.id}: {format_cents(exp.amount_cents)} on {exp.category} ({exp.spent_on})")
        elif args.command == "list":
            print(format_list(filter_expenses(repo.all(), args.month, args.category)))
        elif args.command == "summary":
            print(format_summary(filter_expenses(repo.all(), args.month)))
        elif args.command == "budget":
            month = args.month or month_key(today)
            repo.set_budget(parse_category(args.category), month, parse_amount(args.limit))
            print(f"Budget for {args.category} in {month} set to {args.limit}")
        elif args.command == "status":
            month = args.month or month_key(today)
            for row in budget_status(repo.all(), repo.budgets(), month):
                flag = "OVER" if row["over"] else "ok"
                print(f"{row['category']:<12} spent {format_cents(row['spent']):>12} of "
                      f"{format_cents(row['limit']):>12}  [{flag}]")
        elif args.command == "delete":
            repo.delete(args.id)
            print(f"Deleted #{args.id}")
        elif args.command == "export":
            export_csv(args.csv, repo.all())
            print(f"Exported to {args.csv}")
        elif args.command == "import":
            n, errors = import_csv(args.csv, repo)
            print(f"Imported {n} expenses")
            for err in errors:
                print("  rejected", err)
            return 1 if errors else 0
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except StorageError as exc:
        print(f"storage error: {exc}", file=sys.stderr)
        return 2
    return 0
