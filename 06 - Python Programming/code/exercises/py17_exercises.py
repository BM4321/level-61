"""PY17 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py17.py
"""

from __future__ import annotations
import math
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract shape interface. [given]"""

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        return f'{type(self).__name__}: area={self.area():.2f}'

class Circle(Shape):

    def __init__(self, r: float):
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

class Rectangle(Shape):

    def __init__(self, w: float, h: float):
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

class Triangle(Shape):

    def __init__(self, a: float, b: float, c: float):
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

class Square(Shape):
    """Sibling of Rectangle (not a subclass) to respect LSP."""

    def __init__(self, side: float):
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

def total_area(shapes: list[Shape]) -> float:
    """Sum of areas (polymorphic)."""
    raise NotImplementedError

def largest(shapes: list[Shape]) -> Shape:
    """Shape with the largest area; ValueError if empty."""
    raise NotImplementedError

class Employee(ABC):
    """Abstract employee. [given]"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def monthly_pay(self) -> int:
        ...

class Salaried(Employee):

    def __init__(self, name: str, annual: int):
        raise NotImplementedError

    def monthly_pay(self) -> int:
        raise NotImplementedError

class Hourly(Employee):

    def __init__(self, name: str, rate: int, hours: float):
        raise NotImplementedError

    def monthly_pay(self) -> int:
        """Hours above 160 are paid at 1.5x."""
        raise NotImplementedError

class Commissioned(Employee):

    def __init__(self, name: str, base: int, rate: float, sales: int):
        raise NotImplementedError

    def monthly_pay(self) -> int:
        raise NotImplementedError

def payroll_total(staff: list[Employee]) -> int:
    raise NotImplementedError

class Stack:
    """LIFO stack implemented by composition over a list."""

    def __init__(self):
        raise NotImplementedError

    def push(self, x) -> None:
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def peek(self):
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

class FakeSender:
    """Test double that records messages instead of sending them. [given]"""

    def __init__(self):
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, msg: str) -> None:
        self.sent.append((to, msg))

class OrderService:
    """Places orders and notifies via injected senders (composition)."""

    def __init__(self, notifiers: list):
        raise NotImplementedError

    def place(self, customer: str, item: str) -> None:
        raise NotImplementedError
