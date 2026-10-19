"""Command-line interface: python -m marks report data/sample_marks.csv [--out results.csv]"""
import argparse
import sys
from pathlib import Path

from .report import compute_results, format_report
from .storage import load_marks, save_results


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="marks", description="Student marks and grading system")
    sub = p.add_subparsers(dest="command", required=True)
    rep = sub.add_parser("report", help="print a graded report from a CSV file")
    rep.add_argument("csv", type=Path)
    rep.add_argument("--out", type=Path, help="also save results to this CSV")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records, errors = load_marks(args.csv)
    except FileNotFoundError:
        print(f"error: file not found: {args.csv}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    results = compute_results(records)
    print(format_report(results, errors))
    if args.out:
        save_results(args.out, results)
        print(f"\nSaved {len(results)} results to {args.out}")
    return 0 if not errors else 1
