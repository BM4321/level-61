"""PY09 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py09.py
"""

def count_vowels(text: str) -> int:
    """Number of a/e/i/o/u characters, case-insensitive."""
    raise NotImplementedError

def normalise(s: str) -> str:
    """Collapse whitespace runs to single spaces, trim, casefold."""
    raise NotImplementedError

def acronym(phrase: str) -> str:
    """'portable network graphics' -> 'PNG'."""
    raise NotImplementedError

def is_palindrome_sentence(s: str) -> bool:
    """Palindrome ignoring case and non-alphanumeric characters."""
    raise NotImplementedError

def caesar_shift(text: str, k: int) -> str:
    """Shift ASCII letters by k (wrapping); other characters unchanged. TOY CIPHER ONLY."""
    raise NotImplementedError

def is_palindrome_two_pointer(s: str) -> bool:
    """Same as is_palindrome_sentence but O(1) extra space."""
    raise NotImplementedError

def are_anagrams(a: str, b: str) -> bool:
    """Anagram test ignoring whitespace and case (counting algorithm)."""
    raise NotImplementedError

def parse_settings(line: str) -> dict[str, str]:
    """'host=db1; port=5432' -> dict; ValueError if a part lacks '='."""
    raise NotImplementedError

def mask(number: str, visible: int=4) -> str:
    """Mask all but the last `visible` digits (spaces removed)."""
    raise NotImplementedError

def word_wrap(text: str, width: int) -> list[str]:
    """Greedy wrap at spaces; long words get their own line; ValueError if width < 1."""
    raise NotImplementedError

def vigenere(text: str, key: str, decrypt: bool=False) -> str:
    """Vigenere cipher over ASCII letters (TOY CIPHER ONLY)."""
    raise NotImplementedError
