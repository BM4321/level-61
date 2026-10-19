"""PY-17 reference solutions (inheritance, composition, polymorphism)."""
from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract shape interface. [given]"""

    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:
        return f"{type(self).__name__}: area={self.area():.2f}"


class Circle(Shape):
    def __init__(self, r: float):
        if r <= 0:
            raise ValueError("radius must be positive")
        self.r = r

    def area(self) -> float:
        return math.pi * self.r ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.r


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        if w <= 0 or h <= 0:
            raise ValueError("sides must be positive")
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h

    def perimeter(self) -> float:
        return 2 * (self.w + self.h)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        if min(a, b, c) <= 0 or a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("invalid triangle")
        self.a, self.b, self.c = a, b, c

    def perimeter(self) -> float:
        return self.a + self.b + self.c

    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))


class Square(Shape):
    """Sibling of Rectangle (not a subclass) to respect LSP."""

    def __init__(self, side: float):
        if side <= 0:
            raise ValueError("side must be positive")
        self.side = side

    def area(self) -> float:
        return self.side ** 2

    def perimeter(self) -> float:
        return 4 * self.side


def total_area(shapes: list[Shape]) -> float:
    """Sum of areas (polymorphic)."""
    return sum(s.area() for s in shapes)


def largest(shapes: list[Shape]) -> Shape:
    """Shape with the largest area; ValueError if empty."""
    if not shapes:
        raise ValueError("no shapes")
    return max(shapes, key=lambda s: s.area())


class Employee(ABC):
    """Abstract employee. [given]"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def monthly_pay(self) -> int: ...


class Salaried(Employee):
    def __init__(self, name: str, annual: int):
        super().__init__(name)
        self.annual = annual

    def monthly_pay(self) -> int:
        return self.annual // 12


class Hourly(Employee):
    def __init__(self, name: str, rate: int, hours: float):
        super().__init__(name)
        self.rate, self.hours = rate, hours

    def monthly_pay(self) -> int:
        """Hours above 160 are paid at 1.5x."""
        overtime = max(0, self.hours - 160)
        return round(self.rate * (self.hours - overtime) + self.rate * 1.5 * overtime)


class Commissioned(Employee):
    def __init__(self, name: str, base: int, rate: float, sales: int):
        super().__init__(name)
        self.base, self.rate, self.sales = base, rate, sales

    def monthly_pay(self) -> int:
        return round(self.base + self.rate * self.sales)


def payroll_total(staff: list[Employee]) -> int:
    return sum(e.monthly_pay() for e in staff)


class Stack:
    """LIFO stack implemented by composition over a list."""

    def __init__(self):
        self._items: list = []

    def push(self, x) -> None:
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


class FakeSender:
    """Test double that records messages instead of sending them. [given]"""

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, msg: str) -> None:
        self.sent.append((to, msg))


class OrderService:
    """Places orders and notifies via injected senders (composition)."""

    def __init__(self, notifiers: list):
        self.notifiers = notifiers
        self.orders: list[tuple[str, str]] = []

    def place(self, customer: str, item: str) -> None:
        self.orders.append((customer, item))
        for n in self.notifiers:
            n.send(customer, f"Order placed: {item}")
