"""PY-15 reference solutions (exceptions and defensive programming)."""
import json
import time
from pathlib import Path


class BankError(Exception):
    """Base class for banking domain errors."""


class InsufficientFundsError(BankError):
    """Raised when a withdrawal exceeds the balance."""

    def __init__(self, balance: int, amount: int):
        super().__init__(f"cannot withdraw {amount}; balance is {balance}")
        self.balance = balance
        self.amount = amount


class ConfigError(Exception):
    """Raised when a configuration file is present but invalid."""


def safe_divide(a: float, b: float) -> float | None:
    """a / b, or None if b == 0; other errors (e.g. TypeError) propagate."""
    try:
        return a / b
    except ZeroDivisionError:
        return None


def parse_int_or_default(text, default: int = 0) -> int:
    """int(text), or default if text is not a valid integer (or not a str/number)."""
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


def read_int(prompt: str, attempts: int = 3, input_fn=input) -> int:
    """Ask up to `attempts` times; ValueError('too many invalid attempts') after that."""
    for remaining in range(attempts, 0, -1):
        text = input_fn(prompt)
        try:
            return int(text)
        except ValueError:
            print(f"{text!r} is not a whole number ({remaining - 1} tries left)")
    raise ValueError("too many invalid attempts")


def withdraw(balance: int, amount: int) -> int:
    """New balance; ValueError if amount <= 0; InsufficientFundsError if amount > balance."""
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


def load_config(path: Path) -> dict:
    """{} if the file is missing; ConfigError (chained) if it is not valid JSON."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path} is not valid JSON (line {exc.lineno})") from exc


def retry(func, attempts: int = 3, delay: float = 0.5,
          retry_on: tuple = (TimeoutError, ConnectionError), sleep=time.sleep):
    """Call func(); on a retry_on error wait delay*2**(i-1) and retry; re-raise the last error."""
    for i in range(1, attempts + 1):
        try:
            return func()
        except retry_on:
            if i == attempts:
                raise
            sleep(delay * 2 ** (i - 1))
    raise ValueError("attempts must be >= 1")


def process_batch(items: list, handler) -> tuple[list, list[tuple[int, Exception]]]:
    """Apply handler to each item; collect (index, exception) failures and continue."""
    results, failures = [], []
    for i, item in enumerate(items):
        try:
            results.append(handler(item))
        except Exception as exc:
            failures.append((i, exc))
    return results, failures
