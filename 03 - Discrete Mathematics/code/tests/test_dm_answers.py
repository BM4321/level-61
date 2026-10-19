"""Machine checks of the worked answers in the DM lessons (one section per lesson)."""
import itertools
import math

from dm_tools import *  # noqa: F403


def rows(n):
    return itertools.product([True, False], repeat=n)


# ------------------------------------------------------------------ DM-01
def test_dm01_examples():
    assert is_tautology("((p -> q) and (q -> r)) -> (p -> r)", ["p", "q", "r"])
    assert is_tautology("(p -> q) <-> (not q -> not p)", ["p", "q"])
    # knights & knaves example 3: a <-> not b and b <-> (a <-> b)
    sols = [(a, b) for a, b in rows(2) if evaluate("(a <-> not b) and (b <-> (a <-> b))", {"a": a, "b": b})]
    assert sols == [(True, False)]


def test_dm01_practice():
    assert is_tautology("not (p or q) -> not p", ["p", "q"])
    assert is_tautology("(p and q) -> p", ["p", "q"])
    assert is_contradiction("p and not (p or q)", ["p", "q"])
    assert not is_tautology("(p -> q) -> p", ["p", "q"]) and not is_contradiction("(p -> q) -> p", ["p", "q"])
    granted = sum(evaluate("P and (D or O)", dict(zip("PDO", v))) for v in rows(3))
    assert granted == 3
    sols = [(a, b) for a, b in rows(2) if evaluate("a <-> (not a or not b)", {"a": a, "b": b})]
    assert sols == [(True, False)]
    env = {"C": True, "J": True, "E": False, "B": False}
    assert evaluate("C and (J or (E and B))", env) and not evaluate("C and (J or E) and B", env)


# ------------------------------------------------------------------ DM-02
def test_dm02():
    V2, V3 = ["p", "q"], ["p", "q", "r"]
    assert equivalent("not (p or (not p and q))", "not p and not q", V2)
    assert is_tautology("(p and q) -> (p or q)", V2)
    assert equivalent("not ((L and not M) -> X)", "(L and not M) and not X", ["L", "M", "X"])
    majority_dnf = "(p and q) or (p and r) or (q and r)"
    assert minterms(majority_dnf, V3) == [3, 5, 6, 7]
    assert equivalent(majority_dnf, "(p or q) and (p or r) and (q or r)", V3)
    assert equivalent("not (p -> q)", "p and not q", V2)
    assert equivalent("(p and q) or (p and not q)", "p", V2)
    assert equivalent("(p -> r) and (q -> r)", "(p or q) -> r", V3)
    assert equivalent("p -> (q -> r)", "(p and q) -> r", V3)
    assert minterms("p xor q xor r", V3) == [1, 2, 4, 7]
    nand = lambda a, b: f"not (({a}) and ({b}))"  # noqa: E731
    assert equivalent(nand("p", "p"), "not p", ["p"])
    assert equivalent(nand(nand("p", "q"), nand("p", "q")), "p and q", V2)
    assert equivalent(nand(nand("p", "p"), nand("q", "q")), "p or q", V2)


# ------------------------------------------------------------------ DM-03
def test_dm03():
    D = [-1, 0, 1, 2]
    assert all(x * x >= x for x in D)
    assert [x for x in D if x * x == 2 * x] == [0, 2]
    assert all((not x > 0) or x * x > 0 for x in D)
    Z = range(-20, 21)
    assert all(any(x + y == 0 for y in Z) for x in Z)                 # ∀x∃y
    assert not any(all(x + y == 0 for x in Z) for y in Z)             # ∃y∀x
    assert not all(any(x * y == 1 for y in Z) for x in Z)             # ∀x∃y xy=1 false
    P, Q = {1}, {2}
    dom = [1, 2]
    lhs = all(x in P or x in Q for x in dom)
    rhs = all(x in P for x in dom) or all(x in Q for x in dom)
    assert lhs and not rhs
    assert all([]) is True and any([]) is False


# ------------------------------------------------------------------ DM-04
def test_dm04():
    assert valid_argument(["b and t -> d", "not d", "b"], "not t", ["b", "t", "d"])
    assert valid_argument(["p -> q", "not q"], "not p", ["p", "q"])
    assert not valid_argument(["p -> q", "not p"], "not q", ["p", "q"])
    assert valid_argument(["p or q", "p -> r", "q -> r"], "r", ["p", "q", "r"])
    assert valid_argument(["p -> q", "r -> s", "p or r", "not q"], "s", ["p", "q", "r", "s"])
    assert valid_argument(["(w and not h) -> o", "not o", "w"], "h", ["w", "h", "o"])
    assert valid_argument(["not p or q", "not q or r", "p"], "r", ["p", "q", "r"])
    assert not valid_argument(["(p and not m) -> c", "m"], "not c", ["p", "m", "c"])
    assert is_contradiction("(p or q) and (not p or r) and (not q or r) and not r", ["p", "q", "r"])


# ------------------------------------------------------------------ DM-05
def test_dm05_numeric_claims():
    N = 2 * 3 * 5 * 7 * 11 * 13 + 1
    assert N == 30031 == 59 * 509
    vals = [n * n + n + 41 for n in range(1, 41)]
    is_p = lambda k: k > 1 and all(k % d for d in range(2, math.isqrt(k) + 1))  # noqa: E731
    assert all(is_p(v) for v in vals[:39]) and vals[39] == 1681 == 41 * 41
    assert all((n * n + n) % 2 == 0 and (n ** 3 - n) % 2 == 0 for n in range(-50, 51))
    assert all((n * n) % 3 != 0 for n in range(-30, 31) if n % 3 != 0)
    assert all((n % 2 == 1) == (n * n % 2 == 1) for n in range(-50, 51))


# ------------------------------------------------------------------ DM-06
def test_dm06():
    U = set(range(1, 11))
    A, B = {1, 2, 3, 4, 5}, {4, 5, 6, 7}
    assert (A | B, A & B, A - B, B - A, A ^ B, U - A) == ({1, 2, 3, 4, 5, 6, 7}, {4, 5}, {1, 2, 3}, {6, 7},
                                                            {1, 2, 3, 6, 7}, {6, 7, 8, 9, 10})
    assert U - (A | B) == (U - A) & (U - B) == {8, 9, 10}
    U8 = set(range(1, 9))
    A, B, C = {1, 2, 3, 4}, {3, 4, 5, 6}, {2, 4, 6, 8}
    assert (A & B & C, (A | B) - C, (U8 - A) & C, A ^ C) == ({4}, {1, 3, 5}, {6, 8}, {1, 3, 6, 8})
    assert len(power_set({1, 2, 3})) == 8 and len(power_set(power_set({0, 1}))) == 16
    assert len(cartesian({0, 1}, "xyz")) == 6 and 2 ** 6 == 64
    # identities hold for random sets
    import random
    rng = random.Random(6)
    for _ in range(200):
        X, Y, Z = ({rng.randint(0, 9) for _ in range(rng.randint(0, 6))} for _ in range(3))
        assert X - (Y | Z) == (X - Y) & (X - Z)
        assert X | (Y & Z) == (X | Y) & (X | Z)
        V = set(range(10))
        assert (V - (X | Y)) | ((V - X) & Y) == V - X
        assert cartesian(X, Y & Z) == cartesian(X, Y) & cartesian(X, Z)
    assert 40 - (25 + 18 - 7) == 4


# ------------------------------------------------------------------ DM-07
def test_dm07():
    assert (math.floor(3.7), math.ceil(3.2), math.floor(-3.7), math.ceil(-3.2), -17 % 5) == (3, 4, -4, -3, 3)
    assert (math.floor(-2.5), math.ceil(-2.5)) == (-3, -2)
    f = {1: "a", 2: "b", 3: "a", 4: "c"}
    assert is_surjective(f, "abc") and not is_injective(f)
    assert count_functions(3, 4) == {"all": 64, "injective": 24, "surjective": 0}
    assert count_functions(4, 4)["surjective"] == 24
    # roots of x^2 + 6x + 3 = 0 satisfy 2x^2+3 == (2x+3)^2
    for x in (-3 + math.sqrt(6), -3 - math.sqrt(6)):
        assert math.isclose(2 * x * x + 3, (2 * x + 3) ** 2)
    # E(x) = 2x mod 26 is not injective; Caesar is
    assert len({(2 * x) % 26 for x in range(26)}) == 13
    assert len({(x + 3) % 26 for x in range(26)}) == 26
    assert sum(map(ord, "ab")) % 16 == sum(map(ord, "ba")) % 16


# ------------------------------------------------------------------ DM-08
def test_dm08():
    from fractions import Fraction as Fr
    assert sum(2 * i + 1 for i in range(1, 6)) == 35
    assert sum(3 * 2 ** k for k in range(5)) == 93
    assert sum(range(10, 21)) == 165
    assert sum(Fr(1, i * (i + 1)) for i in range(1, 5)) == Fr(4, 5)
    assert sum(range(1, 101)) == 5050 and sum(i * i for i in range(1, 11)) == 385
    assert sum(range(1, 98, 3)) == 1617
    for n in range(1, 30):
        assert sum(6 * i * i - 2 * i for i in range(1, n + 1)) == 2 * n * n * (n + 1)
        assert sum(2 * i + 1 for i in range(1, n + 1)) == n * n + 2 * n
        assert sum(1 for i in range(1, n + 1) for j in range(i, n + 1)) == n * (n + 1) // 2
        triple = sum(1 for i in range(n) for j in range(i) for k in range(j))
        assert triple == math.comb(n, 3)
        assert sum(i + j for i in range(1, n + 1) for j in range(1, n + 1)) == n * n * (n + 1)
    total = 50000 * sum(1.01 ** j for j in range(1, 13))
    assert round(total) == 640466
    waits = lambda k, cap=None: sum(min(0.5 * 2 ** i, cap) if cap else 0.5 * 2 ** i for i in range(k))  # noqa: E731
    assert waits(10) == 511.5 and waits(11) == 1023.5
    assert all(waits(k, 30) == 31.5 + 30 * (k - 6) for k in range(6, 20))


# ------------------------------------------------------------------ DM-09
def test_dm09():
    for n in range(0, 60):
        assert sum(2 ** i for i in range(n + 1)) == 2 ** (n + 1) - 1
        assert (n ** 3 + 2 * n) % 3 == 0 and (n ** 3 - n) % 6 == 0
    assert [n for n in range(0, 12) if not 2 ** n > n * n] == [2, 3, 4]
    assert all(2 ** n > n * n for n in range(5, 200))
    assert all(math.factorial(n) > 2 ** n for n in range(4, 100)) and not math.factorial(3) > 8
    reachable = lambda n: any(4 * a + 5 * b == n for a in range(n // 4 + 1) for b in range(n // 5 + 1))  # noqa: E731
    assert all(reachable(n) for n in range(12, 300)) and not reachable(11)
    fib = iterate_recurrence([1, 1], [0, 1], 60)
    assert all(fib[n] < 2 ** n for n in range(61))
    assert all(sum(fib[: n + 1]) == fib[n + 2] - 1 for n in range(58))


# ------------------------------------------------------------------ DM-10
def _closure(rel):
    rel = set(rel)
    while True:
        new = {(a, d) for a, b in rel for c, d in rel if b == c} - rel
        if not new:
            return rel
        rel |= new


def test_dm10():
    A = [1, 2, 3]
    R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1), (2, 3)}
    assert is_reflexive(R, A) and not is_symmetric(R) and not is_antisymmetric(R) and not is_transitive(R)
    D = [1, 2, 3, 4]
    lt = {(a, b) for a in D for b in D if a < b}
    assert not is_reflexive(lt, D) and is_antisymmetric(lt) and is_transitive(lt) and not is_symmetric(lt)
    par = {(a, b) for a in D for b in D if (a + b) % 2 == 0}
    assert is_reflexive(par, D) and is_symmetric(par) and is_transitive(par)
    assert sorted(map(sorted, equivalence_classes(range(11), lambda x, y: x % 3 == y % 3))) == \
        [[0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8]]
    close = {(a, b) for a in range(-3, 4) for b in range(-3, 4) if abs(a - b) <= 1}
    assert not is_transitive(close)
    pos = range(1, 25)
    div = {(a, b) for a in pos for b in pos if b % a == 0}
    assert is_reflexive(div, pos) and is_antisymmetric(div) and is_transitive(div)
    zdiv = {(a, b) for a in range(-4, 5) for b in range(-4, 5) if a != 0 and b % a == 0}
    assert not is_antisymmetric(zdiv)
    clo = _closure({(1, 2), (2, 3), (3, 4), (4, 2)})
    assert len(clo) == 12 and {(2, 2), (3, 3), (4, 4)} <= clo and (1, 1) not in clo
    n = 3
    reflexive_count = sum(1 for mask in range(2 ** (n * n))
                          if all(mask >> (i * n + i) & 1 for i in range(n)))
    assert reflexive_count == 64


# ------------------------------------------------------------------ DM-11
def _room_allocations(students, k):
    if k == 0:
        yield []
        return
    for trio in itertools.combinations(students, 3):
        rest = [s for s in students if s not in trio]
        for r in _room_allocations(rest, k - 1):
            yield [trio] + r


def test_dm11():
    assert 26 ** 3 * 10 ** 5 == 1_757_600_000
    assert sum(1 for b in itertools.product("01", repeat=8) if b[0] == "1" or b[-2:] == ("0", "0")) == 160
    assert (perm(10, 3), comb(10, 3), comb(9, 2), comb(10, 3) - comb(6, 3)) == (720, 120, 36, 100)
    assert multiset_perm([1, 4, 4, 2]) == 34650
    banana = {p for p in itertools.permutations("BANANA")}
    assert len(banana) == 60 and sum(1 for p in banana if "NN" not in "".join(p)) == 40
    assert math.factorial(5) == 120 and 2 * math.factorial(4) == 48
    assert comb(12, 5) - comb(7, 5) - 5 * comb(7, 4) == 596
    assert multiset_perm([3, 2, 1, 1]) == 420 and multiset_perm([2, 2, 1, 1]) == 180
    assert combinations_with_repetition(4, 10) == 286 and combinations_with_repetition(4, 6) == 84
    assert 256 - 1 - 8 - 28 == 219
    total = valid = together = 0
    cs = set(range(6))
    for alloc in _room_allocations(list(range(12)), 4):
        total += 1
        valid += all(0 < len(set(t) & cs) < 3 for t in alloc)
        together += any(0 in t and 1 in t for t in alloc)
    assert (total, valid, together) == (369_600, 194_400, 67_200)
    assert 6 * 180 * 180 == 194_400
    assert combinations_with_repetition(3, 5) == 21 and combinations_with_repetition(3, 4) == 15
    assert multiset_perm([2, 2, 1]) == 30


# ------------------------------------------------------------------ DM-12
def test_dm12():
    assert math.ceil(100 / 12) == 9 and math.ceil(25 / 12) == 3 and math.ceil(24 / 12) == 2
    for chosen in itertools.combinations(range(1, 11), 6):
        assert any(a + b == 11 for a, b in itertools.combinations(chosen, 2))
    assert not any(a + b == 11 for a, b in itertools.combinations(range(1, 6), 2))
    assert 30 + 25 + 20 - 10 - 8 - 6 + 3 == 54
    assert count_divisible(1000, [2, 3, 5]) == 734 and 100 - count_divisible(100, [2, 3, 5, 7]) == 22
    assert sum(2 ** k for k in range(10)) == 2 ** 10 - 1
    assert [derangements(n) for n in range(1, 7)] == [0, 1, 2, 9, 44, 265]
    assert sum(1 for p in itertools.permutations(range(5)) if all(p[i] != i for i in range(5))) == 44
    assert count_functions(5, 3)["surjective"] == 150
    assert 22 + 18 - 7 == 33 and count_divisible(60, [2, 3]) == 40
    # Ramsey R(3,3) = 6: every 2-colouring of K6 has a mono triangle; the pentagon colouring of K5 has none
    edges6 = list(itertools.combinations(range(6), 2))
    for colours in itertools.product([0, 1], repeat=len(edges6)):
        col = dict(zip(edges6, colours))
        assert any(col[(a, b)] == col[(a, c)] == col[(b, c)] for a, b, c in itertools.combinations(range(6), 3))
    pent = {(a, b): int((b - a) % 5 in (1, 4)) for a, b in itertools.combinations(range(5), 2)}
    assert not any(pent[(a, b)] == pent[(a, c)] == pent[(b, c)] for a, b, c in itertools.combinations(range(5), 3))


# ------------------------------------------------------------------ DM-13
def test_dm13():
    C = math.comb
    assert C(8, 3) * 2 ** 5 * (-3) ** 3 == -48384
    assert C(6, 3) * 8 == 160 and C(10, 5) == 252 and C(8, 4) * 16 == 1120
    assert 101 ** 4 == 104060401 and binomial_coefficients(6) == [1, 6, 15, 20, 15, 6, 1]
    assert C(7, 3) * 8 == 280 and C(6, 2) * 2 ** 4 == 240
    assert round(0.99 ** 20, 3) == 0.818 and abs((1 - 0.2 + 0.019 - 0.00114) - 0.99 ** 20) < 1e-4
    for n in range(0, 15):
        assert sum(C(n, k) * 2 ** k for k in range(n + 1)) == 3 ** n
        assert sum(C(n, k) ** 2 for k in range(n + 1)) == C(2 * n, n)
        assert sum(k * C(n, k) for k in range(n + 1)) == (n * 2 ** (n - 1) if n else 0)
    assert round(C(8, 4) / 256, 3) == 0.273


# ------------------------------------------------------------------ DM-14
def test_dm14():
    N = 15
    a = iterate_recurrence([3], [1], N, lambda k: 2)
    assert a == [2 * 3 ** n - 1 for n in range(N + 1)]
    a = iterate_recurrence([5, -6], [1, 4], N)
    assert a == [2 * 3 ** n - 2 ** n for n in range(N + 1)]
    a = iterate_recurrence([4, -4], [1, 6], N)
    assert a == [(1 + 2 * n) * 2 ** n for n in range(N + 1)]
    a = iterate_recurrence([2], [1], N, lambda k: k)
    assert a == [3 * 2 ** n - n - 2 for n in range(N + 1)]
    fib = iterate_recurrence([1, 1], [0, 1], 30)
    phi, psi = (1 + 5 ** 0.5) / 2, (1 - 5 ** 0.5) / 2
    assert all(round((phi ** n - psi ** n) / 5 ** 0.5) == fib[n] for n in range(31))
    no11 = lambda n: sum(1 for b in itertools.product("01", repeat=n) if "11" not in "".join(b))  # noqa: E731
    assert [no11(n) for n in range(1, 11)] == [fib[n + 2] for n in range(1, 11)]
    assert iterate_recurrence([2], [0], 10, lambda k: 1) == [2 ** n - 1 for n in range(11)]
    a = iterate_recurrence([1, 6], [3, 6], N)
    assert all(5 * a[n] == 12 * 3 ** n + 3 * (-2) ** n for n in range(N + 1))
    a = iterate_recurrence([6, -9], [2, 9], N)
    assert a == [(2 + n) * 3 ** n for n in range(N + 1)]
    assert iterate_recurrence([3], [1], N, lambda k: 4) == [3 ** (n + 1) - 2 for n in range(N + 1)]
    assert fib[11] == 89
    bal, month = 2_000_000.0, 0
    while bal > 0:
        bal = bal * 1.01 - 100_000
        month += 1
    assert month == 23 and math.isclose(math.log(1.25) / math.log(1.01), 22.43, abs_tol=0.01)
