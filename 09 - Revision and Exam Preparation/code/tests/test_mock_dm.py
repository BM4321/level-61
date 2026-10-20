import math
from fractions import Fraction
from itertools import product

from x_tools import dijkstra, kruskal, path_to, undirected

B = [False, True]


def test_q1_logic():
    assert all((not ((not p) or q)) == (p and not q) for p, q in product(B, B))
    syllogism = lambda p, q, r: (not (((not p) or q) and ((not q) or r))) or ((not p) or r)  # noqa: E731
    assert all(syllogism(*v) for v in product(B, B, B))


def test_q2_sets_relations_functions():
    union = 70 + 50 + 40 - 25 - 20 - 15 + 10
    assert (union, 120 - union) == (110, 10)
    A = [1, 2, 3, 4]
    R = {(1, 1), (2, 2), (3, 3), (4, 4), (1, 2), (2, 1), (3, 4), (4, 3)}
    assert all((a, a) in R for a in A)
    assert all((b, a) in R for a, b in R)
    assert all((a, d) in R for a, b in R for c, d in R if b == c)
    classes = {frozenset(b for b in A if (a, b) in R) for a in A}
    assert classes == {frozenset({1, 2}), frozenset({3, 4})}
    images = {2 * n + 3 for n in range(-50, 50)}
    assert len(images) == 100 and 4 not in images


def test_q3_identities():
    assert all(sum(2 * i - 1 for i in range(1, n + 1)) == n * n for n in range(1, 200))
    assert all((n * n) % 2 == 1 for n in range(-99, 100, 2))


def test_q4_counting():
    c = math.comb
    assert c(10, 4) == 210 and c(10, 4) - c(6, 4) == 195
    assert c(4, 1) * c(6, 3) + c(4, 2) * c(6, 2) + c(4, 3) * c(6, 1) + c(4, 4) == 195
    assert [c(4, 1) * c(6, 3), c(4, 2) * c(6, 2), c(4, 3) * c(6, 1)] == [80, 90, 24]
    assert 26 ** 2 * 10 ** 4 == 6_760_000 and math.perm(8, 3) == 336
    assert math.factorial(5) // (math.factorial(2) ** 2) == 30
    assert math.ceil(30 / 12) == 3 and 12 * 2 < 30


def test_q5_binomial_and_recurrence():
    assert math.comb(5, 3) * 2 ** 3 * (-1) ** 2 == 80
    a = [2, 3]
    for _ in range(2, 20):
        a.append(3 * a[-1] - 2 * a[-2])
    assert a == [1 + 2 ** n for n in range(20)] and a[2:4] == [5, 9]


def test_q6_graphs():
    edges = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2)]
    dist, prev = dijkstra(undirected(edges), "A")
    assert dist == {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10}
    assert path_to(prev, "A", "E") == ["A", "C", "B", "D", "E"]
    mst, total = kruskal(edges)
    assert total == 10 and {frozenset(e[:2]) for e in mst} == {frozenset(p) for p in ("BC", "AC", "DE", "BD")}
    degrees = [3, 3, 2, 2, 2]
    assert sum(degrees) // 2 == 6 and sum(d % 2 for d in degrees) == 2


def test_q7_boolean():
    f = lambda x, y: (x and y) or (x and not y) or ((not x) and y)  # noqa: E731
    assert all(bool(f(x, y)) == (x or y) for x, y in product(B, B))


def test_q8_probability():
    p_six = 1 - Fraction(5, 6) ** 4
    assert p_six == Fraction(671, 1296) and round(float(p_six), 3) == 0.518
    post = 0.02 * 0.95 / (0.02 * 0.95 + 0.98 * 0.10)
    assert round(0.02 * 0.95 + 0.98 * 0.10, 3) == 0.117 and round(post, 3) == 0.162
