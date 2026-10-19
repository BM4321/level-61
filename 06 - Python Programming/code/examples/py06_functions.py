"""PY-06: argument passing, mutable defaults, closures. Run: python examples/py06_functions.py"""


def rebind(n):
    n = n + 1


def mutate(items):
    items.append(99)


a, b = 1, [1]
rebind(a)
mutate(b)
print("after calls:", a, b)


def add_item_wrong(item, basket=[]):  # deliberate bug: shared default
    basket.append(item)
    return basket


print(add_item_wrong("pen"))   # ['pen']
print(add_item_wrong("book"))  # ['pen', 'book']  <- shared default list


def make_multiplier(k):
    def multiply(x):
        return x * k
    return multiply


triple = make_multiplier(3)
print("triple(10) =", triple(10))
print("sorted by key:", sorted(["bea", "Ali", "chen"], key=str.lower))
