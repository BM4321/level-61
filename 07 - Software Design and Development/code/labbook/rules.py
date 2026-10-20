"""Booking rules as interchangeable strategies (Strategy + Composite patterns, Open/Closed principle).

To add a rule, write a new class with a `check` method; existing rules and the service do not change.
"""
from __future__ import annotations

from datetime import time, timedelta
from typing import Iterable, Protocol

from .domain import Booking, Role, User, Workstation
from .errors import RuleViolation


class BookingRule(Protocol):
    name: str

    def check(self, booking: Booking, user: User, ws: Workstation, existing: Iterable[Booking]) -> None:
        """Raise RuleViolation if the booking is not allowed."""


class NoOverlap:
    name = "no-overlap"

    def check(self, booking, user, ws, existing):
        for other in existing:
            if other.active and other.ws_id == booking.ws_id and other.slot.overlaps(booking.slot):
                raise RuleViolation(self.name, f"{ws.ws_id} already booked {other.slot.start:%H:%M}-{other.slot.end:%H:%M}")


class OpeningHours:
    name = "opening-hours"

    def __init__(self, opens: time = time(7, 0), closes: time = time(22, 0)):
        self.opens, self.closes = opens, closes

    def check(self, booking, user, ws, existing):
        s, e = booking.slot.start, booking.slot.end
        if s.date() != e.date() or s.time() < self.opens or e.time() > self.closes:
            raise RuleViolation(self.name, f"labs open {self.opens:%H:%M}-{self.closes:%H:%M} on a single day")


class WeeklyQuota:
    name = "weekly-quota"

    def __init__(self, max_hours: float = 10.0, applies_to: Role = Role.STUDENT):
        self.max_hours, self.applies_to = max_hours, applies_to

    def check(self, booking, user, ws, existing):
        if user.role is not self.applies_to:
            return
        week_start = booking.slot.start - timedelta(days=booking.slot.start.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=7)
        used = sum(b.slot.hours for b in existing
                   if b.active and b.user_id == user.user_id and week_start <= b.slot.start < week_end)
        if used + booking.slot.hours > self.max_hours:
            raise RuleViolation(self.name, f"{used + booking.slot.hours:g} h exceeds {self.max_hours:g} h per week")


class WorkstationInService:
    name = "in-service"

    def check(self, booking, user, ws, existing):
        if not ws.in_service:
            raise RuleViolation(self.name, f"{ws.ws_id} is out of service")


class GpuForLecturersAndApprovedOnly:
    """Example of a rule added later without touching the service (open/closed)."""

    name = "gpu-access"

    def __init__(self, approved_students: set[str] | None = None):
        self.approved = approved_students or set()

    def check(self, booking, user, ws, existing):
        if ws.has_gpu and user.role is Role.STUDENT and user.user_id not in self.approved:
            raise RuleViolation(self.name, "GPU workstations need supervisor approval")


class RuleSet:
    """Composite: applies every rule; behaves like a single rule."""

    name = "all-rules"

    def __init__(self, rules: list[BookingRule]):
        self.rules = list(rules)

    def check(self, booking, user, ws, existing):
        existing = list(existing)
        for rule in self.rules:
            rule.check(booking, user, ws, existing)


def default_rules() -> RuleSet:
    return RuleSet([WorkstationInService(), OpeningHours(), NoOverlap(), WeeklyQuota()])
