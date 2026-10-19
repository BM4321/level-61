"""PY15 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py15.py
"""

import json
import time
from pathlib import Path

class BankError(Exception):
    """Base class for banking domain errors."""

class InsufficientFundsError(BankError):
    """Raised when a withdrawal exceeds the balance."""

    def __init__(self, balance: int, amount: int):
        super().__init__(f'cannot withdraw {amount}; balance is {balance}')
        self.balance = balance
        self.amount = amount

class ConfigError(Exception):
    """Raised when a configuration file is present but invalid."""

def safe_divide(a: float, b: float) -> float | None:
    """a / b, or None if b == 0; other errors (e.g. TypeError) propagate."""
    raise NotImplementedError

def parse_int_or_default(text, default: int=0) -> int:
    """int(text), or default if text is not a valid integer (or not a str/number)."""
    raise NotImplementedError

def read_int(prompt: str, attempts: int=3, input_fn=input) -> int:
    """Ask up to `attempts` times; ValueError('too many invalid attempts') after that."""
    raise NotImplementedError

def withdraw(balance: int, amount: int) -> int:
    """New balance; ValueError if amount <= 0; InsufficientFundsError if amount > balance."""
    raise NotImplementedError

def load_config(path: Path) -> dict:
    """{} if the file is missing; ConfigError (chained) if it is not valid JSON."""
    raise NotImplementedError

def retry(func, attempts: int=3, delay: float=0.5, retry_on: tuple=(TimeoutError, ConnectionError), sleep=time.sleep):
    """Call func(); on a retry_on error wait delay*2**(i-1) and retry; re-raise the last error."""
    raise NotImplementedError

def process_batch(items: list, handler) -> tuple[list, list[tuple[int, Exception]]]:
    """Apply handler to each item; collect (index, exception) failures and continue."""
    raise NotImplementedError
