"""PY-10: aliasing, copies and traps. Run: python examples/py10_lists.py"""
import copy

a = [1, 2, 3]
b = a
c = a[:]
a.append(4)
print("alias b:", b, "| copy c:", c)

grid = [[0, 0], [0, 0]]
shallow = grid.copy()
deep = copy.deepcopy(grid)
shallow[0][0] = 9
print("grid after shallow edit:", grid, "| deep copy:", deep)

board = [[0] * 3] * 3
board[0][0] = "X"
print("multiplication trap:", board)

xs = [1, 2, 2, 3]
for x in xs:
    if x == 2:
        xs.remove(x)
print("remove-while-iterating:", xs)

students = [("Ali", 71), ("Bea", 88), ("Chen", 71)]
print(sorted(students, key=lambda s: (-s[1], s[0])))
first, *rest = [1, 2, 3, 4]
print(first, rest)
