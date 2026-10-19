"""PY-17: polymorphism, composition and an LSP violation. Run: python examples/py17_oop.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py17_solutions import Circle, Rectangle, Square, Triangle, total_area  # noqa: E402

shapes = [Circle(1), Rectangle(2, 3), Square(2), Triangle(3, 4, 5)]
for s in shapes:
    print(s.describe())
print("total:", round(total_area(shapes), 3))


class MutableRect:
    def __init__(self, w, h):
        self.w, self.h = w, h

    def set_width(self, w):
        self.w = w

    def area(self):
        return self.w * self.h


class MutableSquare(MutableRect):  # deliberately violates LSP
    def __init__(self, side):
        super().__init__(side, side)

    def set_width(self, w):
        self.w = self.h = w


for r in (MutableRect(5, 5), MutableSquare(5)):
    old_h = r.h
    r.set_width(10)
    print(type(r).__name__, "area", r.area(), "expected", 10 * old_h, "OK" if r.area() == 10 * old_h else "LSP BROKEN")
print("MRO of MutableSquare:", [c.__name__ for c in MutableSquare.__mro__])
