"""PY-11: dicts, sets, comprehensions. Run: python examples/py11_dicts_sets.py"""
from collections import Counter, defaultdict

words = "the cat and the hat".split()
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts, Counter(words).most_common(1))

by_length = defaultdict(list)
for w in words:
    by_length[len(w)].append(w)
print(dict(by_length))

a, b = {1, 2, 3}, {3, 4}
print(a | b, a & b, a - b, a ^ b, type({}))

python, dm, cyber = {"S1", "S2", "S3", "S5"}, {"S2", "S3", "S4"}, {"S3"}
print("Python & DM but not Cyber:", (python & dm) - cyber)

grades = {"Ali": "B", "Bea": "A", "Chen": "B"}
print("lossy inversion:", {v: k for k, v in grades.items()})
