"""Application service: coordinates a use case. Business rules live in domain/rules, not here."""
from __future__ import annotations

from dataclasses import dataclass, field

from .domain import Booking, BookingStatus, Role, TimeSlot, User, Workstation
from .errors import NotFound, PermissionDenied
from .events import Event, EventBus
from .repository import BookingRepository
from .rules import BookingRule, default_rules


@dataclass
class Directory:
    """Read-only lookup of users and workstations (kept simple for the case study)."""

    users: dict[str, User] = field(default_factory=dict)
    workstations: dict[str, Workstation] = field(default_factory=dict)

    def user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise NotFound(f"user {user_id}")
        return self.users[user_id]

    def workstation(self, ws_id: str) -> Workstation:
        if ws_id not in self.workstations:
            raise NotFound(f"workstation {ws_id}")
        return self.workstations[ws_id]


class BookingService:
    def __init__(self, repo: BookingRepository, directory: Directory, bus: EventBus,
                 rules: BookingRule | None = None, auto_confirm: bool = True):
        self.repo, self.directory, self.bus = repo, directory, bus
        self.rules = rules or default_rules()
        self.auto_confirm = auto_confirm

    # Use case UC-01: Book a workstation
    def book(self, user_id: str, ws_id: str, slot: TimeSlot) -> Booking:
        user, ws = self.directory.user(user_id), self.directory.workstation(ws_id)
        booking = Booking(None, user_id, ws_id, slot)
        existing = self.repo.for_workstation(ws_id) + self.repo.for_user(user_id)
        self.rules.check(booking, user, ws, existing)
        if self.auto_confirm:
            booking.transition(BookingStatus.CONFIRMED)
        self.repo.add(booking)
        assert booking.booking_id is not None   # assigned by the repository
        self.bus.publish(Event(f"booking.{booking.status.value}", booking.booking_id, user_id,
                               f"{ws_id} {slot.start:%Y-%m-%d %H:%M}-{slot.end:%H:%M}"))
        return booking

    # Use case UC-02: Cancel a booking
    def cancel(self, actor_id: str, booking_id: int) -> Booking:
        actor, booking = self.directory.user(actor_id), self.repo.get(booking_id)
        if actor.user_id != booking.user_id and actor.role is not Role.TECHNICIAN:
            raise PermissionDenied("only the booker or a technician may cancel")
        booking.transition(BookingStatus.CANCELLED)
        self.repo.save(booking)
        self.bus.publish(Event("booking.cancelled", booking_id, booking.user_id, f"by {actor_id}"))
        return booking

    # Use case UC-03: Check in
    def check_in(self, user_id: str, booking_id: int) -> Booking:
        booking = self.repo.get(booking_id)
        if booking.user_id != user_id:
            raise PermissionDenied("only the booker may check in")
        booking.transition(BookingStatus.CHECKED_IN)
        self.repo.save(booking)
        self.bus.publish(Event("booking.checked_in", booking_id, user_id))
        return booking

    def my_bookings(self, user_id: str) -> list[Booking]:
        return sorted(self.repo.for_user(user_id), key=lambda b: b.slot.start)
