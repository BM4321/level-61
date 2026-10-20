"""Behavioural patterns around LabBook: Observer (waiting list), Command (undo), State (class-per-state)."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Protocol

from labbook.domain import Booking, TimeSlot
from labbook.errors import InvalidTransition, LabBookError
from labbook.events import Event
from labbook.repository import BookingRepository
from labbook.service import BookingService


# ------------------------------------------------------------------ OBSERVER: waiting list reacts to cancellations
class WaitingList:
    """Subscribes to 'booking.cancelled'. Offers the freed slot to the first waiting user (FIFO)."""

    def __init__(self, repo: BookingRepository):
        self.repo = repo
        self.queues: dict[tuple, deque[str]] = defaultdict(deque)
        self.offers: list[tuple[str, str, TimeSlot]] = []

    def join(self, user_id: str, ws_id: str, slot: TimeSlot) -> int:
        q = self.queues[(ws_id, slot)]
        if user_id not in q:
            q.append(user_id)
        return list(q).index(user_id) + 1          # position in queue

    def __call__(self, event: Event) -> None:
        booking = self.repo.get(event.booking_id)
        q = self.queues.get((booking.ws_id, booking.slot))
        if q:
            self.offers.append((q.popleft(), booking.ws_id, booking.slot))


# ------------------------------------------------------------------ COMMAND: encapsulate requests, support undo
class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...


@dataclass
class BookCommand:
    service: BookingService
    user_id: str
    ws_id: str
    slot: TimeSlot
    booking: Booking | None = None

    def execute(self) -> None:
        self.booking = self.service.book(self.user_id, self.ws_id, self.slot)

    def undo(self) -> None:
        if self.booking is not None and self.booking.booking_id is not None:
            self.service.cancel(self.user_id, self.booking.booking_id)


@dataclass
class CommandHistory:
    done: list[Command] = field(default_factory=list)

    def run(self, cmd: Command) -> None:
        cmd.execute()                    # if it raises, nothing is recorded
        self.done.append(cmd)

    def undo_last(self) -> None:
        if not self.done:
            raise LabBookError("nothing to undo")
        self.done.pop().undo()


# ------------------------------------------------------------------ STATE: class-per-state alternative to ALLOWED table
class TicketState(Protocol):
    name: str

    def assign(self, ticket: RepairTicket, tech: str) -> None: ...
    def start(self, ticket: RepairTicket) -> None: ...
    def resolve(self, ticket: RepairTicket, note: str) -> None: ...


class _Base:
    name = "base"

    def assign(self, ticket, tech):
        raise InvalidTransition(f"cannot assign when {self.name}")

    def start(self, ticket):
        raise InvalidTransition(f"cannot start when {self.name}")

    def resolve(self, ticket, note):
        raise InvalidTransition(f"cannot resolve when {self.name}")


class Open(_Base):
    name = "open"

    def assign(self, ticket, tech):
        ticket.technician = tech
        ticket.state = Assigned()


class Assigned(_Base):
    name = "assigned"

    def assign(self, ticket, tech):          # re-assignment allowed while not started
        ticket.technician = tech

    def start(self, ticket):
        ticket.state = InProgress()


class InProgress(_Base):
    name = "in_progress"

    def resolve(self, ticket, note):
        if not note.strip():
            raise InvalidTransition("a resolution note is required")
        ticket.resolution = note
        ticket.state = Resolved()


class Resolved(_Base):
    name = "resolved"


@dataclass
class RepairTicket:
    """Workstation repair ticket (technician workflow). Behaviour is delegated to the current state object."""

    ws_id: str
    state: TicketState = field(default_factory=Open)
    technician: str | None = None
    resolution: str = ""

    def assign(self, tech: str) -> None:
        self.state.assign(self, tech)

    def start(self) -> None:
        self.state.start(self)

    def resolve(self, note: str) -> None:
        self.state.resolve(self, note)
