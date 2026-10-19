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
