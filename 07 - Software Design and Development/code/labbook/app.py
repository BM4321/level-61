"""Composition root (factory): the one place that chooses concrete implementations."""
from __future__ import annotations

from .domain import Role, User, Workstation
from .events import AuditLog, EventBus, Outbox
from .repository import InMemoryBookingRepository, SqliteBookingRepository
from .service import BookingService, Directory


def demo_directory() -> Directory:
    users = [User("u-amina", "Amina", Role.STUDENT), User("u-baraka", "Baraka", Role.STUDENT),
             User("u-drm", "Dr Mushi", Role.LECTURER), User("u-juma", "Juma", Role.TECHNICIAN)]
    stations = [Workstation("LAB1-01", "LAB1"), Workstation("LAB1-02", "LAB1"),
                Workstation("LAB2-GPU1", "LAB2", has_gpu=True), Workstation("LAB1-03", "LAB1", in_service=False)]
    return Directory({u.user_id: u for u in users}, {w.ws_id: w for w in stations})


def create_app(storage: str = "memory", path: str = ":memory:"):
    """Return (service, outbox, audit) wired together. storage: 'memory' or 'sqlite'."""
    repo = InMemoryBookingRepository() if storage == "memory" else SqliteBookingRepository(path)
    bus, outbox, audit = EventBus(), Outbox(), AuditLog()
    bus.subscribe("booking.confirmed", outbox)
    bus.subscribe("booking.cancelled", outbox)
    bus.subscribe("*", audit)
    return BookingService(repo, demo_directory(), bus), outbox, audit
