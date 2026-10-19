import random

import pytest

from _target import load

m = load("py16")


def test_bank_account():
    a = m.BankAccount("Amina", 10_000)
    a.deposit(2_500)
    a.withdraw(500)
    assert a.balance == 12_000
    assert a.history() == [("deposit", 2500), ("withdraw", 500)]
    a.history().clear()
    assert len(a.history()) == 2           # copy returned
    assert repr(a) == "BankAccount(owner='Amina', balance=12000)"
    with pytest.raises(AttributeError):
        a.balance = 0
    for bad in (0, -5):
        with pytest.raises(ValueError):
            a.deposit(bad)
    with pytest.raises(ValueError):
        a.withdraw(1_000_000)
    with pytest.raises(ValueError):
        m.BankAccount("  ")


def test_transfer():
    a, b = m.BankAccount("A", 100), m.BankAccount("B")
    a.transfer_to(b, 40)
    assert (a.balance, b.balance) == (60, 40)
    with pytest.raises(ValueError):
        a.transfer_to(b, 1000)
    assert (a.balance, b.balance) == (60, 40)


def test_rectangle():
    r = m.Rectangle(3, 4)
    assert (r.area, r.perimeter) == (12, 14)
    assert m.Rectangle.square(5).area == 25
    with pytest.raises(ValueError):
        m.Rectangle(0, 2)


def test_fraction():
    F = m.Fraction
    assert F(1, 2) + F(1, 3) == F(5, 6)
    assert F(2, 4) == F(1, 2) and F(1, -2) == F(-1, 2)
    assert F(1, -2).denominator == 2 and F(1, -2).numerator == -1
    assert 1 + F(1, 2) == F(3, 2) and F(1, 2) + 1 == F(3, 2)
    assert F(3, 4) - F(1, 4) == F(1, 2)
    assert F(2, 3) * F(3, 4) == F(1, 2)
    assert sorted([F(2, 3), F(1, 2), F(-1, 5)]) == [F(-1, 5), F(1, 2), F(2, 3)]
    assert len({F(1, 2), F(3, 6)}) == 1
    assert str(F(6, 3)) == "2" and str(F(5, 6)) == "5/6"
    with pytest.raises(ZeroDivisionError):
        F(1, 0)
    with pytest.raises(TypeError):
        F(1, 2) + "x"


def test_student():
    s = m.Student("S1", "Amina", (70, 80))
    assert s.average == 75 and s.grade == "A"
    assert m.Student("S2", "Bo").grade == "F"
    with pytest.raises(ValueError):
        m.Student("X1", "Bad")
    with pytest.raises(Exception):
        s.name = "changed"   # frozen


def test_inventory():
    inv = m.Inventory()
    inv.add("pen", 10)
    inv.add("pad", 2)
    inv.add("pen", 5)
    inv.remove("pad", 2)
    assert inv.quantity("pen") == 15 and inv.quantity("pad") == 0 and len(inv) == 1
    inv.add("ink", 1)
    assert inv.low_stock(3) == ["ink"]
    with pytest.raises(ValueError):
        inv.remove("pen", 99)
    with pytest.raises(ValueError):
        inv.add("x", 0)


def test_money():
    M = m.Money
    assert M(100, "TZS") + M(50, "TZS") == M(150, "TZS")
    assert M(100, "TZS") - M(150, "TZS") == M(-50, "TZS")
    assert M(1, "TZS") < M(2, "TZS")
    with pytest.raises(ValueError):
        M(1, "TZS") + M(1, "USD")
    assert [x.minor for x in M(100, "TZS").allocate([1, 1, 1])] == [34, 33, 33]


def test_money_allocate_sums_exactly():
    rng = random.Random(16)
    for _ in range(300):
        amount = rng.randint(0, 10_000)
        ratios = [rng.randint(0, 5) for _ in range(rng.randint(1, 6))]
        if sum(ratios) == 0:
            continue
        parts = m.Money(amount, "TZS").allocate(ratios)
        assert sum(p.minor for p in parts) == amount
