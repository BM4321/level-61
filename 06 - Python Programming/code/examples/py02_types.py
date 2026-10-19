"""PY-02: types, operators and conversions. Run: python examples/py02_types.py"""
import math
from decimal import Decimal

print("type(7/7) =", type(7 / 7).__name__, "| 7//7 =", 7 // 7)
print("-7 // 2 =", -7 // 2, "| -7 % 2 =", -7 % 2, "| int(-7/2) =", int(-7 / 2))
print("2**3**2 =", 2 ** 3 ** 2, "| -2**2 =", -2 ** 2)
print("0.1 + 0.2 =", 0.1 + 0.2, "| isclose:", math.isclose(0.1 + 0.2, 0.3))
print("Decimal exact:", Decimal("0.1") + Decimal("0.2"))
print("round(2.5), round(3.5) =", round(2.5), round(3.5))

a = [1, 2]
b = a
b.append(3)
print("aliasing: a =", a, "| a is b:", a is b)

total = 7384
hours, rest = divmod(total, 3600)
minutes, seconds = divmod(rest, 60)
print(f"{total}s = {hours}h {minutes}m {seconds}s")
