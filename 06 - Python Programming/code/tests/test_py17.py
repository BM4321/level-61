import math

import pytest

from _target import load

m = load("py17")


def test_shapes():
    assert math.isclose(m.Circle(1).area(), math.pi)
    assert m.Rectangle(3, 4).perimeter() == 14
    assert math.isclose(m.Triangle(3, 4, 5).area(), 6.0)
    assert m.Square(3).area() == 9
    with pytest.raises(ValueError):
        m.Triangle(1, 2, 3)
    with pytest.raises(TypeError):
        m.Shape()
    assert m.Rectangle(2, 3).describe() == "Rectangle: area=6.00"


def test_polymorphic_helpers():
    shapes = [m.Rectangle(2, 3), m.Square(3), m.Triangle(3, 4, 5)]
    assert math.isclose(m.total_area(shapes), 6 + 9 + 6)
    assert isinstance(m.largest(shapes), m.Square)
    assert not issubclass(m.Square, m.Rectangle)
    with pytest.raises(ValueError):
        m.largest([])


def test_payroll():
    staff = [m.Salaried("Amina", 12_000_000), m.Hourly("Juma", 5_000, 170),
             m.Commissioned("Neema", 300_000, 0.05, 2_000_000)]
    assert [e.monthly_pay() for e in staff] == [1_000_000, 875_000, 400_000]
    assert m.payroll_total(staff) == 2_275_000
    assert m.Hourly("x", 1000, 100).monthly_pay() == 100_000


def test_stack():
    s = m.Stack()
    assert s.is_empty() and len(s) == 0
    s.push(1)
    s.push(2)
    assert s.peek() == 2 and len(s) == 2
    assert s.pop() == 2 and s.pop() == 1
    with pytest.raises(IndexError):
        s.pop()
    assert not hasattr(s, "insert")


def test_order_service_with_fake():
    fake = m.FakeSender()
    svc = m.OrderService([fake])
    svc.place("amina@example.com", "Python book")
    assert fake.sent == [("amina@example.com", "Order placed: Python book")]
