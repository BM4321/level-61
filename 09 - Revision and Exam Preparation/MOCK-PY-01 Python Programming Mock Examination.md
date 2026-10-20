---
title: "Python Programming Mock Examination"
module: "Python Programming"
module_code: "CST06102"
topic_id: "MOCK-PY-01"
type: "exam"
syllabus_status: "supplementary"
status: "not-started"
tags:
  - semester-6
  - python
  - exam
---

# MOCK-PY-01 Python Programming Mock Examination

> [!warning] A designed practice paper
> This is **not** a past paper, and its format (2.5 hours, 100 marks, three sections) is designed, not official. Check your real exam format with your lecturer. Every output and model solution below was produced by running the code: `09 - Revision and Exam Preparation/code/tests/test_mock_py.py` executes the Section A snippets from this note and tests the model solutions in `mock_solutions.py`.

**Instructions (designed):** 2 hours 30 minutes. Answer **all** of Section A, **all** of Section B and **both** questions in Section C. Write code in Python 3.10 or later. Show your working for tracing questions. Time guide: about 1.4 minutes per mark ([[Exam Technique and Assessment Strategy]]).

**Covers:** [[PY 01 Curriculum Map]] units U1–U7.

---

## Section A: reading code (30 marks)

**A1 (5 marks).** What does this print?
```python
# question A1
nums = [3, 8, 1, 9, 4, 7]
print(nums[1:5:2], nums[::-2], [n * n for n in nums if n % 2 == 0])
```

**A2 (5 marks).** What does this print? Explain the `else` clause.
```python
# question A2
for n in [4, 6, 9, 10]:
    if n % 3 == 0:
        print("found", n)
        break
else:
    print("none")
total = 0
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    total += i
print(total)
```

**A3 (5 marks).** What does this print, and why is it a bug? Rewrite the function correctly.
```python
# question A3
def add_item(item, basket=[]):
    basket.append(item)
    return basket
print(add_item("pen"), add_item("book"))
```

**A4 (5 marks).** What does this print?
```python
# question A4
text = "to be or not to be"
counts = {}
for w in text.split():
    counts[w] = counts.get(w, 0) + 1
print(counts, sorted(set(text.split())))
```

**A5 (5 marks).** What does this print? State the order in which `try`, `except`, `else` and `finally` run.
```python
# question A5
def f(x):
    try:
        print("try")
        r = 10 / x
    except ZeroDivisionError:
        print("except")
        return -1
    else:
        print("else")
        return r
    finally:
        print("finally")
print(f(2)); print(f(0))
```

**A6 (5 marks).** Give the worst-case time complexity of each, in terms of $n$ = `len(xs)`, with a one-line reason:
(a) `x in xs` for a list; (b) `x in set(xs)` including building the set; (c) `sorted(xs)`; (d) a loop over `xs` that calls `xs.index(v)` for each `v`; (e) `xs[len(xs) // 2]`.

---

## Section B: writing code (40 marks)

**B1 (10 marks).** Write `grade(mark)` returning a letter using this **designed** scheme: A 70–100, B 60–69, C 50–59, D 40–49, F 0–39. Raise `TypeError` for non-numbers (including `bool`) and `ValueError` for marks outside 0–100. Then write four pytest tests that check the boundaries.

**B2 (15 marks).** Write `course_averages(lines)`. `lines` is a list of strings from a CSV file, the first being the header `student,course,mark`. Return a tuple `(averages, skipped)`: a dictionary from course code to the average mark rounded to 1 decimal place, and the number of lines skipped because they were malformed (wrong number of fields, an empty student or course, a non-numeric mark, or a mark outside 0–100). For example:
```text
student,course,mark
S1,CST06102,71
S2,CST06102,64.5
S3,GST06106,abc
S4,GST06106,58
S5,CST06102
S6,GST06106,105
S7,GST06106,49
```
should give `({"CST06102": 67.8, "GST06106": 53.5}, 3)`.

**B3 (15 marks).** Write a class `Stock` with `add(sku, qty)`, `remove(sku, qty)`, `quantity(sku)` and `__len__` (the number of SKUs with a positive quantity). Quantities must be positive. `remove` must raise a custom exception `InsufficientStock` carrying `sku`, `wanted` and `available` when there isn't enough stock, **and must not change the stock in that case**.

---

## Section C: design, debugging and algorithms (30 marks)

**C1 (15 marks).** The function below works, but a reviewer rejected it. (a) Identify three problems. (b) Refactor it into two functions with named constants. (c) Write tests that would have caught the negative-days bug.
```python
# question C1
def fee(d, l):
    if l == True:
        return 25000
    if d > 20:
        return 10000
    return d * 500
```

**C2 (15 marks).** (a) Write `first_index(items, target)` returning the index of the **first** occurrence of `target` in a sorted list, or −1, in $O(\log n)$ time. (b) Give five test cases, including the edge cases. (c) Explain why a linear scan is $O(n)$ and why your solution is $O(\log n)$.

---

## Marking guide

> [!success]- Section A answers
> **A1** `[8, 9] [7, 9, 8] [64, 16]`. Slice `1:5:2` takes indices 1 and 3; `::-2` takes indices 5, 3, 1; the comprehension squares the even numbers (8, 4). *(2 marks for the slices, 1 for the comprehension, 2 for exact formatting/order.)*
>
> **A2** Prints `found 6` then `12`. The loop's `else` runs only if the loop finishes **without** `break`; here 6 triggers `break`, so `none` isn't printed. The `while` adds 1, 2, 4, 5 (skipping 3) = 12. *(2 for the `for`/`else`, 3 for the total with reasoning.)*
>
> **A3** Prints `['pen', 'book'] ['pen', 'book']`. The default list is created **once**, when the function is defined, and shared between calls; both calls return the same list object, which is printed after both appends. Fix: `def add_item(item, basket=None):` then `if basket is None: basket = []`. *(2 output, 2 explanation, 1 fix.)*
>
> **A4** `{'to': 2, 'be': 2, 'or': 1, 'not': 1} ['be', 'not', 'or', 'to']`. Dictionaries keep insertion order; `sorted` orders the set alphabetically. *(3 + 2.)*
>
> **A5** Prints:
> ```text
> try
> else
> finally
> 5.0
> try
> except
> finally
> -1
> ```
> `finally` runs before the function actually returns, whichever branch returns. *(1 per correct line group, 1 for the explanation.)*
>
> **A6** (a) $O(n)$, linear scan. (b) $O(n)$ to build the set, then $O(1)$ average lookup: $O(n)$ overall. (c) $O(n \log n)$. (d) $O(n^2)$: $n$ calls, each $O(n)$. (e) $O(1)$, indexing. *(1 each.)*

> [!success]- B1 model solution (10)
> ```python
> BANDS = [(70, "A"), (60, "B"), (50, "C"), (40, "D"), (0, "F")]
>
>
> def grade(mark):
>     if isinstance(mark, bool) or not isinstance(mark, (int, float)):
>         raise TypeError("mark must be a number")
>     if not 0 <= mark <= 100:
>         raise ValueError("mark must be between 0 and 100")
>     for floor, letter in BANDS:
>         if mark >= floor:
>             return letter
> ```
> Tests: `grade(70) == "A"`, `grade(69.9) == "B"`, `grade(40) == "D"`, `grade(39) == "F"`; `pytest.raises(ValueError)` for `-1` and `100.1`; `pytest.raises(TypeError)` for `True` and `"70"`. *(Marks: correct bands 4; validation 3, including the `bool` check, which catches `True` being an `int`; tests 3.)*

> [!success]- B2 model solution (15)
> ```python
> def course_averages(lines):
>     totals = {}
>     skipped = 0
>     for line in lines[1:]:
>         parts = [p.strip() for p in line.split(",")]
>         if len(parts) != 3 or not parts[0] or not parts[1]:
>             skipped += 1
>             continue
>         try:
>             mark = float(parts[2])
>         except ValueError:
>             skipped += 1
>             continue
>         if not 0 <= mark <= 100:
>             skipped += 1
>             continue
>         totals.setdefault(parts[1], []).append(mark)
>     return {c: round(sum(m) / len(m), 1) for c, m in sorted(totals.items())}, skipped
> ```
> For the example: CST06102 = (71 + 64.5)/2 = 67.75 → **67.8**; GST06106 = (58 + 49)/2 = **53.5**; skipped: `abc`, the 2-field line, and 105 → **3**. *(Parsing 4; validation 5; averaging and rounding 3; skip count 3.)* Note: `round(67.75, 1)` gives 67.8 here, but binary floating point can make some halves round down; if exact decimal rounding matters, use `decimal`.

> [!success]- B3 model solution (15)
> ```python
> class InsufficientStock(Exception):
>     def __init__(self, sku, wanted, available):
>         super().__init__(f"{sku}: wanted {wanted}, only {available} available")
>         self.sku, self.wanted, self.available = sku, wanted, available
>
>
> class Stock:
>     def __init__(self):
>         self._qty = {}
>
>     def add(self, sku, qty):
>         if qty <= 0:
>             raise ValueError("quantity must be positive")
>         self._qty[sku] = self._qty.get(sku, 0) + qty
>
>     def remove(self, sku, qty):
>         if qty <= 0:
>             raise ValueError("quantity must be positive")
>         available = self._qty.get(sku, 0)
>         if qty > available:
>             raise InsufficientStock(sku, qty, available)   # checked before any change
>         self._qty[sku] = available - qty
>
>     def quantity(self, sku):
>         return self._qty.get(sku, 0)
>
>     def __len__(self):
>         return sum(1 for q in self._qty.values() if q > 0)
> ```
> *(Exception class with attributes 4; validation 3; remove leaves stock unchanged on failure 4; `__len__` counting only positive quantities 2; encapsulation (`_qty`) 2.)*

> [!success]- C1 model answer (15)
> (a) Any three: cryptic names (`d`, `l`); magic numbers (25000, 10000, 500, 20); `== True` instead of a plain truth test; the cap is expressed as a day count (20) rather than as the amount, so changing the daily rate silently breaks it; **negative days produce a negative fee**; no validation or docstring. *(1 each, up to 3, plus 3 for explaining why they matter.)*
> (b)
> ```python
> LATE_FEE_PER_DAY = 500
> LATE_FEE_CAP = 10_000
> LOST_ITEM_FEE = 25_000
>
>
> def late_fee(days_late):
>     if days_late < 0:
>         raise ValueError("days_late cannot be negative")
>     return min(days_late * LATE_FEE_PER_DAY, LATE_FEE_CAP)
>
>
> def total_fee(days_late, lost):
>     return LOST_ITEM_FEE if lost else late_fee(days_late)
> ```
> *(5.)* Behaviour is preserved for valid inputs: 20 days → 10,000 and 21 days → 10,000 in both versions.
> (c) `late_fee(-1)` raises `ValueError`; `late_fee(0) == 0`; `late_fee(20) == 10_000`; `late_fee(21) == 10_000`; `total_fee(3, True) == 25_000`. *(4.)*

> [!success]- C2 model answer (15)
> (a)
> ```python
> def first_index(items, target):
>     lo, hi, found = 0, len(items) - 1, -1
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         if items[mid] < target:
>             lo = mid + 1
>         elif items[mid] > target:
>             hi = mid - 1
>         else:
>             found, hi = mid, mid - 1   # record, then keep searching left
>     return found
> ```
> *(7: the "keep searching left" step is the key mark.)*
> (b) `first_index([], 5) == -1`; `first_index([5], 5) == 0`; `first_index([1, 2, 2, 2, 3], 2) == 1`; `first_index([1, 3, 5], 4) == -1`; `first_index([2, 2, 2], 2) == 0`. *(5.)*
> (c) A linear scan may inspect all $n$ elements. Each binary-search step halves the remaining range, so after $k$ steps $n/2^k$ elements remain; it stops when that reaches 1, i.e. after about $\log_2 n$ steps. *(3.)*

**Grade boundaries for self-assessment (designed):** ≥ 70 strong; 50–69 secure, revise the weakest section; < 50 → add the weakest topics to [[Weak Area Tracker]].

Back to [[Exam Technique and Assessment Strategy]] · [[QB-PY Python Question Bank]] · [[PY 00 Dashboard]]
