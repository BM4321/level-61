"""PY-05: loop patterns. Run: python examples/py05_loops.py"""

# accumulator
total = 0
for i in range(1, 5):
    total += i
    print(f"i={i} total={total}")

# early-exit search with loop-else
for n in [3, 7, 11]:
    if n % 2 == 0:
        print("found even", n)
        break
else:
    print("no even number found")

# enumerate and zip
for rank, (name, mark) in enumerate(zip(["Ali", "Bea", "Chen"], [71, 64, 88]), start=1):
    print(rank, name, mark)

# nested loop: iteration count
count = 0
for i in range(4):
    for j in range(i):
        count += 1
print("triangular nested loop iterations for n=4:", count, "= n(n-1)/2 =", 4 * 3 // 2)
