"""Domain model: entities, value objects and the booking state machine. No I/O here."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from .errors import InvalidTransition, ValidationError


class Role(Enum):
    STUDENT = "student"
    LECTURER = "lecturer"
    TECHNICIAN = "technician"


@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    role: Role


@dataclass(frozen=True)
class TimeSlot:
    """A value object: immutable, compared by value, validated on creation."""

    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValidationError("slot must end after it starts")
        if (self.end - self.start) > timedelta(hours=8):
            raise ValidationError("slot longer than 8 hours")

    @property
    def hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600

    def overlaps(self, other: TimeSlot) -> bool:
        """Half-open intervals [start, end): touching slots do not overlap."""
        return self.start < other.end and other.start < self.end


@dataclass(frozen=True)
class Workstation:
    ws_id: str
    lab_id: str
    has_gpu: bool = False
    in_service: bool = True


class BookingStatus(Enum):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


ALLOWED = {
    BookingStatus.REQUESTED: {BookingStatus.CONFIRMED, BookingStatus.CANCELLED},
    BookingStatus.CONFIRMED: {BookingStatus.CHECKED_IN, BookingStatus.CANCELLED, BookingStatus.NO_SHOW},
    BookingStatus.CHECKED_IN: {BookingStatus.COMPLETED},
    BookingStatus.COMPLETED: set(),
    BookingStatus.CANCELLED: set(),
    BookingStatus.NO_SHOW: set(),
}
ACTIVE = {BookingStatus.REQUESTED, BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN}


@dataclass
class Booking:
    """An entity: identity (booking_id) matters, state changes over time."""

    booking_id: int | None
    user_id: str
    ws_id: str
    slot: TimeSlot
    status: BookingStatus = BookingStatus.REQUESTED
    history: list[tuple[BookingStatus, BookingStatus]] = field(default_factory=list)

    def transition(self, new: BookingStatus) -> None:
        if new not in ALLOWED[self.status]:
            raise InvalidTransition(f"{self.status.value} -> {new.value} not allowed")
        self.history.append((self.status, new))
        self.status = new

    @property
    def active(self) -> bool:
        return self.status in ACTIVE
