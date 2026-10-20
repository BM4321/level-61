---
title: "Python Question Bank"
module: "Python Programming"
module_code: "CST06102"
topic_id: "QB-PY"
type: "question-bank"
tags:
  - semester-6
  - python
  - exam
---

# QB-PY Python Question Bank

> [!info] How to use
> Two questions per lesson, at the level shown (L1 recall … L5 project). Answer closed book, then open the folded answer. **Every printed output below was produced by running the snippet:** `09 - Revision and Exam Preparation/code/tests/test_qb.py` executes each `# question` snippet from this note and checks that its output appears in the answer. Log misses in [[Mistake Log]].

## [[PY-01 How Python Executes Programs and Environment Setup]]

**Q1 (L1).** What's the difference between a syntax error and a runtime error? When is each detected?

> [!success]- Answer
> A syntax error is detected when Python compiles the file to bytecode, before any line runs; nothing executes. A runtime error (exception) happens while the program runs, at the failing line; earlier lines have already executed.

**Q2 (L2).** Why use a virtual environment for each project? Give the commands to create and activate one.

> [!success]- Answer
> It isolates each project's packages and versions, so projects don't break each other and the setup is reproducible. `python -m venv .venv`, then `. .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows); install with `python -m pip install …`.

## [[PY-02 Variables, Types, Expressions and Operators]]

**Q3 (L2).** What does this print? Explain each part.
```python
# question P02
print(7 // 2, -7 // 2, 7 % 3, -7 % 3, 2 ** 3 ** 2, 0.1 + 0.2 == 0.3)
```

> [!success]- Answer
> ```text
> 3 -4 1 2 512 False
> ```
> Floor division rounds towards −∞ (`-7 // 2` is −4) and `%` takes the sign of the divisor (`-7 % 3` is 2); `**` is right-associative (`3 ** 2` first, so 2⁹ = 512); 0.1 + 0.2 isn't exactly 0.3 in binary floating point. Compare floats with `math.isclose`.

**Q4 (L1).** Name the type of each: `3`, `3.0`, `"3"`, `[3]`, `(3,)`, `{3}`, `{"a": 3}`, `None`, `True`.

> [!success]- Answer
> int, float, str, list, tuple, set, dict, NoneType, bool (a subclass of int).

## [[PY-03 Input, Output and String Formatting]]

**Q5 (L1).** What does this print? Explain each part.
```python
# question P03
name, mark = "Asha", 71.456
print(f"{name:>6}|{mark:.1f}|{mark:08.2f}|{1234567:,}")
```

> [!success]- Answer
> ```text
>   Asha|71.5|00071.46|1,234,567
> ```
> `>6` right-aligns in 6 characters; `.1f` rounds to 1 decimal; `08.2f` zero-pads to width 8 with 2 decimals; `,` adds thousands separators.

**Q6 (L2).** Write code that reads a mark with `input`, converts it to a float, and prints "Invalid" instead of crashing on bad input.

> [!success]- Answer
> ```python
> raw = "72.5"   # stands in for input("Mark: ")
> try:
>     mark = float(raw)
>     print(f"Mark: {mark:.1f}")
> except ValueError:
>     print("Invalid")
> ```

## [[PY-04 Conditions and Branching]]

**Q7 (L2).** What does this print? Explain each part.
```python
# question P04
x = 0
print(x or "default", x and "never", not x, 5 if x else 6)
```

> [!success]- Answer
> ```text
> default 0 True 6
> ```
> `or` returns the first truthy operand (or the last); `and` returns the first falsy operand (here 0); `not 0` is True; the conditional expression picks 6 because `x` is falsy.

**Q8 (L3).** Write `classify(t)` returning "cold" below 15, "mild" from 15 up to (not including) 25, "hot" otherwise. Which inputs test the boundaries?

> [!success]- Answer
> ```python
> def classify(t):
>     if t < 15:
>         return "cold"
>     if t < 25:
>         return "mild"
>     return "hot"
> ```
> Boundaries: 14.9, 15, 24.9, 25.

## [[PY-05 Loops and Iteration]]

**Q9 (L2).** What does this print? Explain each part.
```python
# question P05
for i in range(10, 0, -3):
    print(i, end=" ")
print()
print([i * j for i in range(1, 4) for j in range(i)])
```

> [!success]- Answer
> ```text
> 10 7 4 1 
> [0, 0, 2, 0, 3, 6]
> ```
> `range(10, 0, -3)` gives 10, 7, 4, 1; the nested comprehension computes `i * j` for j < i: (1: 0), (2: 0, 2), (3: 0, 3, 6).

**Q10 (L3).** Write a loop that asks for numbers until the user types `done`, then prints the total; ignore lines that aren't numbers.

> [!success]- Answer
> ```python
> lines = ["4", "x", "6.5", "done", "9"]   # stands in for repeated input()
> total = 0.0
> for line in lines:
>     if line == "done":
>         break
>     try:
>         total += float(line)
>     except ValueError:
>         continue
> print(total)   # 10.5
> ```

## [[PY-06 Functions, Parameters, Return Values and Scope]]

**Q11 (L3).** What does this print? Explain each part.
```python
# question P06
count = 0
def bump():
    global count
    count += 1
    return count
def outer():
    n = 0
    def inner():
        nonlocal n
        n += 10
        return n
    inner(); return inner()
print(bump(), bump(), outer())
```

> [!success]- Answer
> ```text
> 1 2 20
> ```
> `global` makes `bump` rebind the module-level `count` (1, then 2); `nonlocal` makes `inner` rebind `outer`'s `n`, so two calls give 10 then 20.

**Q12 (L2).** Why is `def f(items=[])` a bug? Show the fix.

> [!success]- Answer
> The default list is created once, at definition time, and shared across calls. Use `def f(items=None):` and `if items is None: items = []`.

## [[PY-07 Recursion]]

**Q13 (L3).** What does this print? Explain each part.
```python
# question P07
def f(n):
    return 1 if n <= 1 else f(n - 1) + f(n - 2)
calls = 0
def g(n):
    global calls
    calls += 1
    return 1 if n <= 1 else g(n - 1) + g(n - 2)
print(f(10), g(10), calls)
```

> [!success]- Answer
> ```text
> 89 89 177
> ```
> Both compute the Fibonacci-like value 89 for n = 10. Naive recursion makes 177 calls for n = 10, because subproblems are recomputed; the number grows exponentially. Memoise (`functools.lru_cache`) or iterate.

**Q14 (L2).** What are the two parts every recursive function needs, and what happens without the first?

> [!success]- Answer
> A base case that returns without recursing, and a recursive case that moves towards it. Without a reachable base case, recursion continues until `RecursionError`.

## [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing]]

**Q15 (L2).** Make this precise and decompose it: "tell me which rooms keep reporting problems".

> [!success]- Answer
> "Given (room, date) reports, return rooms with ≥ 3 reports in the last 30 days, most first." Steps: filter by date → count per room → keep counts ≥ 3 → sort by count descending. (Implemented as `repeat_rooms` in [[PRJ-PY-05 Hostel Maintenance System]].)

**Q16 (L3).** Trace `x = 5; y = 1; while x > 1: y *= x; x -= 2` and give the final values.

> [!success]- Answer
> x: 5 → 3 → 1; y: 1 → 5 → 15. Final x = 1, y = 15.

## [[PY-09 Strings and String Processing]]

**Q17 (L2).** What does this print? Explain each part.
```python
# question P09
s = "Hostel Block-A, Room 101"
print(s.lower().split(), s[::-1][:5], s.replace(" ", "").count("o"), "-".join(s.split(", ")))
```

> [!success]- Answer
> ```text
> ['hostel', 'block-a,', 'room', '101'] 101 m 4 Hostel Block-A-Room 101
> ```
> `split()` splits on whitespace (the comma stays attached); `[::-1][:5]` takes the last 5 characters reversed; removing spaces leaves 4 lowercase `o`s; `join` replaces ", " with "-".

**Q18 (L3).** Write `is_valid_room(code)` that accepts codes like `A-101` (one capital letter, a hyphen, three digits) and rejects everything else.

> [!success]- Answer
> ```python
> import re
>
>
> def is_valid_room(code):
>     return re.fullmatch(r"[A-Z]-\d{3}", code) is not None
>
>
> print(is_valid_room("A-101"), is_valid_room("a-101"), is_valid_room("A-1012"))   # True False False
> ```

## [[PY-10 Lists and Tuples]]

**Q19 (L3).** What does this print? Explain each part.
```python
# question P10
a = [1, 2, 3]
b = a
c = a[:]
b.append(4)
t = (1, [2, 3])
t[1].append(4)
print(a, c, t, a is b, a == c)
```

> [!success]- Answer
> ```text
> [1, 2, 3, 4] [1, 2, 3] (1, [2, 3, 4]) True False
> ```
> `b = a` makes an alias (same list); `a[:]` makes a shallow copy; a tuple can't be rebound, but a list inside it can be mutated. `is` tests identity, `==` equality.

**Q20 (L2).** When should you use a tuple rather than a list?

> [!success]- Answer
> For fixed-size records whose positions have meaning (coordinates, (room, category) keys), or when you need a hashable value for a dict key or set member.

## [[PY-11 Dictionaries, Sets and Comprehensions]]

**Q21 (L2).** What does this print? Explain each part.
```python
# question P11
marks = {"S1": 71, "S2": 48, "S3": 64, "S4": 39}
passed = {s for s, m in marks.items() if m >= 40}
print(sorted(passed), {s: m for s, m in marks.items() if m < 50}, max(marks, key=marks.get))
```

> [!success]- Answer
> ```text
> ['S1', 'S2', 'S3'] {'S2': 48, 'S4': 39} S1
> ```
> The set comprehension keeps marks ≥ 40; the dict comprehension keeps marks < 50; `max(marks, key=marks.get)` returns the key with the highest value.

**Q22 (L3).** Count how many reports each category has in `["plumbing", "electrical", "plumbing"]` two ways.

> [!success]- Answer
> `counts = {}` with `counts[c] = counts.get(c, 0) + 1`; or `collections.Counter(cats)`. Both give `{'plumbing': 2, 'electrical': 1}`.

## [[PY-12 Searching, Sorting and Complexity]]

**Q23 (L2).** What does this print? Explain each part.
```python
# question P12
data = [("b", 3), ("a", 3), ("c", 1)]
print(sorted(data, key=lambda t: (-t[1], t[0])), sorted("banana"), min(data, key=lambda t: t[1]))
```

> [!success]- Answer
> ```text
> [('a', 3), ('b', 3), ('c', 1)] ['a', 'a', 'a', 'b', 'n', 'n'] ('c', 1)
> ```
> The key sorts by count descending, then name ascending; `sorted` on a string returns a list of characters; `min` with a key compares the counts.

**Q24 (L3).** Binary search on 1,000,000 sorted items: at most how many comparisons? Linear search?

> [!success]- Answer
> About ⌈log₂ 1,000,000⌉ = 20 comparisons; linear search up to 1,000,000.

## [[PY-13 Modules, Packages, Imports and Virtual Environments]]

**Q25 (L2).** What does `if __name__ == "__main__":` do?

> [!success]- Answer
> Code under it runs only when the file is executed as a script, not when it's imported as a module, so a module can be both imported and run.

**Q26 (L3).** A test file fails with `ModuleNotFoundError: No module named 'hostel'`. Give two fixes.

> [!success]- Answer
> Run from the project root with the package importable: install it in editable mode (`pip install -e .`), or configure the test runner's path (e.g. `pythonpath = src` in `pytest.ini`). Don't edit `sys.path` inside application code.

## [[PY-14 Files, CSV and JSON]]

**Q27 (L2).** Why use `with open(...) as f:`?

> [!success]- Answer
> The file is closed automatically when the block ends, even if an exception occurs.

**Q28 (L3).** Write a function that reads a CSV with header `room,category` and returns a list of dicts, using the `csv` module.

> [!success]- Answer
> ```python
> import csv
> import io
>
>
> def read_reports(fh):
>     return list(csv.DictReader(fh))
>
>
> print(read_reports(io.StringIO("room,category\nA-101,plumbing\n")))   # [{'room': 'A-101', 'category': 'plumbing'}]
> ```

## [[PY-15 Exceptions and Defensive Programming]]

**Q29 (L3).** What does this print? Explain each part.
```python
# question P15
def parse(s):
    try:
        return int(s)
    except ValueError as e:
        raise ValueError(f"bad number: {s!r}") from e
try:
    parse("4x")
except ValueError as e:
    print(e, type(e.__cause__).__name__)
```

> [!success]- Answer
> ```text
> bad number: '4x' ValueError
> ```
> `raise … from e` chains the original exception as `__cause__`, so the traceback shows both: your message adds context without hiding the root cause.

**Q30 (L2).** Why is `except Exception: pass` dangerous?

> [!success]- Answer
> It silently hides every error, including bugs, so failures surface later, far from the cause. Catch the specific exceptions you can handle, and log or re-raise the rest.

## [[PY-16 Classes and Objects]]

**Q31 (L3).** What does this print? Explain each part.
```python
# question P16
class Counter:
    total = 0
    def __init__(self):
        self.n = 0
    def click(self):
        self.n += 1
        Counter.total += 1
        return self
a, b = Counter(), Counter()
a.click().click(); b.click()
print(a.n, b.n, Counter.total)
```

> [!success]- Answer
> ```text
> 2 1 3
> ```
> `n` is an instance attribute (separate per object: 2 and 1); `total` is a class attribute shared by all instances (3). Returning `self` allows chaining.

**Q32 (L2).** What's an invariant? Give one for a `BankAccount`, and say where it's enforced.

> [!success]- Answer
> A condition that must always hold for a valid object, e.g. balance ≥ 0 (if overdrafts aren't allowed). Enforce it in `__init__` and in every method that changes the balance (raise an exception rather than breaking it).

## [[PY-17 Inheritance, Composition and Polymorphism]]

**Q33 (L3).** What does this print? Explain each part.
```python
# question P17
class Shape:
    def area(self):
        raise NotImplementedError
    def describe(self):
        return f"{type(self).__name__} with area {self.area():.1f}"
class Rect(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
class Square(Rect):
    def __init__(self, s): super().__init__(s, s)
print([s.describe() for s in (Rect(2, 3.5), Square(3))], Square.__mro__[1].__name__)
```

> [!success]- Answer
> ```text
> ['Rect with area 7.0', 'Square with area 9.0'] Rect
> ```
> Polymorphism: `describe` calls the subclass's `area`. `Square` reuses `Rect` via `super().__init__`; its MRO is Square → Rect → Shape → object.

**Q34 (L2).** When is composition better than inheritance?

> [!success]- Answer
> When the relationship is "has-a" or "uses-a", or when behaviour varies by configuration: e.g. a service *has* a repository rather than *being* one. Inheritance couples the subclass to the parent's implementation.

## [[PY-18 Iterators, Generators, Decorators and Context Managers]]

**Q35 (L3).** What does this print? Explain each part.
```python
# question P18
def evens(limit):
    n = 0
    while n < limit:
        yield n
        n += 2
gen = evens(7)
print(next(gen), list(gen), list(gen))
def shout(fn):
    def wrapper(*a):
        return fn(*a).upper()
    return wrapper
@shout
def greet(name):
    return f"hi {name}"
print(greet("amina"))
```

> [!success]- Answer
> ```text
> 0 [2, 4, 6] []
> HI AMINA
> ```
> A generator is lazy and single-use: after `next` returns 0, `list(gen)` consumes 2, 4, 6, and a second `list` is empty. The decorator wraps `greet` and upper-cases its result.

**Q36 (L2).** Why might a generator be better than a list for processing a 2 GB log file?

> [!success]- Answer
> It yields one item at a time, so memory use stays constant, instead of loading the whole file into a list.

## [[PY-19 Type Hints, Documentation, Clean Code and Refactoring]]

**Q37 (L2).** Do type hints change how Python runs your code? What checks them?

> [!success]- Answer
> No: they're not enforced at runtime. Static checkers such as mypy check them, and editors use them.

**Q38 (L3).** Name three refactorings for a 60-line function with nested ifs and magic numbers.

> [!success]- Answer
> Extract functions with descriptive names; replace magic numbers with named constants; use guard clauses (early returns) to flatten nesting; replace a type switch with a dictionary or polymorphism.

## [[PY-20 Testing, Debugging and Test-Driven Development]]

**Q39 (L2).** Describe the TDD cycle.

> [!success]- Answer
> Red: write a failing test for the next small behaviour. Green: write the simplest code that passes. Refactor: improve the code with the tests still passing. Repeat.

**Q40 (L3).** How do you test code that depends on the current time?

> [!success]- Answer
> Inject a clock (a function or object returning the time) and pass a fake in tests, as [[PRJ-PY-05 Hostel Maintenance System]] does for the reopen window and throttling.

## [[PY-21 Data Structures and Algorithm Design]]

**Q41 (L3).** What does this print? Explain each part.
```python
# question P21
from collections import deque
import heapq
q = deque([1, 2, 3]); q.appendleft(0); q.pop()
h = [5, 1, 4]; heapq.heapify(h); heapq.heappush(h, 2)
print(list(q), [heapq.heappop(h) for _ in range(len(h))])
```

> [!success]- Answer
> ```text
> [0, 1, 2] [1, 2, 4, 5]
> ```
> `deque` supports O(1) appends and pops at both ends; `heapq` keeps the smallest item at index 0, so repeated `heappop` returns items in ascending order.

**Q42 (L2).** Which structure for: (a) a FIFO queue; (b) membership tests on 1 million IDs; (c) always taking the most urgent job?

> [!success]- Answer
> (a) `collections.deque`; (b) `set`; (c) a heap (`heapq`) of (priority, time, item) tuples.

## [[PY-22 SQL and Database Integration]]

**Q43 (L3).** What does this print? Explain each part.
```python
# question P22
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE r (room TEXT, cat TEXT)")
db.executemany("INSERT INTO r VALUES (?, ?)", [("A-101", "plumbing"), ("A-101", "electrical"), ("B-204", "plumbing")])
print(db.execute("SELECT room, COUNT(*) FROM r GROUP BY room ORDER BY COUNT(*) DESC, room").fetchall())
print(db.execute("SELECT COUNT(*) FROM r WHERE cat = ?", ("plumbing",)).fetchone())
```

> [!success]- Answer
> ```text
> [('A-101', 2), ('B-204', 1)]
> (2,)
> ```
> `GROUP BY` counts per room, ordered by the count; the `?` placeholder passes `"plumbing"` as a parameter, never as part of the SQL text.

**Q44 (L2).** Why must a status update and its history row be in one transaction?

> [!success]- Answer
> So either both happen or neither does: otherwise a crash between them leaves the audit trail disagreeing with the data.

## [[PY-23 HTTP APIs and External Services]]

**Q45 (L2).** Name four things robust API client code must handle.

> [!success]- Answer
> Timeouts; HTTP error statuses (check them, e.g. `raise_for_status`); invalid or unexpected JSON; retries with backoff for transient failures (and rate limits); plus keeping API keys out of the code (environment variables).

**Q46 (L3).** How can you test an API client without calling the real service?

> [!success]- Answer
> Inject the HTTP function or session and pass a fake that returns canned responses (including error cases), or use recorded responses.

## [[PY-24 Secure Programming and Input Validation]]

**Q47 (L2).** Allowlist or blocklist validation: which, and why?

> [!success]- Answer
> Allowlist: define exactly what's valid (e.g. `[A-Z]-\d{3}` for room codes) and reject everything else; blocklists miss variants.

**Q48 (L3).** Which standard-library modules for: (a) password hashing; (b) a password-reset token; (c) comparing two MACs?

> [!success]- Answer
> (a) `hashlib.scrypt` (or `pbkdf2_hmac`); (b) `secrets.token_urlsafe`; (c) `hmac.compare_digest` (constant-time).

## [[PY-25 Performance, Packaging and Project Organization]]

**Q49 (L2).** What should you do before optimising code?

> [!success]- Answer
> Measure: profile (`cProfile`, `timeit`) to find where the time actually goes, then optimise that, and re-measure.

**Q50 (L3).** What does `[project.scripts] hostel = "hostel.cli:main"` in `pyproject.toml` do?

> [!success]- Answer
> Installing the package creates a `hostel` command that calls `main()` in `hostel/cli.py`.

Back to [[Question Bank Index]] · [[MOCK-PY-01 Python Programming Mock Examination]] · [[PY 00 Dashboard]]
