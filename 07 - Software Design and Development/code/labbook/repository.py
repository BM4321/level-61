"""Persistence behind an interface (Repository pattern, Dependency Inversion).

The service depends on the `BookingRepository` protocol; tests use the in-memory version and
production can use SQLite (or anything else) without changing the service.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Protocol

from .domain import Booking, BookingStatus, TimeSlot
from .errors import NotFound


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

    def add(self, booking: Booking) -> Booking:
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

    def __init__(self, path: str = ":memory:") -> None:
        self.conn = sqlite3.connect(path)
        self.conn.executescript(self.SCHEMA)

    @staticmethod
    def _row_to_booking(row) -> Booking:
        bid, user_id, ws_id, start, end, status = row
        return Booking(bid, user_id, ws_id, TimeSlot(datetime.fromisoformat(start), datetime.fromisoformat(end)),
                       BookingStatus(status))

    def add(self, booking: Booking) -> Booking:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO bookings (user_id, ws_id, start_at, end_at, status) VALUES (?,?,?,?,?)",
                (booking.user_id, booking.ws_id, booking.slot.start.isoformat(), booking.slot.end.isoformat(),
                 booking.status.value))
        booking.booking_id = cur.lastrowid
        return booking

    def get(self, booking_id: int) -> Booking:
        row = self.conn.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
        if row is None:
            raise NotFound(f"booking {booking_id}")
        return self._row_to_booking(row)

    def save(self, booking: Booking) -> None:
        with self.conn:
            cur = self.conn.execute("UPDATE bookings SET status = ? WHERE booking_id = ?",
                                    (booking.status.value, booking.booking_id))
        if cur.rowcount == 0:
            raise NotFound(f"booking {booking.booking_id}")

    def for_workstation(self, ws_id: str) -> list[Booking]:
        rows = self.conn.execute("SELECT * FROM bookings WHERE ws_id = ? ORDER BY start_at", (ws_id,))
        return [self._row_to_booking(r) for r in rows]

    def for_user(self, user_id: str) -> list[Booking]:
        rows = self.conn.execute("SELECT * FROM bookings WHERE user_id = ? ORDER BY start_at", (user_id,))
        return [self._row_to_booking(r) for r in rows]
