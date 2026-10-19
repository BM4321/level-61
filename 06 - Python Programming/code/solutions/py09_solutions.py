"""PY-09 reference solutions (strings)."""


def count_vowels(text: str) -> int:
    """Number of a/e/i/o/u characters, case-insensitive."""
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count


def normalise(s: str) -> str:
    """Collapse whitespace runs to single spaces, trim, casefold."""
    return " ".join(s.split()).casefold()


def acronym(phrase: str) -> str:
    """'portable network graphics' -> 'PNG'."""
    return "".join(word[0].upper() for word in phrase.split())


def is_palindrome_sentence(s: str) -> bool:
    """Palindrome ignoring case and non-alphanumeric characters."""
    letters = [ch.casefold() for ch in s if ch.isalnum()]
    return letters == letters[::-1]


def caesar_shift(text: str, k: int) -> str:
    """Shift ASCII letters by k (wrapping); other characters unchanged. TOY CIPHER ONLY."""
    out = []
    for ch in text:
        if "a" <= ch <= "z":
            out.append(chr((ord(ch) - ord("a") + k) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            out.append(chr((ord(ch) - ord("A") + k) % 26 + ord("A")))
        else:
            out.append(ch)
    return "".join(out)


def is_palindrome_two_pointer(s: str) -> bool:
    """Same as is_palindrome_sentence but O(1) extra space."""
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():
            i += 1
        elif not s[j].isalnum():
            j -= 1
        elif s[i].casefold() != s[j].casefold():
            return False
        else:
            i += 1
            j -= 1
    return True


def are_anagrams(a: str, b: str) -> bool:
    """Anagram test ignoring whitespace and case (counting algorithm)."""
    def clean(s: str) -> list[str]:
        return [c for c in s.casefold() if not c.isspace()]

    ca, cb = clean(a), clean(b)
    if len(ca) != len(cb):
        return False
    counts: dict[str, int] = {}
    for c in ca:
        counts[c] = counts.get(c, 0) + 1
    for c in cb:
        if counts.get(c, 0) == 0:
            return False
        counts[c] -= 1
    return True


def parse_settings(line: str) -> dict[str, str]:
    """'host=db1; port=5432' -> dict; ValueError if a part lacks '='."""
    result = {}
    for part in line.split(";"):
        part = part.strip()
        if not part:
            continue
        key, sep, value = part.partition("=")
        if not sep:
            raise ValueError(f"missing '=' in {part!r}")
        result[key.strip()] = value.strip()
    return result


def mask(number: str, visible: int = 4) -> str:
    """Mask all but the last `visible` digits (spaces removed)."""
    digits = number.replace(" ", "")
    return "*" * (len(digits) - visible) + digits[-visible:]


def word_wrap(text: str, width: int) -> list[str]:
    """Greedy wrap at spaces; long words get their own line; ValueError if width < 1."""
    if width < 1:
        raise ValueError("width must be >= 1")
    lines: list[str] = []
    current = ""
    for word in text.split():
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def vigenere(text: str, key: str, decrypt: bool = False) -> str:
    """Vigenere cipher over ASCII letters (TOY CIPHER ONLY)."""
    out, k = [], 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key[k % len(key)].upper()) - ord("A")
            if decrypt:
                shift = -shift
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            k += 1
        else:
            out.append(ch)
    return "".join(out)
