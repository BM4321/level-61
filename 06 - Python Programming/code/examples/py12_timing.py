"""PY-12: empirical growth rates. Run: python examples/py12_timing.py

Doubling n should roughly quadruple insertion-sort time (quadratic) and roughly
double sorted() time (n log n). Your absolute numbers depend on your machine.
"""
import random
import sys
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py12_solutions import binary_search, insertion_sort, linear_search  # noqa: E402

previous = None
print(f"{'n':>6} {'insertion(s)':>13} {'ratio':>6} {'sorted(s)':>10}")
for n in (1000, 2000, 4000):
    data = [random.random() for _ in range(n)]
    t_ins = timeit.timeit(lambda: insertion_sort(data), number=3)
    t_builtin = timeit.timeit(lambda: sorted(data), number=3)
    ratio = f"{t_ins / previous:5.1f}x" if previous else "  -  "
    previous = t_ins
    print(f"{n:>6} {t_ins:>13.4f} {ratio:>6} {t_builtin:>10.5f}")

xs = list(range(1_000_000))
t_lin = timeit.timeit(lambda: linear_search(xs, 999_999), number=5)
t_bin = timeit.timeit(lambda: binary_search(xs, 999_999), number=5)
print(f"search 1e6 items: linear {t_lin:.4f}s vs binary {t_bin:.6f}s")
