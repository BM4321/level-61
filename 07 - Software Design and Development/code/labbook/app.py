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


def create_app_from_env(env: dict[str, str] | None = None):
    """Twelve-factor style configuration: storage choice and path come from the environment.

    LABBOOK_STORAGE = memory | sqlite   (default: memory)
    LABBOOK_DB      = path to the SQLite file (required when LABBOOK_STORAGE=sqlite)
    """
    import os

    env = dict(os.environ) if env is None else env
    storage = env.get("LABBOOK_STORAGE", "memory")
    if storage not in ("memory", "sqlite"):
        raise ValueError(f"LABBOOK_STORAGE must be 'memory' or 'sqlite', not {storage!r}")
    if storage == "sqlite" and not env.get("LABBOOK_DB"):
        raise ValueError("LABBOOK_DB is required when LABBOOK_STORAGE=sqlite")
    return create_app(storage, env.get("LABBOOK_DB", ":memory:"))


def health(service) -> dict[str, str]:
    """Readiness probe: can we reach storage? Used by deployment tooling and monitoring."""
    try:
        service.repo.for_user("__healthcheck__")
        return {"status": "ok", "storage": type(service.repo).__name__}
    except Exception as exc:  # noqa: BLE001 - report any storage failure
        return {"status": "error", "detail": type(exc).__name__}
