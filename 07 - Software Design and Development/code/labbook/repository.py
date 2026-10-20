"""Persistence behind an interface (Repository pattern, Dependency Inversion).

The service depends on the `BookingRepository` protocol; tests use the in-memory version and
production can use SQLite (or anything else) without changing the service.
"""
from __future__ import annotations

import sqlite3
import threading
from datetime import datetime
from typing import Protocol

from .domain import ACTIVE, Booking, BookingStatus, TimeSlot
from .errors import NotFound, RuleViolation

_ACTIVE_VALUES = tuple(s.value for s in ACTIVE)


class BookingRepository(Protocol):
    def add(self, booking: Booking) -> Booking: ...
    def get(self, booking_id: int) -> Booking: ...
    def save(self, booking: Booking) -> None: ...
    def for_workstation(self, ws_id: str) -> list[Booking]: ...
    def for_user(self, user_id: str) -> list[Booking]: ...


class InMemoryBookingRepository:
    def __init__(self) -> None:
        self._rows: dict[int, Booking] = {}
        self._next = 1
        self._lock = threading.Lock()

    def add(self, booking: Booking) -> Booking:
        """Atomically re-check overlap and insert (the guarantee behind FR-02 under concurrency)."""
        with self._lock:
            if booking.active and any(b.active and b.ws_id == booking.ws_id and b.slot.overlaps(booking.slot)
                                      for b in self._rows.values()):
                raise RuleViolation("no-overlap", f"{booking.ws_id} was booked by someone else just now")
            booking.booking_id = self._next
            self._rows[self._next] = booking
            self._next += 1
        return booking

    def get(self, booking_id: int) -> Booking:
        try:
            return self._rows[booking_id]
        except KeyError:
            raise NotFound(f"booking {booking_id}") from None

    def save(self, booking: Booking) -> None:
        if booking.booking_id is None:
            raise NotFound("booking has not been added yet")
        self.get(booking.booking_id)          # must exist
        self._rows[booking.booking_id] = booking

    def for_workstation(self, ws_id: str) -> list[Booking]:
        return [b for b in self._rows.values() if b.ws_id == ws_id]

    def for_user(self, user_id: str) -> list[Booking]:
        return [b for b in self._rows.values() if b.user_id == user_id]


class SqliteBookingRepository:
    SCHEMA = """
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    TEXT NOT NULL,
        ws_id      TEXT NOT NULL,
        start_at   TEXT NOT NULL,
        end_at     TEXT NOT NULL,
        status     TEXT NOT NULL CHECK (status IN
                   ('requested','confirmed','checked_in','completed','cancelled','no_show')),
        CHECK (end_at > start_at)
    );
    CREATE INDEX IF NOT EXISTS ix_bookings_ws ON bookings (ws_id, start_at);
    """

    def __init__(self, path: str = ":memory:", timeout: float = 5.0) -> None:
        # isolation_level=None: we control transactions explicitly (BEGIN IMMEDIATE below).
        self.conn = sqlite3.connect(path, timeout=timeout, isolation_level=None, check_same_thread=False)
        self.conn.executescript(self.SCHEMA)

    @staticmethod
    def _row_to_booking(row) -> Booking:
        bid, user_id, ws_id, start, end, status = row
        return Booking(bid, user_id, ws_id, TimeSlot(datetime.fromisoformat(start), datetime.fromisoformat(end)),
                       BookingStatus(status))

    def add(self, booking: Booking) -> Booking:
        """Check-and-insert in ONE write transaction, so concurrent writers cannot both pass the check.

        BEGIN IMMEDIATE takes SQLite's write lock up front; a second writer waits (up to `timeout`)
        and then sees the first writer's committed row.
        """
        start, end = booking.slot.start.isoformat(), booking.slot.end.isoformat()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if booking.active:
                clash = self.conn.execute(
                    f"SELECT 1 FROM bookings WHERE ws_id = ? AND status IN ({','.join('?' * len(_ACTIVE_VALUES))})"
                    " AND start_at < ? AND end_at > ? LIMIT 1",
                    (booking.ws_id, *_ACTIVE_VALUES, end, start)).fetchone()
                if clash:
                    raise RuleViolation("no-overlap", f"{booking.ws_id} was booked by someone else just now")
            cur = self.conn.execute(
                "INSERT INTO bookings (user_id, ws_id, start_at, end_at, status) VALUES (?,?,?,?,?)",
                (booking.user_id, booking.ws_id, start, end, booking.status.value))
            self.conn.execute("COMMIT")
        except BaseException:
            self.conn.execute("ROLLBACK")
            raise
        booking.booking_id = cur.lastrowid
        return booking

    def get(self, booking_id: int) -> Booking:
        row = self.conn.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
        if row is None:
            raise NotFound(f"booking {booking_id}")
        return self._row_to_booking(row)

    def save(self, booking: Booking) -> None:
        cur = self.conn.execute("UPDATE bookings SET status = ? WHERE booking_id = ?",   # autocommit
                                (booking.status.value, booking.booking_id))
        if cur.rowcount == 0:
            raise NotFound(f"booking {booking.booking_id}")

    def for_workstation(self, ws_id: str) -> list[Booking]:
        rows = self.conn.execute("SELECT * FROM bookings WHERE ws_id = ? ORDER BY start_at", (ws_id,))
        return [self._row_to_booking(r) for r in rows]

    def for_user(self, user_id: str) -> list[Booking]:
        rows = self.conn.execute("SELECT * FROM bookings WHERE user_id = ? ORDER BY start_at", (user_id,))
        return [self._row_to_booking(r) for r in rows]
