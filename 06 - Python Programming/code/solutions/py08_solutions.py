"""PY-08 reference solutions (algorithmic patterns)."""


def second_largest(marks: list[float]) -> float | None:
    """Second-highest DISTINCT value, or None."""
    first = second = None
    for m in marks:
        if first is None or m > first:
            second, first = first, m
        elif m < first and (second is None or m > second):
            second = m
    return second


def run_length_encode(s: str) -> str:
    """'aaabccdddd' -> 'a3b1c2d4'."""
    if not s:
        return ""
    parts = []
    current, count = s[0], 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            parts.append(f"{current}{count}")
            current, count = ch, 1
    parts.append(f"{current}{count}")
    return "".join(parts)


def run_length_decode(s: str) -> str:
    """'a12b1' -> 'aaaaaaaaaaaab' (counts may have several digits)."""
    out = []
    char, digits = None, ""
    for ch in s:
        if ch.isdigit():
            digits += ch
        else:
            if char is not None:
                out.append(char * int(digits))
            char, digits = ch, ""
    if char is not None:
        out.append(char * int(digits))
    return "".join(out)


def first_duplicate(xs: list):
    """First element seen a second time scanning left to right, else None."""
    seen = set()
    for x in xs:
        if x in seen:
            return x
        seen.add(x)
    return None


def merge_sorted(a: list, b: list) -> list:
    """Merge two sorted lists in O(len(a) + len(b))."""
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


def greedy_change(amount: int, coins: list[int]) -> list[int]:
    """Largest-coin-first change; ValueError if exact change impossible."""
    result = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            result.append(c)
    if amount != 0:
        raise ValueError("cannot make exact change")
    return result


def min_coins(amount: int, coins: list[int]) -> int | None:
    """Optimal coin count by dynamic programming, None if impossible."""
    inf = float("inf")
    best = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return None if best[amount] == inf else int(best[amount])


def to_binary(n: int) -> str:
    """Binary digits of n >= 0 via repeated division ('0' for n == 0)."""
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = str(n % 2) + result
        n //= 2
    return result
