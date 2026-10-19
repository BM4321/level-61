"""Pure functions that compute results and format the report (no printing here)."""
from .grading import final_mark, has_passed, letter_grade
from .stats import distribution, mean, median, rank, std_dev


def compute_results(records: list[dict]) -> list[dict]:
    results = []
    for r in records:
        final = final_mark(r["coursework"], r["exam"])
        results.append({**r, "final": final, "grade": letter_grade(final)})
    return rank(results)


def summary(results: list[dict]) -> dict:
    finals = [r["final"] for r in results]
    return {
        "count": len(finals),
        "mean": round(mean(finals), 1),
        "median": round(median(finals), 1),
        "std_dev": round(std_dev(finals), 1),
        "min": min(finals),
        "max": max(finals),
        "pass_rate": round(100 * sum(has_passed(x) for x in finals) / len(finals), 1),
        "distribution": distribution([r["grade"] for r in results]),
    }


def format_report(results: list[dict], errors: list[str]) -> str:
    lines = [f"{'Rank':>4}  {'ID':<6} {'Name':<18} {'CW':>5} {'Exam':>5} {'Final':>6} Grade",
             "-" * 56]
    for r in results:
        lines.append(f"{r['rank']:>4}  {r['student_id']:<6} {r['name']:<18} "
                     f"{r['coursework']:>5.1f} {r['exam']:>5.1f} {r['final']:>6.1f} {r['grade']:>3}")
    if results:
        s = summary(results)
        lines += ["-" * 56,
                  f"Students: {s['count']}  Mean: {s['mean']}  Median: {s['median']}  "
                  f"SD: {s['std_dev']}  Min: {s['min']}  Max: {s['max']}",
                  f"Pass rate: {s['pass_rate']}%   Grades: "
                  + "  ".join(f"{k}={v}" for k, v in s["distribution"].items())]
    if errors:
        lines += ["", f"Rejected rows ({len(errors)}):"] + [f"  - {e}" for e in errors]
    return "\n".join(lines)
