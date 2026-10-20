"""A minimal in-process event bus (Observer pattern). Publishers don't know their subscribers."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Event:
    name: str            # e.g. "booking.confirmed"
    booking_id: int
    user_id: str
    detail: str = ""


Handler = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self.errors: list[tuple[str, Exception]] = []

    def subscribe(self, name: str, handler: Handler) -> None:
        self._handlers[name].append(handler)

    def publish(self, event: Event) -> None:
        # One failing subscriber must not break the booking or the other subscribers.
        for handler in self._handlers[event.name] + self._handlers["*"]:
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001 - deliberately isolating subscribers
                self.errors.append((getattr(handler, "__name__", repr(handler)), exc))


class Outbox:
    """Test-friendly subscriber that records notification messages instead of sending email."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def __call__(self, event: Event) -> None:
        self.messages.append(f"to {event.user_id}: {event.name} #{event.booking_id} {event.detail}".rstrip())


class AuditLog:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def __call__(self, event: Event) -> None:
        self.lines.append(f"{event.name} booking={event.booking_id} user={event.user_id}")
