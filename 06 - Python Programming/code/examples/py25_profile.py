"""PY-25: profile a slow function, then compare with the fixed one.
Run: python -m cProfile -s cumtime examples/py25_profile.py | head -25
"""
import random
import sys
import time
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py25_solutions import keyword_counts_fast, keyword_counts_slow  # noqa: E402

rng = random.Random(25)
vocab = [f"word{i}" for i in range(500)]
docs = [" ".join(rng.choice(vocab) for _ in range(50)) for _ in range(400)]
stop = vocab[:100]


def main():
    t0 = time.perf_counter()
    slow = keyword_counts_slow(docs, stop)
    t1 = time.perf_counter()
    fast = keyword_counts_fast(docs, stop)
    t2 = time.perf_counter()
    assert slow == fast
    print(f"slow: {t1 - t0:.3f}s  fast: {t2 - t1:.4f}s  speed-up ≈ {(t1 - t0) / (t2 - t1):.0f}x")
    setup = "data = list(range(10_000)); targets = list(range(0, 20_000, 7))"
    t_list = timeit.timeit("[t in data for t in targets]", setup=setup, number=3)
    t_set = timeit.timeit("s = set(data); [t in s for t in targets]", setup=setup, number=3)
    print(f"membership: list {t_list:.3f}s vs set {t_set:.5f}s")


if __name__ == "__main__":
    main()
