---
title: "Sets, Set Operations, Power Sets and Cartesian Products"
aliases:
  - Set theory
  - Venn diagrams
  - Power set
  - Cartesian product
module: "Discrete Mathematics"
module_code: "GST06106"
topic_id: "DM-06"
type: "lesson"
unit: "U3 Structures"
difficulty: "beginner"
syllabus_status: "provisional-core"
status: "not-started"
mastery: 0
prerequisites:
  - "[[DM-03 Predicates and Quantifiers]]"
next: "[[DM-07 Functions]]"
last_reviewed: ""
next_review: ""
tags:
  - semester-6
  - discrete-math
  - sets
---

# DM-06 Sets, Set Operations, Power Sets and Cartesian Products

> [!info] Topic card
> **Unit:** U3 · **Time:** 4 h · **Python analogue:** `set`, `frozenset`, `|`, `&`, `-`, `^`, `<=`, `itertools.product` ([[PY-11 Dictionaries, Sets and Comprehensions]])

## 1. Learning objectives
1. **Describe** sets in roster and set-builder notation, and **use** ∈, ⊆, ⊂, =, ∅, U and |A| correctly.
2. **Compute** unions, intersections, differences, complements and symmetric differences, and **draw** them as Venn regions.
3. **Prove** set identities by element ("double inclusion") arguments and by membership tables.
4. **Construct** power sets and Cartesian products, and **count** their sizes ($2^n$, $|A|\cdot|B|$).
5. **Represent** sets as bit strings and in Python, and **relate** the set laws to the logic laws.

## 2. Why it matters
Sets are the language of all of mathematics and much of computing: database tables are sets of tuples, types are sets of values, permissions are sets of rights, and test suites partition the input space. Set identities are the logic laws ([[DM-02 Logical Equivalence and Laws of Logic]]) seen through membership.

## 3. Prerequisites
[[DM-03 Predicates and Quantifiers]]: set-builder notation uses predicates, and subset proofs use ∀.

## 4. Intuition
A set is a **bag that ignores order and duplicates**: {1, 2, 2, 3} is the same set as {3, 1, 2}. The questions you can ask are "is this in the bag?" and "how many distinct things?"

## 5. Rigorous explanation

### 5.1 Notation, symbol by symbol
| Notation | Meaning | Example |
|---|---|---|
| $\{a, b, c\}$ | roster: list the elements | $\{2, 3, 5, 7\}$ |
| $\{x \in D \mid P(x)\}$ | set-builder: the elements of D satisfying P | $\{n \in \mathbb{Z} \mid n \text{ even}\}$ |
| $x \in A$ / $x \notin A$ | membership / non-membership | $3 \in \{1,3\}$ |
| $A \subseteq B$ | subset: $\forall x\,(x\in A \to x \in B)$ | $\{1\}\subseteq\{1,2\}$ |
| $A \subset B$ (or ⊊) | proper subset: $A\subseteq B$ and $A\ne B$ | |
| $A = B$ | $A \subseteq B$ and $B \subseteq A$ | |
| $\varnothing$ or $\{\}$ | empty set (a subset of every set) | |
| $U$ | universal set (the context) | all students |
| $\lvert A\rvert$ | cardinality (number of distinct elements) | $\lvert\{a,a,b\}\rvert = 2$ |
| ℕ, ℤ, ℚ, ℝ | naturals, integers, rationals, reals | (conventions differ on whether 0 ∈ ℕ, so state yours) |

### 5.2 Operations
| Operation | Definition | Logic counterpart | Python |
|---|---|---|---|
| Union $A\cup B$ | $\{x \mid x\in A \lor x\in B\}$ | ∨ | `A \| B` |
| Intersection $A\cap B$ | $\{x \mid x\in A \land x\in B\}$ | ∧ | `A & B` |
| Difference $A - B$ (or $A\setminus B$) | $\{x \mid x\in A \land x\notin B\}$ | $p\land\lnot q$ | `A - B` |
| Complement $\overline{A}$ (or $A^c$) | $\{x \in U \mid x\notin A\}$ | ¬ | `U - A` |
| Symmetric difference $A \oplus B$ (△) | $(A-B)\cup(B-A)$ | ⊕ | `A ^ B` |
**Disjoint:** $A \cap B = \varnothing$.

### 5.3 Set identities (compare with DM-02)
| Name | Identity |
|---|---|
| Identity | $A\cup\varnothing = A$, $A\cap U = A$ |
| Domination | $A\cup U = U$, $A\cap\varnothing=\varnothing$ |
| Complement | $A\cup\overline{A}=U$, $A\cap\overline{A}=\varnothing$, $\overline{\overline{A}}=A$ |
| Commutative, associative | as for ∨/∧ |
| Distributive | $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$, $A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$ |
| **De Morgan** | $\overline{A\cup B}=\overline{A}\cap\overline{B}$, $\overline{A\cap B}=\overline{A}\cup\overline{B}$ |
| Absorption | $A\cup(A\cap B)=A$, $A\cap(A\cup B)=A$ |
| Difference | $A - B = A\cap\overline{B}$ |

### 5.4 Proving set identities
- **Double inclusion:** to prove $X = Y$, show $X\subseteq Y$ (take an arbitrary $x\in X$, deduce $x\in Y$) **and** $Y\subseteq X$.
- **Membership table:** like a truth table, with 1 = "in the set" and 0 = "not in". Two sets are equal iff their columns match in every row.
- **Chain of identities:** like the algebraic proofs in DM-02.

### 5.5 Power sets and Cartesian products
- **Power set** $\mathcal{P}(A)$: the set of **all subsets** of A. If $|A| = n$, then $|\mathcal{P}(A)| = 2^n$ (each element is in or out of a subset: 2 choices per element, by the product rule).
  $\mathcal{P}(\{a,b\}) = \{\varnothing, \{a\}, \{b\}, \{a,b\}\}$.
- **Ordered pair** $(a,b)$: here order matters, and $(a,b) = (c,d)$ iff $a=c$ and $b=d$.
- **Cartesian product** $A \times B = \{(a,b)\mid a\in A, b\in B\}$, with $|A\times B| = |A|\cdot|B|$. In general $A\times B \ne B\times A$.
- $A^n$ = n-tuples from A, e.g. $\{0,1\}^8$ = all bytes, of which there are $2^8 = 256$.

### 5.6 Bit-string representation
Fix an order of $U = \{u_1, \dots, u_n\}$. Represent $A$ by the bit string with bit $i$ = 1 iff $u_i \in A$. Then ∪ is bitwise OR, ∩ is AND, and complement is NOT. This is how permission flags are stored (e.g. Unix `rwx` bits, [[CS-10 Operating System Security and Hardening]]).

## 6. Terminology
| Term | Meaning |
|---|---|
| Element / member | Object in a set |
| Roster / set-builder | Listing / describing by a property |
| Subset / proper subset | All elements contained / and not equal |
| Cardinality | Number of distinct elements |
| Disjoint | Empty intersection |
| Partition | Disjoint non-empty subsets whose union is the whole set |
| Power set | Set of all subsets |
| Cartesian product | Set of ordered pairs |

## 7. Step-by-step: double-inclusion proof of De Morgan, $\overline{A\cup B}=\overline{A}\cap\overline{B}$
**(⊆)** Let $x\in\overline{A\cup B}$. Then $x\notin A\cup B$, i.e. $\lnot(x\in A\lor x\in B)$. By De Morgan (logic), $x\notin A \land x\notin B$, so $x\in\overline{A}$ and $x\in\overline{B}$, i.e. $x\in\overline{A}\cap\overline{B}$.
**(⊇)** Let $x\in\overline{A}\cap\overline{B}$. Then $x\notin A$ and $x\notin B$, so $\lnot(x\in A\lor x\in B)$, i.e. $x\notin A\cup B$, so $x\in\overline{A\cup B}$.
Both inclusions hold, so the sets are equal. ∎ *Each set step is a logic step on membership statements, which is exactly why the laws mirror each other.*

## 8. Diagram: Venn regions of A and B (with U)
```text
 U ┌───────────────────────────────────────┐
   │      A                    B           │
   │   ┌──────────┐      ┌──────────┐      │
   │   │  A − B   │ A∩B  │  B − A   │      │
   │   │ (region1)│(reg2)│ (region3)│      │
   │   └──────────┘      └──────────┘      │
   │          outside both: region 4 = complement of (A∪B)
   └───────────────────────────────────────┘
```
*Text version: two overlapping circles split U into 4 regions. Region 1 is in A only, region 2 is in both, region 3 is in B only, and region 4 is in neither. A∪B = regions 1–3, A⊕B = regions 1 and 3, and the complement of A∪B = region 4. (Plain text is used because Mermaid has no Venn diagram type.) With three sets there are 8 regions, one per row of a 3-variable membership table.*

## 9. Worked examples

### Example 1 (basic): computing operations
$U=\{1,\dots,10\}$, $A=\{1,2,3,4,5\}$, $B=\{4,5,6,7\}$.
| Expression | Result |
|---|---|
| $A\cup B$ | {1, 2, 3, 4, 5, 6, 7} |
| $A\cap B$ | {4, 5} |
| $A - B$ | {1, 2, 3} |
| $B - A$ | {6, 7} |
| $A\oplus B$ | {1, 2, 3, 6, 7} |
| $\overline{A}$ | {6, 7, 8, 9, 10} |
| $\overline{A\cup B}$ | {8, 9, 10} = $\overline{A}\cap\overline{B}$ ✔ (De Morgan) |
Bit strings (positions 1..10): A = 1111100000, B = 0001111000. A AND B = 0001100000, i.e. {4, 5} ✔.

### Example 2 (intermediate): membership-table proof of $A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$
| A | B | C | B∩C | A∪(B∩C) | A∪B | A∪C | (A∪B)∩(A∪C) |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 1 | 0 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
The two target columns are identical, so the sets are equal. ∎

### Example 3 (challenging): power set and Cartesian product
$A = \{0, 1\}$, $B = \{x, y, z\}$.
- $\mathcal{P}(A) = \{\varnothing, \{0\}, \{1\}, \{0,1\}\}$, with $2^2 = 4$ elements.
- $|\mathcal{P}(\mathcal{P}(A))| = 2^4 = 16$.
- $A\times B = \{(0,x),(0,y),(0,z),(1,x),(1,y),(1,z)\}$, with $2\cdot 3 = 6$ pairs.
- $|\mathcal{P}(A\times B)| = 2^6 = 64$, the number of **relations** from A to B ([[DM-10 Relations, Equivalence Relations and Partial Orders]]).
- **Trap:** is $\varnothing\in\mathcal{P}(A)$? **Yes.** Is $\varnothing\subseteq\mathcal{P}(A)$? **Also yes** (∅ is a subset of every set). Is $0 \in \mathcal{P}(A)$? **No.** The elements of $\mathcal{P}(A)$ are *sets*, so $\{0\}\in\mathcal{P}(A)$ but $0 \notin \mathcal{P}(A)$.

## 10. Application: role-based permissions
Permissions per role: Lecturer = {read, edit_marks}, Admin = {read, edit_marks, manage_users}, Student = {read}. A user with roles {Lecturer, Student} has the **union** {read, edit_marks}. The "separation of duties" requirement *no user may both approve and pay an invoice* says that $\{\text{approve},\text{pay}\} \not\subseteq \text{perms}(u)$ for every user $u$. That's a set constraint that code can check ([[CS-04 Authorization and Access Control]]).

## 11. Common mistakes
| Mistake | Correct |
|---|---|
| Confusing ∈ with ⊆ | $1\in\{1,2\}$ but $\{1\}\subseteq\{1,2\}$; $1\subseteq\{1,2\}$ is meaningless |
| $\lvert\{1,1,2\}\rvert = 3$ | 2 (duplicates don't count) |
| $\{\varnothing\} = \varnothing$ | No. $\{\varnothing\}$ has one element. |
| $\overline{A\cap B}=\overline{A}\cap\overline{B}$ | De Morgan flips: $\overline{A}\cup\overline{B}$ |
| Proving equality by one inclusion | Need both directions |
| Proving with a Venn diagram picture | A diagram illustrates. A membership table or element argument proves. |
| $A\times B = B\times A$ | Ordered pairs: generally different |

## 12. Comparison
| Structure | Order? | Duplicates? | Example |
|---|---|---|---|
| Set | No | No | {1, 2} |
| Multiset (bag) | No | Yes | {1, 1, 2}, like `Counter` |
| Sequence / tuple | Yes | Yes | (1, 1, 2) |
| Ordered pair | Yes | — | (1, 2) ≠ (2, 1) |

## 13. Practice
**L1** 1. List $\{x\in\mathbb{Z}\mid -2 < x \le 3\}$. 2. True or false: $\varnothing\subseteq\{1\}$, $\varnothing\in\{1\}$, $\{1\}\in\{\{1\},2\}$, $\{1\}\subseteq\{\{1\},2\}$.

**L2** 3. With $U=\{1,\dots,8\}$, $A=\{1,2,3,4\}$, $B=\{3,4,5,6\}$, $C=\{2,4,6,8\}$, compute $A\cap B\cap C$, $(A\cup B)-C$, $\overline{A}\cap C$ and $A\oplus C$. 4. Write $\mathcal{P}(\{1,2,3\})$ and state its size.

**L3** 5. Prove by double inclusion: $A - (B\cup C) = (A-B)\cap(A-C)$. 6. Prove using identities: $\overline{(A\cup B)}\cup(\overline{A}\cap B) = \overline{A}$.

**L4** 7. Prove or disprove: (a) if $A\cup B = A\cup C$ then $B = C$; (b) $A\times(B\cap C) = (A\times B)\cap(A\times C)$. 8. In a class of 40, 25 study Python, 18 study Cyber Security, and 7 study both. How many study neither? Show it as a Venn computation ([[DM-12 Pigeonhole Principle and Inclusion-Exclusion]] generalises this).

**L5** 9. Prove that $|\mathcal{P}(A)| = 2^{|A|}$ for every finite set A, by induction on |A| ([[DM-09 Mathematical Induction]]): for an element $a$, the subsets of $A$ split into those without $a$ and those with $a$.

## 14. Hints
> [!tip]- Hints
> 2: careful with ∅ ∈ vs ⊆, and with sets as elements. 6: apply De Morgan to the first term, then factor out $\overline{A}$. 7(a): try $A = \{1\}$, $B = \{1\}$, $C = \varnothing$. 8: |P ∪ C| = 25 + 18 − 7.

## 15. Worked solutions
> [!success]- Solutions 1–2
> 1. {−1, 0, 1, 2, 3}. 2. T (∅ is a subset of everything), F (the only element of {1} is 1), T ({1} is listed as an element), F (the element 1 of {1} isn't an element of {{1}, 2}).

> [!success]- Solution 3
> $A\cap B\cap C = \{4\}$. $(A\cup B)-C = \{1,2,3,4,5,6\}-\{2,4,6,8\} = \{1,3,5\}$. $\overline{A}\cap C = \{5,6,7,8\}\cap\{2,4,6,8\} = \{6,8\}$. $A\oplus C = \{1,3\}\cup\{6,8\} = \{1,3,6,8\}$.

> [!success]- Solution 4
> $\{\varnothing,\{1\},\{2\},\{3\},\{1,2\},\{1,3\},\{2,3\},\{1,2,3\}\}$, with size $2^3 = 8$.

> [!success]- Solution 5
> (⊆) Let $x\in A-(B\cup C)$. Then $x\in A$ and $x\notin B\cup C$, so $x\notin B$ and $x\notin C$ (De Morgan). Hence $x\in A-B$ and $x\in A-C$, so $x\in(A-B)\cap(A-C)$.
> (⊇) Let $x\in(A-B)\cap(A-C)$. Then $x\in A$, $x\notin B$, $x\notin C$, so $x\notin B\cup C$. Hence $x\in A-(B\cup C)$. ∎

> [!success]- Solution 6
> $\overline{A\cup B}\cup(\overline{A}\cap B) = (\overline{A}\cap\overline{B})\cup(\overline{A}\cap B)$ (De Morgan) $= \overline{A}\cap(\overline{B}\cup B)$ (distributive) $= \overline{A}\cap U$ (complement) $= \overline{A}$ (identity). ∎

> [!success]- Solution 7
> (a) **False.** $A=\{1\}$, $B=\{1\}$, $C=\varnothing$: $A\cup B = \{1\} = A\cup C$, but $B\ne C$.
> (b) **True.** $(a,x)\in A\times(B\cap C) \iff a\in A \land x\in B \land x\in C \iff (a,x)\in A\times B \land (a,x)\in A\times C$. ∎

> [!success]- Solution 8
> $|P\cup C| = |P| + |C| - |P\cap C| = 25 + 18 - 7 = 36$, so **4** study neither. Regions: Python only 18, both 7, Cyber only 11, neither 4 (18 + 7 + 11 + 4 = 40 ✔).

> [!success]- Solution 9
> Let $S(n)$: "every set with n elements has $2^n$ subsets". **Base** $n=0$: the only subset of ∅ is ∅, so there is 1 = $2^0$ subset ✔. **Step:** assume $S(k)$, and let $|A| = k+1$. Pick $a\in A$ and let $A' = A - \{a\}$, so $|A'| = k$. Every subset of A either excludes $a$ (and is a subset of $A'$: $2^k$ of them, by the hypothesis) or includes $a$ (and is $T\cup\{a\}$ for a unique subset $T\subseteq A'$: another $2^k$). These cases are disjoint and exhaustive, so there are $2^k + 2^k = 2^{k+1}$ subsets. By induction, $S(n)$ holds for all n ≥ 0. ∎

## 16. Self-test (pass ≥ 4/5)
1. $|\mathcal{P}(\varnothing)|$? 2. $\overline{A\cap B}$ = ? 3. How do you prove A = B? 4. $|A\times B|$ for |A| = 3, |B| = 4? 5. Is {2} ∈ {1, 2, 3}?
> [!success]- Answers
> 1. 1 (namely {∅}). 2. $\overline{A}\cup\overline{B}$. 3. Show A ⊆ B and B ⊆ A. 4. 12. 5. No ({2} ⊆ {1, 2, 3}, but 2, not {2}, is the element).

## 17. Flashcards
#flashcards/discrete-math
Size of the power set of an n-element set?::2ⁿ
Size of A × B?::|A|·|B|
De Morgan for sets?::complement(A∪B) = Ā∩B̄ and complement(A∩B) = Ā∪B̄
How to prove two sets equal?::Double inclusion: A ⊆ B and B ⊆ A.
A − B equals?::A ∩ B̄
Difference between ∈ and ⊆?::∈ relates an element to a set; ⊆ relates a set to a set.
Symmetric difference A ⊕ B?::Elements in exactly one of A and B: (A−B) ∪ (B−A).

## 18. Blank-page recall
Write the operations table (with the logic counterparts and Python operators) and prove one De Morgan law by double inclusion.

## 19. Revision summary
- Sets ignore order and duplicates. ∈ vs ⊆ is the classic trap.
- ∪ ∩ − complement ⊕ mirror ∨ ∧ "and not" ¬ ⊕.
- Prove identities by double inclusion or membership tables, not with pictures.
- $|\mathcal{P}(A)| = 2^{|A|}$ and $|A\times B| = |A||B|$.

## 20. Links
Prev: [[DM-05 Direct Proof, Contrapositive and Contradiction]] · Next: [[DM-07 Functions]] · Applied: [[PY-11 Dictionaries, Sets and Comprehensions]], [[PY-22 SQL and Database Integration]], [[CS-04 Authorization and Access Control]], [[X-01 Logic and Sets in Python and Requirements]]

## 21. Sources
- Rosen (2019), §2.1–2.2 "Sets" and "Set Operations".
- Levin, *Discrete Mathematics: An Open Introduction*, §0.3 (sets): https://discrete.openmathbooks.org/
- Python docs, *Set Types*: https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

## 22. Mastery checklist
- [ ] ∈/⊆ questions all correct (practice 2)
- [ ] Double-inclusion proofs written for practice 5 and 7(b)
- [ ] Induction proof of $2^n$ subsets (practice 9) · reviews scheduled
