"""Minimal statement-coverage measurement (standard library only), for when coverage.py is unavailable.

Usage:  python line_coverage.py labbook            # runs the test suite, reports per-file coverage
It approximates coverage.py: executable lines come from compiled code objects; executed lines from
sys.settrace. Use coverage.py (pip install coverage) for real projects.
"""
from __future__ import annotations

import os
import sys
import threading
import types


def executable_lines(path: str) -> set[int]:
    with open(path, encoding="utf-8") as f:
        code = compile(f.read(), path, "exec")
    lines: set[int] = set()
    stack = [code]
    while stack:
        c = stack.pop()
        lines.update(line for _s, _e, line in c.co_lines() if line)
        stack.extend(k for k in c.co_consts if isinstance(k, types.CodeType))
    return lines


def measure(package: str, test_args: list[str]) -> dict[str, tuple[int, int, list[int]]]:
    root = os.path.abspath(package)
    hits: dict[str, set[int]] = {}

    def tracer(frame, event, arg):
        fn = os.path.abspath(frame.f_code.co_filename)
        if not fn.startswith(root):
            return None
        hits.setdefault(fn, set()).add(frame.f_lineno)

        def local(frame, event, arg):
            if event == "line":
                hits[fn].add(frame.f_lineno)
            return local
        return local

    import pytest
    sys.settrace(tracer)
    threading.settrace(tracer)
    try:
        code = pytest.main(test_args + ["-q", "-p", "no:cacheprovider"])
    finally:
        sys.settrace(None)
        threading.settrace(None)
    if code != 0:
        raise SystemExit(f"tests failed (exit {code})")
    report = {}
    for dirpath, _d, files in os.walk(root):
        for name in sorted(files):
            if name.endswith(".py"):
                p = os.path.join(dirpath, name)
                exe = executable_lines(p)
                hit = hits.get(p, set()) & exe
                report[os.path.relpath(p)] = (len(exe), len(hit), sorted(exe - hit))
    return report


if __name__ == "__main__":
    pkg = sys.argv[1] if len(sys.argv) > 1 else "labbook"
    rep = measure(pkg, ["tests"])
    total_exe = sum(e for e, _h, _m in rep.values())
    total_hit = sum(h for _e, h, _m in rep.values())
    print(f"{'file':28} {'stmts':>5} {'hit':>5} {'cover':>6}  missing lines")
    for f, (e, h, missing) in rep.items():
        print(f"{f:28} {e:5} {h:5} {100 * h / e if e else 100:5.0f}%  {missing}")
    print(f"{'TOTAL':28} {total_exe:5} {total_hit:5} {100 * total_hit / total_exe:5.0f}%")
