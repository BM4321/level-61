---
title: "Input, Output and String Formatting"
aliases:
  - f-strings
  - print and input
module: "Python Programming"
module_code: "CST06102"
topic_id: "PY-03"
type: "lesson"
unit: "U1 Foundations"
difficulty: "beginner"
syllabus_status: "provisional-core"
status: "not-started"
mastery: 0
prerequisites:
  - "[[PY-02 Variables, Types, Expressions and Operators]]"
next: "[[PY-04 Conditions and Branching]]"
last_reviewed: ""
next_review: ""
tags:
  - semester-6
  - python
  - programming-fundamentals
---

# PY-03 Input, Output and String Formatting

> [!info] Topic card
> **Unit:** U1 · **Time:** 2–3 h · **Code:** `examples/py03_io.py`, `exercises/py03_exercises.py`

## 1. Learning objectives
1. **Use** `print()` with multiple arguments and the `sep`, `end` and `file` parameters.
2. **Read** user input with `input()` and **convert** it safely.
3. **Format** output with f-strings and format specifications: width, alignment, precision, thousands separators, padding and percentages.
4. **Distinguish** `str()` from `repr()`, and the display value from the stored value.
5. **Separate** computation (functions returning strings) from I/O (printing). This makes code testable.

## 2. Why it matters
Programs communicate through I/O. Clean, aligned output makes reports readable. More importantly, *separating formatting from printing* is the first step toward testable design, a theme of [[PY-20 Testing, Debugging and Test-Driven Development]].

## 3. Prerequisites
[[PY-02 Variables, Types, Expressions and Operators]]: types and conversion, especially "`input()` returns `str`".

## 4. Intuition
`print` is a **printer**: it converts each argument to text, joins them with a separator, and adds a line ending. An f-string is a **template with holes**: `f"Total: {total:.2f}"` means "put `total` here, shown with 2 decimals".

## 5. Rigorous explanation

### 5.1 `print`
Signature (simplified): `print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)`.
- Each object is converted with `str()`.
- The pieces are joined with `sep`, then `end` is written.
```python
print("a", "b", "c")             # a b c
print("a", "b", "c", sep="-")    # a-b-c
print("no newline", end="")      # cursor stays on the line
print()                          # just a newline
```

### 5.2 `input`
`input(prompt)` writes the prompt, reads one line from standard input, and returns it **without** the trailing newline, **always as `str`**. If input ends (Ctrl-D / Ctrl-Z, or a closed pipe), it raises `EOFError`.

### 5.3 f-strings and the format-spec mini-language
`f"{expression:spec}"`. The general spec form is `[[fill]align][sign][width][,][.precision][type]`.

| Spec | Example | Result | Meaning |
|---|---|---|---|
| `.2f` | `f"{3.14159:.2f}"` | `3.14` | Fixed-point, 2 decimals |
| `10` | `f"{'hi':10}"` | `'hi        '` | Width 10 (strings left-align by default) |
| `>10` | `f"{'hi':>10}"` | `'        hi'` | Right-align |
| `^10` | `f"{'hi':^10}"` | `'    hi    '` | Centre |
| `*^10` | `f"{'hi':*^10}"` | `'****hi****'` | Fill character `*` |
| `05d` | `f"{42:05d}"` | `00042` | Zero-pad an integer |
| `,` | `f"{1234567:,}"` | `1,234,567` | Thousands separator |
| `,.2f` | `f"{1234.5:,.2f}"` | `1,234.50` | Both |
| `.1%` | `f"{0.256:.1%}"` | `25.6%` | Multiply by 100 and add % |
| `+` | `f"{5:+}"` | `+5` | Always show the sign |
| `e` | `f"{12345.678:.2e}"` | `1.23e+04` | Scientific notation |
| `=` (3.8+) | `f"{x=}"` | `x=5` | Debug: shows the expression and its value |

Numbers right-align by default, and strings left-align.

### 5.4 `str` vs `repr`
`str(obj)` is the *user-friendly* text. `repr(obj)` is the *unambiguous, developer* text. For strings, `repr` includes the quotes and escapes: `repr("a\nb")` → `'a\\nb'` (shown as `'a\nb'`). In f-strings, `{x!r}` uses `repr`. The REPL echo uses `repr` (see [[PY-01 How Python Executes Programs and Environment Setup]]).

### 5.5 Escape sequences
`\n` newline, `\t` tab, `\\` backslash, `\"` quote. In **raw strings** (`r"C:\new"`) backslashes are literal. That's handy for Windows paths and regular expressions.

### 5.6 Formatting is display only
`f"{2.675:.2f}"` gives `'2.67'` or `'2.68'`, depending on the binary value stored ([[PY-02 Variables, Types, Expressions and Operators]], §5.6). Formatting **does not change** the number. Never format first and then compute with the string.

## 6. Terminology
| Term | Meaning |
|---|---|
| Standard output / input | Default text output (screen) / input (keyboard) streams |
| f-string | String literal prefixed with `f`, containing `{expressions}` |
| Format specification | The part after `:` in `{value:spec}` |
| `repr` | Unambiguous representation intended for developers |
| Escape sequence | Backslash code for special characters |
| Separation of concerns | Keeping computation separate from presentation/I/O |

## 7. Step-by-step: building an aligned table
Goal:
```text
Item            Qty     Price
Pen               3      1.50
Notebook         12     25.00
```
1. Choose column widths: name 14 (left), qty 5 (right), price 10 (right, 2 decimals).
2. Header: `f"{'Item':<14}{'Qty':>5}{'Price':>10}"`.
3. Rows: `f"{name:<14}{qty:>5}{price:>10.2f}"`.

## 8. Diagram: data flow through a program
```mermaid
flowchart LR
    K[Keyboard] -->|"input() → str"| C[Convert:<br/>int()/float()]
    C --> P[Process:<br/>pure functions]
    P -->|return values| F[Format:<br/>f-strings]
    F -->|"print()"| S[Screen]
```
*Text version: input arrives as text, is converted to numbers, processed by pure functions, formatted into strings, and printed. Keeping each stage separate means the processing and formatting steps can be tested without a keyboard.*

## 9. Worked examples

### Example 1 (basic): greeting with conversion
```python
name = input("Name: ")            # 'Juma'
age = int(input("Age: "))         # '20' -> 20
print(f"Hello {name}, next year you will be {age + 1}.")
```
**I/O:** `Juma`, `20` → `Hello Juma, next year you will be 21.`
**Edge cases:** an age typed as `20.5` raises `ValueError` from `int()`. A name with surrounding spaces stays as typed, so use `input().strip()` to remove them.

### Example 2 (intermediate): receipt formatter. Incorrect → bug → corrected
```python
# INCORRECT: computation, formatting and printing tangled; columns misaligned
items = [("Pen", 3, 1.5), ("Notebook", 12, 25)]
for name, qty, price in items:
    print(name, qty, price * qty)
```
Output: `Pen 3 4.5` / `Notebook 12 300`. The columns don't align, there are no fixed decimals (`300` vs `4.5`), and it can't be tested.

**Bug analysis:** `print` with default `sep=' '` gives variable-width columns, and floats print their shortest representation.
```python
# CORRECTED: pure function returning a string
def format_receipt(items: list[tuple[str, int, float]]) -> str:
    lines = [f"{'Item':<14}{'Qty':>5}{'Total':>10}"]
    grand = 0.0
    for name, qty, price in items:
        line_total = qty * price
        grand += line_total
        lines.append(f"{name:<14}{qty:>5}{line_total:>10.2f}")
    lines.append(f"{'TOTAL':<19}{grand:>10.2f}")
    return "\n".join(lines)

print(format_receipt([("Pen", 3, 1.5), ("Notebook", 12, 25)]))
```
Output:
```text
Item            Qty     Total
Pen               3      4.50
Notebook         12    300.00
TOTAL                  304.50
```
Now a test can assert on the returned string without capturing the screen.

### Example 3 (challenging): progress bar on one line
```python
def progress_bar(done: int, total: int, width: int = 20) -> str:
    fraction = done / total
    filled = int(fraction * width)            # truncate: bar never overstates progress
    return f"[{'#' * filled}{'.' * (width - filled)}] {fraction:6.1%}"

print(progress_bar(7, 20))   # [#######.............]  35.0%
```
- `'#' * filled` repeats a string.
- `{fraction:6.1%}` shows the percentage in a field of width 6.
- **Edge cases:** `total == 0` raises `ZeroDivisionError`, so decide on a policy (raise `ValueError`, or treat it as 100%). `done > total` overflows the bar, so clamp it with `min(done, total)`.
- **Complexity:** $O(w)$ for width $w$.

## 10. Application
A lecturer exports marks to the screen for a quick check before saving them to CSV ([[PY-14 Files, CSV and JSON]]). Aligned columns with fixed decimals let them spot an outlier such as `105.00` instantly. This is the report function in [[PRJ-PY-01 Student Marks and Grading System]].

## 11. Common mistakes
| Mistake | Why | Fix |
|---|---|---|
| `print("Total: " + total)` → `TypeError` | Concatenating `str` and a number | Use an f-string: `f"Total: {total}"` |
| Forgetting the `f` prefix: `"Total {total}"` | Looks almost identical | Add `f` |
| `f"{price:.2}"` expecting 2 decimals | Without `f`, `.2` means 2 *significant digits* | Use `.2f` |
| Rounding with formatting, then computing | Formatting produces a `str` | Compute with numbers, format at the end |
| `input()` result never stripped | Trailing spaces break comparisons | `.strip()` |
| Printing inside every function | Makes testing hard | Return strings; print at the edge of the program |

## 12. Comparison
| Technique | Example | Status |
|---|---|---|
| f-string | `f"{x:.2f}"` | **Preferred** (3.6+) |
| `str.format` | `"{:.2f}".format(x)` | Fine. Useful for templates stored separately from the data |
| `%` formatting | `"%.2f" % x` | Legacy. Still seen in `logging` |
| Concatenation | `"a" + str(x)` | Error-prone for anything non-trivial |

## 13. Practice
**L1** 1. What do `print(1, 2, 3, sep="")` and `print("x", end="!")` output? 2. What is the difference between `f"{3.14159:.2f}"` and `f"{3.14159:.2}"`?

**L2** *(code bank)* 3. `format_money(amount)` → `"TZS 1,234.50"` style (comma thousands separator, 2 decimals). 4. `format_row(name, qty, price)` → a 29-character row exactly as in §7.

**L3** 5. `format_receipt(items)` as in Example 2 (must match the expected string exactly). 6. `progress_bar(done, total, width=20)`, which must clamp `done` to `[0, total]` and raise `ValueError` if `total <= 0`.

**L4** 7. A user enters marks as `"  78 "`, `"78.5"` or `"seventy"`. Write `parse_mark(text) -> float` that strips the text, converts it, and raises `ValueError` with a helpful message if the text is non-numeric or outside 0–100.

**L5** 8. Design `format_table(rows, headers)` that computes each column's width from its longest entry and right-aligns numbers but left-aligns text. Explain why computing the widths first needs two passes over the data.

**Variation:** modify `format_money` to accept a currency code and a number of decimals.

## 14. Hints
> [!tip]- Hints
> 3: `f"{amount:,.2f}"`. 6: `done = max(0, min(done, total))`. 7: Try `float(text.strip())`, then check the range. 8: The first pass gets `max(len(str(cell)))` per column. Use `isinstance(cell, (int, float))` to choose alignment.

## 15. Worked solutions
> [!success]- Solution 1–2
> 1. `123`, then `x!` with no newline after it. 2. `.2f` → `3.14` (2 decimals). `.2` → `3.1` (2 significant digits, general format).

> [!success]- Solutions 3–6
> ```python
> def format_money(amount: float) -> str:
>     return f"TZS {amount:,.2f}"
>
> def format_row(name: str, qty: int, price: float) -> str:
>     return f"{name:<14}{qty:>5}{price:>10.2f}"
>
> def progress_bar(done: int, total: int, width: int = 20) -> str:
>     if total <= 0:
>         raise ValueError("total must be positive")
>     done = max(0, min(done, total))
>     fraction = done / total
>     filled = int(fraction * width)
>     return f"[{'#' * filled}{'.' * (width - filled)}] {fraction:6.1%}"
> ```
> `format_receipt` is shown in Example 2.

> [!success]- Solution 7
> ```python
> def parse_mark(text: str) -> float:
>     cleaned = text.strip()
>     try:
>         value = float(cleaned)
>     except ValueError:
>         raise ValueError(f"not a number: {text!r}") from None
>     if not 0 <= value <= 100:
>         raise ValueError(f"mark out of range 0-100: {value}")
>     return value
> ```
> `{text!r}` shows the quotes and spaces, so the user sees exactly what was wrong. `from None` hides the internal conversion error from the traceback ([[PY-15 Exceptions and Defensive Programming]]).

> [!success]- Solution 8
> ```python
> def format_table(rows: list[list], headers: list[str]) -> str:
>     table = [headers] + rows
>     widths = [max(len(str(r[c])) for r in table) for c in range(len(headers))]
>     def fmt(cell, w):
>         return f"{cell:>{w}}" if isinstance(cell, (int, float)) else f"{str(cell):<{w}}"
>     return "\n".join("  ".join(fmt(cell, w) for cell, w in zip(row, widths)) for row in table)
> ```
> **Two passes:** a column's width depends on *every* row, including ones not yet seen, so you can't format row 1 until you have scanned all rows. Nested braces `{cell:>{w}}` let the width itself be a variable.

## 16. Self-test (pass ≥ 4/5)
1. `f"{7:03d}"`? 2. `f"{0.5:.0%}"`? 3. `f"{'ab':>4}|"`? 4. Default `sep` and `end` of `print`? 5. Why return a string rather than print inside a function?
> [!success]- Answers
> 1. `007`. 2. `50%`. 3. `'  ab|'`. 4. `' '` and `'\n'`. 5. A returned string can be tested, reused (file, web page) and composed. Printing locks you to the console.

## 17. Flashcards
#flashcards/python
Format a float with 2 decimals and thousands separators::f"{x:,.2f}"
What does `{x!r}` do in an f-string?::Inserts repr(x), e.g. strings shown with quotes.
Default alignment of numbers vs strings in a format field?::Numbers right-aligned, strings left-aligned.
What does `input()` return at end of input?::It raises EOFError.
Difference between `.2f` and `.2` format specs?::.2f = 2 decimal places; .2 = 2 significant digits.
What does `f"{x=}"` print?::The expression text and its value, e.g. x=5 (debug format, 3.8+).

## 18. Blank-page recall
Write the format-spec pattern `[[fill]align][sign][width][,][.precision][type]` with one example per part.

## 19. Revision summary
- `print(*objs, sep, end)`. `input()` → `str`, so always convert and strip.
- f-strings: `{value:spec}`, e.g. `<`, `>`, `^`, width, `.2f`, `,`, `%`, `0` padding, `!r`, `=`.
- Formatting is for display only. Compute with numbers.
- Return strings from functions. Print at the program's edge.

## 20. Links
Prev: [[PY-02 Variables, Types, Expressions and Operators]] · Next: [[PY-04 Conditions and Branching]] · Used in: [[PRJ-PY-01 Student Marks and Grading System]] · Deeper strings: [[PY-09 Strings and String Processing]]

## 21. Sources
- Python docs, *Format Specification Mini-Language*: https://docs.python.org/3/library/string.html#formatspec
- Python docs, *Input and Output* (tutorial §7): https://docs.python.org/3/tutorial/inputoutput.html
- PEP 498 *Literal String Interpolation*: https://peps.python.org/pep-0498/

## 22. Mastery checklist
- [ ] `py03` tests pass with `PY_TARGET=exercises`
- [ ] I can produce an aligned table without looking up the syntax
- [ ] Self-test ≥ 4/5 · reviews scheduled
