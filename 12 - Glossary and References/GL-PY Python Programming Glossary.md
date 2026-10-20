---
title: "Python Programming Glossary"
module: "Python Programming"
module_code: "CST06102"
type: "glossary"
tags:
  - semester-6
  - python
  - glossary
---

# GL-PY Python Programming Glossary

Every term below is taken from the Terminology section (§6) of the lesson it links to, so the definitions match the lessons. Generated at the last build; 190 terms.

| Term | Meaning | Lesson |
|---|---|---|
| Abstract class / method | Cannot be instantiated / must be implemented by subclasses | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Abstraction | Ignoring irrelevant details; naming a process | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Accumulator | Variable that builds up a result (sum, product, list) | [[PY-05 Loops and Iteration\|PY-05]] |
| Adaptive | Faster on partially sorted input | [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Adjacency list | Map from each vertex to its neighbours | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| ADT | Abstract data type: operations and behaviour | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Aggregate | Function over many rows: COUNT, SUM, AVG, MIN, MAX | [[PY-22 SQL and Database Integration\|PY-22]] |
| Algorithm | Finite, definite, effective procedure from inputs to outputs | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Alias | Second name for the same object | [[PY-10 Lists and Tuples\|PY-10]] |
| Allowlist / blocklist | Accept only known-good / reject known-bad | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Amdahl's law | Overall speed-up limit given the fraction optimised | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Amortised $O(1)$ | Average cost per operation over many operations | [[PY-10 Lists and Tuples\|PY-10]] |
| Argument | Value supplied in a call | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Assertion | Checked expectation | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Asymptotic | Behaviour as $n \to \infty$ | [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Atomic operation | Happens completely or not at all | [[PY-14 Files, CSV and JSON\|PY-14]] |
| Attribute | Data stored on an object or class | [[PY-16 Classes and Objects\|PY-16]] |
| Backoff | Increasing the delay between retries | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Base case | Input answered without recursion | [[PY-07 Recursion\|PY-07]] |
| Base / parent / superclass | Class being inherited from | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| BFS / DFS | Breadth-first / depth-first search | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Big-O / Ω / Θ | Upper / lower / tight bound up to constants | [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Boundary value | Input exactly at, just below and just above a threshold | [[PY-04 Conditions and Branching\|PY-04]], [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Branch | One alternative block | [[PY-04 Conditions and Branching\|PY-04]] |
| Call tree | Tree of all calls made | [[PY-07 Recursion\|PY-07]] |
| Canonicalisation | Converting input to a standard form before validating | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Characterisation test | Test capturing the current behaviour before changing the code | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| CI | Continuous integration: automated checks on every change | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Class | Blueprint defining attributes and methods | [[PY-16 Classes and Objects\|PY-16]] |
| Closure | Inner function that captures enclosing variables | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Code point | Integer identifying a Unicode character | [[PY-09 Strings and String Processing\|PY-09]] |
| Code smell | Surface symptom of a deeper design problem | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Collision | Two keys mapping to the same table slot | [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Composition | Object built from other objects (has-a) | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Comprehension | Expression building a collection from an iterable | [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Condition / predicate | Expression evaluated for truthiness | [[PY-04 Conditions and Branching\|PY-04]] |
| Constant-time comparison | Comparison whose duration doesn't depend on where the inputs differ | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Constructor | `__init__`, which initialises a new object | [[PY-16 Classes and Objects\|PY-16]] |
| Context manager | Object defining `__enter__`/`__exit__` for `with` | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Counterexample | A specific input for which an algorithm fails | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Coverage | Proportion of code executed by the tests | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Cross-cutting concern | Behaviour needed in many places (logging, timing, auth) | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Current working directory | Base for relative paths | [[PY-14 Files, CSV and JSON\|PY-14]] |
| DDL / DML | Data definition (schema) / manipulation (data) language | [[PY-22 SQL and Database Integration\|PY-22]] |
| Decomposition | Splitting a problem into sub-problems | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Decorator | Callable that transforms a function or class | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Decreasing measure | Quantity that strictly decreases each call (guarantees termination) | [[PY-07 Recursion\|PY-07]] |
| Deep copy | Recursive copy of all nested objects | [[PY-10 Lists and Tuples\|PY-10]] |
| Delegation | Forwarding a call to a component | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Delimiter | Character separating fields (`,`, `;`, `\t`) | [[PY-09 Strings and String Processing\|PY-09]] |
| Delimiter / quoting | Field separator / rules for fields containing it | [[PY-14 Files, CSV and JSON\|PY-14]] |
| Dependency | External package your code needs | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| Derived / child / subclass | Class that inherits | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Deserialisation | The reverse | [[PY-14 Files, CSV and JSON\|PY-14]] |
| Desk check / dry run | Executing an algorithm by hand | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Divide and conquer | Split into parts, solve recursively, combine | [[PY-07 Recursion\|PY-07]], [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Docstring | String literal first in a function, describing it | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]], [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Duck typing | Behaviour-based typing ("has the method?") | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Dunder method | Special `__name__` method hooked into Python syntax | [[PY-16 Classes and Objects\|PY-16]] |
| EAFP / LBYL | Try-then-handle / check-then-act | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Edge case | Input at the extremes of the valid range | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Encapsulation | Bundling data with methods, and hiding internal representation | [[PY-16 Classes and Objects\|PY-16]] |
| Encoding | Mapping between code points and bytes (UTF-8) | [[PY-09 Strings and String Processing\|PY-09]], [[PY-14 Files, CSV and JSON\|PY-14]] |
| Endpoint | URL of an API operation | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Entry point | Script/module you run to start the program | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]], [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Equivalence class | Set of inputs expected to behave the same | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Escape sequence | Backslash code for special characters | [[PY-03 Input, Output and String Formatting\|PY-03]] |
| Exception | Object representing an error condition | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Exception chaining | Linking a new exception to its cause | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Exhaustive | Every input is handled by some branch | [[PY-04 Conditions and Branching\|PY-04]] |
| Fail fast | Detect and report errors as early as possible | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| File handle / object | Python object for reading or writing an open file | [[PY-14 Files, CSV and JSON\|PY-14]] |
| Fixture | Reusable setup for tests | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Foreign key | Column referencing a primary key elsewhere | [[PY-22 SQL and Database Integration\|PY-22]] |
| Format specification | The part after `:` in `{value:spec}` | [[PY-03 Input, Output and String Formatting\|PY-03]] |
| Frame | A call's local namespace and execution state | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| f-string | String literal prefixed with `f`, containing `{expressions}` | [[PY-03 Input, Output and String Formatting\|PY-03]] |
| `functools.wraps` | Copies metadata from the wrapped function | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Generator | Function containing `yield`, producing a lazy iterator | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Generator expression | Lazy comprehension producing items on demand | [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Guard clause | Early `return`/`raise` that handles a special case first | [[PY-04 Conditions and Branching\|PY-04]] |
| Handler | `except` clause that deals with it | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Hash | Integer derived from an object, used to locate it in a table | [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Hashable | Has a fixed hash, so it is usable as a dict key or set member | [[PY-10 Lists and Tuples\|PY-10]], [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Header | Request/response metadata line | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Heap property | Each parent ≤ its children (min-heap) | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Height (of a tree) | Edges on the longest root-to-leaf path | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Higher-order function | Function taking or returning functions | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Hotspot | Code consuming a large share of the run time | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Idempotent | Repeating it has the same effect (GET, PUT, DELETE: yes; POST: generally no) | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Immutable | Cannot be changed after creation | [[PY-09 Strings and String Processing\|PY-09]] |
| Index | Position of a character (0-based) | [[PY-09 Strings and String Processing\|PY-09]], [[PY-22 SQL and Database Integration\|PY-22]] |
| Infinite loop | Loop whose exit condition never becomes true | [[PY-05 Loops and Iteration\|PY-05]] |
| Injection | Untrusted data interpreted as code or commands | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| In-order traversal | Left subtree, node, right subtree | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| In-place | Uses $O(1)$ extra memory | [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Integration test | Tests components working together | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Invariant | Property that must hold for every valid object | [[PY-16 Classes and Objects\|PY-16]] |
| Iterable | Object that can be looped over | [[PY-05 Loops and Iteration\|PY-05]] |
| Iterable / iterator | Can produce an iterator / produces items via `next()` | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Iteration | One execution of the loop body | [[PY-05 Loops and Iteration\|PY-05]] |
| Join | Combining rows from tables on a condition | [[PY-22 SQL and Database Integration\|PY-22]] |
| KDF / work factor | Slow key-derivation function / its cost parameter | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Key / value | Lookup label / associated data | [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Lazy evaluation | Computing values only when needed | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| Least privilege | Grant only the permissions required | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| LIFO / FIFO | Last-in-first-out / first-in-first-out | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Linter / formatter | Tool flagging problems / enforcing layout | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Load factor | Entries ÷ buckets in a hash table | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Logger / handler / formatter | Named log source / output destination / message layout | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Loop invariant | Property true before and after every iteration | [[PY-05 Loops and Iteration\|PY-05]] |
| LSP | Subtypes must be substitutable for their base types | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Main guard | `if __name__ == "__main__":` block | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| Memoisation | Caching results of calls by argument | [[PY-07 Recursion\|PY-07]] |
| Method | Function defined in a class, called on instances | [[PY-16 Classes and Objects\|PY-16]] |
| Module | One `.py` file (or extension module) | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| MRO | Order in which classes are searched for attributes | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Mutable sequence | Ordered collection that can change (list) | [[PY-10 Lists and Tuples\|PY-10]] |
| Mutually exclusive | At most one branch can apply | [[PY-04 Conditions and Branching\|PY-04]] |
| Node / pointer (reference) | Element / link to another node | [[PY-21 Data Structures and Algorithm Design\|PY-21]] |
| Normalisation | Converting text to a canonical form (case, spacing) before comparing | [[PY-09 Strings and String Processing\|PY-09]] |
| Object / instance | A concrete value created from a class | [[PY-16 Classes and Objects\|PY-16]] |
| Off-by-one error | Loop runs one time too many or too few | [[PY-05 Loops and Iteration\|PY-05]] |
| Override | Subclass redefines an inherited method | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Package | Directory of modules with `__init__.py` | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| Packing / unpacking | Building / splitting a tuple from or into names | [[PY-10 Lists and Tuples\|PY-10]] |
| Parameter | Name in the definition | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Parameterised query | SQL with placeholders, with values bound separately | [[PY-22 SQL and Database Integration\|PY-22]] |
| Path traversal | Using `..` or absolute paths to escape a directory | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Persistence | Data surviving program termination | [[PY-14 Files, CSV and JSON\|PY-14]] |
| Pinning | Fixing exact dependency versions | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| Polymorphism | One interface, many implementations | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| Precondition | Condition that must hold before calling (e.g. sorted input) | [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Premature optimisation | Optimising before measuring or needing to | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Primary key | Column(s) uniquely identifying a row | [[PY-22 SQL and Database Integration\|PY-22]] |
| Profiler | Tool measuring where time (or memory) is spent | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Propagation | Exception travelling up the call stack | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Property | Method accessed like an attribute | [[PY-16 Classes and Objects\|PY-16]] |
| Pure function | No side effects; output depends only on inputs | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Query parameter | `key=value` pair after `?` | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Raise / throw | Signal an exception | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Rate limit | Maximum number of requests allowed per time window | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Recursive case | Input answered using calls on smaller inputs | [[PY-07 Recursion\|PY-07]] |
| Refactoring | Behaviour-preserving restructuring | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Referential integrity | Every foreign key value exists in the referenced table | [[PY-22 SQL and Database Integration\|PY-22]] |
| Regression test | Ensures a fixed bug stays fixed | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Relation / table | Set of rows with the same columns | [[PY-22 SQL and Database Integration\|PY-22]] |
| `repr` | Unambiguous representation intended for developers | [[PY-03 Input, Output and String Formatting\|PY-03]] |
| REST | Architectural style: resources, standard methods, statelessness | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Return value | Value sent back to the caller (`None` by default) | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Salt | Random per-password value stored with the hash | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Scope | Region of code where a name is visible | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| `self` | The instance a method is called on | [[PY-16 Classes and Objects\|PY-16]] |
| SemVer | MAJOR.MINOR.PATCH versioning rules | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Sentinel | Special input value that signals the end (e.g. `-1`, `"q"`) | [[PY-05 Loops and Iteration\|PY-05]] |
| Separation of concerns | Keeping computation separate from presentation/I/O | [[PY-03 Input, Output and String Formatting\|PY-03]] |
| Serialisation | Converting in-memory data to bytes or text | [[PY-14 Files, CSV and JSON\|PY-14]] |
| Shadowing | Your file name hiding a library module | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| Shallow copy | New outer container, shared inner objects | [[PY-10 Lists and Tuples\|PY-10]] |
| Short-circuit | Stopping evaluation once the result is known | [[PY-04 Conditions and Branching\|PY-04]] |
| Side effect | Observable change outside the function | [[PY-06 Functions, Parameters, Return Values and Scope\|PY-06]] |
| Slice | Substring defined by start, stop and step | [[PY-09 Strings and String Processing\|PY-09]] |
| Specification | Precise statement of inputs, outputs and conditions | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| Stable sort | Equal elements keep their relative order | [[PY-10 Lists and Tuples\|PY-10]], [[PY-12 Searching, Sorting and Complexity\|PY-12]] |
| Standard output / input | Default text output (screen) / input (keyboard) streams | [[PY-03 Input, Output and String Formatting\|PY-03]] |
| Static type checker | Tool analysing types without running the code (mypy) | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Status code | Three-digit result code | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Stepwise refinement | Writing high-level steps, then refining each | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing\|PY-08]] |
| `StopIteration` | Signals that an iterator is exhausted | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |
| `super()` | Proxy to call the next class's method in the MRO | [[PY-17 Inheritance, Composition and Polymorphism\|PY-17]] |
| `sys.modules` | Cache of imported modules | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| `sys.path` | List of directories searched on import | [[PY-13 Modules, Packages, Imports and Virtual Environments\|PY-13]] |
| Tail call | Recursive call that is the last action (not optimised in CPython) | [[PY-07 Recursion\|PY-07]] |
| TDD | Write the failing test first, then code, then refactor | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| Technical debt | Future cost created by expedient design choices | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Test double | Stand-in for a real dependency | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| TOCTOU | Race between checking a condition and using it | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| `tottime` / `cumtime` | Time inside the function only / including its callees | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Traceback | Report of the call stack at the point of failure | [[PY-15 Exceptions and Defensive Programming\|PY-15]] |
| Transaction | Unit of work that commits or rolls back as a whole | [[PY-22 SQL and Database Integration\|PY-22]] |
| Transport | Component that actually performs network I/O | [[PY-23 HTTP APIs and External Services\|PY-23]] |
| Trust boundary | Point where data enters from a less trusted source | [[PY-24 Secure Programming and Input Validation\|PY-24]] |
| Tuple / row, attribute / column | One record / one field | [[PY-22 SQL and Database Integration\|PY-22]] |
| Type hint / annotation | Declared expected type, checked statically | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring\|PY-19]] |
| Unit test | Tests one function or class in isolation | [[PY-20 Testing, Debugging and Test-Driven Development\|PY-20]] |
| View | Live window onto a dict's keys/values/items | [[PY-11 Dictionaries, Sets and Comprehensions\|PY-11]] |
| Wheel | Built distribution format (`.whl`) | [[PY-25 Performance, Packaging and Project Organization\|PY-25]] |
| Whitespace | Spaces, tabs, newlines | [[PY-09 Strings and String Processing\|PY-09]] |
| Winding / unwinding | Pushing frames down to the base / returning back up | [[PY-07 Recursion\|PY-07]] |
| Wrapper | Inner function adding behaviour around the original | [[PY-18 Iterators, Generators, Decorators and Context Managers\|PY-18]] |

Back to [[Glossary Index]]
