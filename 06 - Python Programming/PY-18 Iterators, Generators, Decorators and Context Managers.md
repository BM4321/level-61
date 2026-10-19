---
title: "Iterators, Generators, Decorators and Context Managers"
aliases:
  - Generators and yield
  - Python decorators
  - with statement
module: "Python Programming"
module_code: "CST06102"
topic_id: "PY-18"
type: "lesson"
unit: "U5 Object-Oriented Programming"
difficulty: "advanced"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
prerequisites:
  - "[[PY-17 Inheritance, Composition and Polymorphism]]"
  - "[[PY-06 Functions, Parameters, Return Values and Scope]]"
next: "[[PY-19 Type Hints, Documentation, Clean Code and Refactoring]]"
last_reviewed: ""
next_review: ""
tags:
  - semester-6
  - python
  - advanced-python
---

# PY-18 Iterators, Generators, Decorators and Context Managers

> [!info] Topic card
> **Unit:** U5 · **Status:** *supplementary* (commonly taught in intermediate Python; may be beyond your official syllabus) · **Time:** 4–5 h · **Code:** `examples/py18_advanced.py`, `exercises/py18_exercises.py`

## 1. Learning objectives
1. **Explain** the iterator protocol (`__iter__`, `__next__`, `StopIteration`), and **implement** an iterator class.
2. **Write** generator functions with `yield`, and **build** lazy data pipelines that use $O(1)$ memory.
3. **Write** decorators (with `functools.wraps`, and with arguments), and **explain** what `@decorator` desugars to.
4. **Implement** context managers with a class (`__enter__`/`__exit__`) and with `contextlib.contextmanager`.
5. **Judge** when these tools improve code and when they obscure it.

## 2. Why it matters
These four features are behind the code you already use: `for` loops (iterators), `open()` in `with` (context managers), `@property` and `@functools.cache` (decorators), and `range` / file reading (lazy iteration). Understanding them lets you process files larger than memory, factor out cross-cutting concerns (timing, logging, retries), and guarantee cleanup.

## 3. Prerequisites
[[PY-06 Functions, Parameters, Return Values and Scope]] (first-class functions, closures), [[PY-16 Classes and Objects]] (dunder methods), [[PY-15 Exceptions and Defensive Programming]] (`finally`).

## 4. Intuition
- An **iterator** is a **ticket dispenser**: each `next()` gives the next ticket, and when it's empty it says "no more" (`StopIteration`).
- A **generator** is a function that can **pause** (`yield`) and later **resume** where it left off, which gives you a dispenser without writing a class.
- A **decorator** is **gift wrapping**: the same function inside, with extra behaviour around it.
- A **context manager** is a **door with an automatic closer**: whatever happens inside the room, the door closes when you leave.

## 5. Rigorous explanation

### 5.1 The iterator protocol
- An **iterable** has `__iter__()` returning an iterator (lists, strings, dicts, files…).
- An **iterator** has `__next__()` returning the next item or raising `StopIteration`, and `__iter__()` returning itself.
- `for x in obj:` means: `it = iter(obj)`, then repeatedly `x = next(it)` until `StopIteration`.
```python
class Countdown:
    def __init__(self, start: int):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

list(Countdown(3))      # [3, 2, 1]
```
An iterator is **single-use**. After it's exhausted, iterating again yields nothing. A list is re-iterable because each `iter(list)` creates a fresh iterator.

### 5.2 Generators
```python
def countdown(start: int):
    while start > 0:
        yield start          # pause here; resume on the next next()
        start -= 1

gen = countdown(3)           # NOTHING runs yet: it creates a generator object
next(gen)                    # 3 (runs until the first yield)
next(gen)                    # 2
```
Calling a generator function returns a generator (an iterator). The body runs **lazily**, only as values are requested. Local state is preserved between `yield`s. When the function returns, `StopIteration` is raised automatically.

**Generator expressions:** `(x * x for x in data)` is like a list comprehension but lazy. `sum(x * x for x in range(10**8))` needs constant memory, while `sum([x * x for x in range(10**8)])` builds a list of 100 million ints first.

**Pipelines:** chain generators so that each line flows through every stage before the next line is read:
```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

def non_blank(lines):
    return (ln for ln in lines if ln.strip())

def parse_ints(lines):
    for ln in lines:
        try:
            yield int(ln)
        except ValueError:
            continue

total = sum(parse_ints(non_blank(read_lines("numbers.txt"))))   # O(1) memory
```
`yield from other_iterable` delegates to a sub-iterator (handy for recursive generators such as tree traversal).

**Useful `itertools`:** `islice` (take a slice of an iterator), `count`, `chain`, `groupby` (consecutive groups; sort first), `accumulate`, `pairwise` (3.10+), `batched` (3.12+).

### 5.3 Decorators
`@decorator` above `def f` means `f = decorator(f)`. A decorator is a function that takes a function and returns a (usually wrapped) function.
```python
import functools
import time

def timed(func):
    @functools.wraps(func)                 # keep func's __name__, docstring, etc.
    def wrapper(*args, **kwargs):          # accept any signature
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper

@timed
def slow_sum(n):
    return sum(range(n))
```
**Decorators with arguments** need one more level: `@retry(times=3)` means `f = retry(times=3)(f)`.
```python
def retry(times: int, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
        return wrapper
    return decorator
```
Standard decorators you already know: `@property`, `@classmethod`, `@staticmethod`, `@functools.cache`, `@dataclass`.

### 5.4 Context managers
`with expr as x: body` calls `expr.__enter__()` (its result is bound to `x`), runs the body, and then **always** calls `__exit__(exc_type, exc, tb)`. If `__exit__` returns a true value, the exception is **suppressed**. Normally return `None`/`False` so it propagates.
```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False                        # never swallow exceptions

with Timer() as t:
    sum(range(10**6))
print(f"{t.elapsed:.4f}s")
```
The same thing with a generator:
```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    result = {}
    try:
        yield result                        # value bound by "as"
    finally:
        result["elapsed"] = time.perf_counter() - start
```
Standard examples: `open(...)`, `threading.Lock()`, `sqlite3.connect(...)` (it manages a *transaction*, not closing, see [[PY-22 SQL and Database Integration]]), `tempfile.TemporaryDirectory()`, `contextlib.suppress(FileNotFoundError)`.

## 6. Terminology
| Term | Meaning |
|---|---|
| Iterable / iterator | Can produce an iterator / produces items via `next()` |
| `StopIteration` | Signals that an iterator is exhausted |
| Generator | Function containing `yield`, producing a lazy iterator |
| Lazy evaluation | Computing values only when needed |
| Decorator | Callable that transforms a function or class |
| Wrapper | Inner function adding behaviour around the original |
| `functools.wraps` | Copies metadata from the wrapped function |
| Context manager | Object defining `__enter__`/`__exit__` for `with` |
| Cross-cutting concern | Behaviour needed in many places (logging, timing, auth) |

## 7. Step-by-step: turning a list-building function into a generator
1. Find `result = []` … `result.append(x)` … `return result`.
2. Replace `result.append(x)` with `yield x`, then delete `result = []` and `return result`.
3. Callers that need a list write `list(gen(...))`. Callers that stream use `for`.
4. Remember that the generator can only be consumed once. Document this.

## 8. Diagram: lazy pipeline (values flow one at a time)
```mermaid
sequenceDiagram
    participant S as sum()
    participant P as parse_ints
    participant N as non_blank
    participant R as read_lines
    S->>P: next()
    P->>N: next()
    N->>R: next()
    R-->>N: "  " (blank)
    N->>R: next()
    R-->>N: "42"
    N-->>P: "42"
    P-->>S: 42
    Note over S,R: repeated per item; only one line in memory at a time
```
*Text version: `sum` asks `parse_ints` for an item, which asks `non_blank`, which asks `read_lines`. Blank lines are skipped inside `non_blank`. One value travels back up per request, so memory use doesn't depend on file size.*

## 9. Worked examples

### Example 1 (basic): generator trace
```python
def evens(limit):
    n = 0
    while n < limit:
        yield n
        n += 2

g = evens(5)
print(next(g), next(g), next(g))   # 0 2 4
print(next(g, "done"))             # 'done' (the default instead of StopIteration)
```
| call | state resumes at | n | yields |
|---|---|---|---|
| next #1 | start | 0 | 0 |
| next #2 | after `yield` | 2 | 2 |
| next #3 | after `yield` | 4 | 4 |
| next #4 | after `yield` | 6 → loop ends | StopIteration |

### Example 2 (intermediate): incorrect → bug → corrected (exhausted iterator)
```python
# INCORRECT
squares = (x * x for x in range(5))
print(sum(squares))     # 30
print(max(squares))     # ValueError: max() iterable argument is empty
```
**Bug:** a generator is single-use, and `sum` consumed it. **Fixes:** materialise it once (`squares = [x * x for x in range(5)]`) if you need multiple passes, or recreate the generator each time.

### Example 3 (challenging): decorator without `wraps` → broken introspection
```python
def logged(func):
    def wrapper(*args, **kwargs):
        print("calling", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@logged
def area(w, h):
    """Rectangle area."""
    return w * h

print(area.__name__, area.__doc__)   # wrapper None: the metadata is lost
```
Debuggers, `help()` and test reports now show "wrapper". **Fix:** decorate `wrapper` with `@functools.wraps(func)`, and then `area.__name__ == "area"`. Note also that `print` inside a library decorator is poor practice. Use `logging` ([[PY-25 Performance, Packaging and Project Organization]]).

### Example 4 (transfer): a counting decorator that keeps state
```python
def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(10)
print(fib.calls)    # 177: matches PY-07's naive call count
```
The recursive calls go through the decorated name `fib`, so they're counted too.

## 10. Application
A log analyser in [[LAB-CS-08 Log Analysis and Incident Response]] processes a multi-gigabyte authentication log with a generator pipeline (`read_lines → parse → filter failed logins → group by IP`). It never loads the file into memory. A `@timed` decorator measures each stage during optimisation ([[PY-25 Performance, Packaging and Project Organization]]).

## 11. Common mistakes
| Mistake | Fix |
|---|---|
| Reusing an exhausted generator | Materialise with `list()`, or recreate it |
| Expecting a generator function to run when called | It runs only on iteration |
| Decorator wrapper with a fixed signature `(x)` | Use `*args, **kwargs` |
| Forgetting `functools.wraps` | Always add it |
| `__exit__` returning `True` by accident | Return `False`/`None` unless you deliberately suppress |
| `@decorator(args)` written without the extra level | Decorator factory: three nested functions |
| Over-using decorators for core logic | Keep business rules explicit. Use decorators for cross-cutting concerns. |

## 12. Comparison
| Need | Tool |
|---|---|
| Re-iterable collection | list/tuple, or a class with `__iter__` returning a new generator |
| One-pass stream, large or infinite data | Generator |
| Add behaviour around many functions | Decorator |
| Guarantee setup/teardown | Context manager |
| Retry, timing, caching | Decorator (`functools.cache` for caching) |

## 13. Practice
**L1** 1. What does `for` call on the object it loops over? 2. What does `@d` above `def f` mean?

**L2** *(code bank)* 3. `Countdown` iterator class. 4. `fibonacci()`, an infinite generator, and `take(n, iterable)` using `itertools.islice`.

**L3** 5. `chunks(iterable, size)` is a generator yielding lists of `size` items (the last may be shorter) and works on **any** iterable, including generators. 6. `count_calls` decorator (Example 4).

**L4** 7. `retry(times, exceptions)` decorator factory. Test it with a function that fails twice. 8. `Timer` context manager class, plus a `timer()` generator-based version. Show that an exception inside the `with` still propagates **and** the time is recorded.

**L5** 9. Build a lazy pipeline `failed_logins_by_ip(lines)` for lines like `"2026-10-19T08:00:01 FAIL user=amina ip=10.0.0.5"`, returning `{ip: count}` for FAIL lines only. It must process a generator of 10⁶ lines without building a list. Explain the memory complexity of each stage.

**Variation:** make `chunks` yield tuples, and add a `strict=True` option that raises `ValueError` if the last chunk is short.

## 14. Hints
> [!tip]- Hints
> 4: `a, b = 0, 1; while True: yield a; a, b = b, a + b`. 5: `it = iter(iterable)`, then repeatedly `batch = list(islice(it, size))`, and stop when it's empty. 7: Three levels: `retry(...)` → `decorator(func)` → `wrapper(*args)`. 9: Use `str.split()` and a dict of counts. Only the dict grows, with $O(\#\text{distinct IPs})$ entries.

## 15. Worked solutions
> [!success]- Solutions 1–2
> 1. `iter(obj)` once, then `next()` on the result until `StopIteration`. 2. `f = d(f)`.

> [!success]- Solutions 4–5
> ```python
> from itertools import islice
>
> def fibonacci():
>     a, b = 0, 1
>     while True:
>         yield a
>         a, b = b, a + b
>
> def take(n, iterable):
>     return list(islice(iterable, n))
>
> def chunks(iterable, size):
>     if size < 1:
>         raise ValueError("size must be >= 1")
>     it = iter(iterable)
>     while True:
>         batch = list(islice(it, size))
>         if not batch:
>             return
>         yield batch
> ```
> `take(10, fibonacci())` → `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`. The infinite generator is safe because `islice` stops pulling.

> [!success]- Solution 8
> ```python
> def test_timer_records_even_on_error():
>     t = Timer()
>     with pytest.raises(ZeroDivisionError):
>         with t:
>             1 / 0
>     assert t.elapsed >= 0
> ```
> `__exit__` runs during exception propagation, records the time and returns `False`, so the exception continues to the test's `pytest.raises`.

> [!success]- Solution 9
> ```python
> def failed_logins_by_ip(lines):
>     counts = {}
>     for line in lines:
>         parts = line.split()
>         if len(parts) < 4 or parts[1] != "FAIL":
>             continue
>         fields = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
>         ip = fields.get("ip")
>         if ip:
>             counts[ip] = counts.get(ip, 0) + 1
>     return counts
> ```
> **Memory:** reading lines lazily is $O(1)$ per line, parsing is $O(\text{line length})$ temporary, and the result dict is $O(k)$ for $k$ distinct IPs. The total is independent of the number of lines. Malformed lines are skipped rather than crashing, but in a real security tool, also **count** the skipped lines (an attacker might craft lines to evade parsing).

## 16. Self-test (pass ≥ 4/5)
1. Why is `sum(x for x in big)` more memory-efficient than `sum([x for x in big])`? 2. What does `functools.wraps` preserve? 3. When does `__exit__` run? 4. What does `next(gen, default)` do at exhaustion? 5. How many nested functions does a decorator with arguments need?
> [!success]- Answers
> 1. The generator produces one item at a time, while the list materialises all items first. 2. The wrapped function's `__name__`, `__doc__`, `__module__`, `__qualname__` and `__wrapped__`. 3. Always on leaving the `with` block, whether normally or through an exception. 4. Returns the default instead of raising StopIteration. 5. Three: factory → decorator → wrapper.

## 17. Flashcards
#flashcards/python
What signals the end of an iterator?::Raising StopIteration (for loops handle it).
What does calling a generator function return?::A generator object; the body runs only when iterated.
Can a generator be iterated twice?::No. Once exhausted it yields nothing; recreate it or use a list.
@decorator above def f is equivalent to?::f = decorator(f)
Why use functools.wraps in decorators?::To preserve the wrapped function's name, docstring and metadata.
How does __exit__ suppress an exception?::By returning a true value (normally return False/None).

## 18. Blank-page recall
Write a generator, a decorator with `wraps`, and a class-based context manager from memory, each in under 10 lines.

## 19. Revision summary
- Iterator protocol: `iter()` + `next()` + `StopIteration`. Iterators are single-use.
- Generators (`yield`) are lazy and stateful. Pipelines run in $O(1)$ memory.
- Decorators wrap functions (`f = d(f)`). Always use `functools.wraps` and `*args, **kwargs`.
- Context managers guarantee cleanup. Don't suppress exceptions by accident.

## 20. Links
Prev: [[PY-17 Inheritance, Composition and Polymorphism]] · Next: [[PY-19 Type Hints, Documentation, Clean Code and Refactoring]] · Related: [[PY-07 Recursion]] (call counting), [[SD-11 Creational and Structural Design Patterns]] (the Decorator *pattern* differs from Python decorators but shares the wrapping idea)

## 21. Sources
- Python docs, *Iterators* and *Generators* (tutorial §9.8–9.10): https://docs.python.org/3/tutorial/classes.html#iterators
- Python docs, `itertools`: https://docs.python.org/3/library/itertools.html · `functools.wraps`: https://docs.python.org/3/library/functools.html#functools.wraps · `contextlib`: https://docs.python.org/3/library/contextlib.html
- PEP 255 *Simple Generators*; PEP 318 *Decorators for Functions and Methods*; PEP 343 *The "with" Statement*: https://peps.python.org/

## 22. Mastery checklist
- [ ] `py18` tests pass with `PY_TARGET=exercises`
- [ ] I built a three-stage lazy pipeline
- [ ] I wrote a decorator factory with arguments · reviews scheduled
