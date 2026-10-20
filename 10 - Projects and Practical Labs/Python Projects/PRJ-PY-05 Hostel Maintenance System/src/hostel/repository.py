"""Persistence layer: one interface, two implementations (in-memory for tests, SQLite for use)."""
from __future__ import annotations

import logging
import sqlite3
import threading
from abc import ABC, abstractmethod
from dataclasses import replace
from datetime import datetime

from .errors import ConcurrentUpdateError, NotFoundError, ValidationError
from .models import HistoryEntry, Priority, Request, Role, Room, Status, User

log = logging.getLogger(__name__)


class HostelRepository(ABC):
    """add/get/list per entity, plus the two operations that must be atomic:
    save_change (update + history row) and consume_reset_token (single use)."""

    @abstractmethod
    def add_room(self, room: Room) -> None: ...
    @abstractmethod
    def get_room(self, code: str) -> Room: ...
    @abstractmethod
    def list_rooms(self) -> list[Room]: ...

    @abstractmethod
    def add_user(self, user: User) -> None: ...
    @abstractmethod
    def get_user(self, reg_no: str) -> User: ...
    @abstractmethod
    def list_users(self, role: Role | None = None) -> list[User]: ...
    @abstractmethod
    def set_password_hash(self, reg_no: str, password_hash: str) -> None: ...
    @abstractmethod
    def login_state(self, reg_no: str) -> tuple[int, datetime | None]: ...
    @abstractmethod
    def record_login_failure(self, reg_no: str, at: datetime) -> int: ...
    @abstractmethod
    def clear_login_failures(self, reg_no: str) -> None: ...

    @abstractmethod
    def add_request(self, request: Request, actor: str) -> Request: ...
    @abstractmethod
    def get_request(self, request_id: int) -> Request: ...
    @abstractmethod
    def list_requests(self, reporter: str | None = None, assignee: str | None = None) -> list[Request]: ...
    @abstractmethod
    def save_change(self, updated: Request, expected_status: Status, entry: HistoryEntry) -> None: ...
    @abstractmethod
    def history(self, request_id: int) -> list[HistoryEntry]: ...

    @abstractmethod
    def add_reset_token(self, token_hash: str, reg_no: str, expires_at: datetime) -> None: ...
    @abstractmethod
    def consume_reset_token(self, token_hash: str, now: datetime) -> str | None: ...


class InMemoryRepository(HostelRepository):
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._rooms: dict[str, Room] = {}
        self._users: dict[str, User] = {}
        self._failures: dict[str, tuple[int, datetime | None]] = {}
        self._requests: dict[int, Request] = {}
        self._history: list[HistoryEntry] = []
        self._tokens: dict[str, tuple[str, datetime, bool]] = {}

    def add_room(self, room: Room) -> None:
        with self._lock:
            if room.code in self._rooms:
                raise ValidationError(f"room {room.code} exists")
            self._rooms[room.code] = room

    def get_room(self, code: str) -> Room:
        try:
            return self._rooms[code]
        except KeyError:
            raise NotFoundError(f"room {code}") from None

    def list_rooms(self) -> list[Room]:
        return sorted(self._rooms.values(), key=lambda r: r.code)

    def add_user(self, user: User) -> None:
        with self._lock:
            if user.reg_no in self._users:
                raise ValidationError(f"user {user.reg_no} exists")
            self._users[user.reg_no] = user

    def get_user(self, reg_no: str) -> User:
        try:
            return self._users[reg_no]
        except KeyError:
            raise NotFoundError(f"user {reg_no}") from None

    def list_users(self, role: Role | None = None) -> list[User]:
        return sorted((u for u in self._users.values() if role is None or u.role == role), key=lambda u: u.reg_no)

    def set_password_hash(self, reg_no: str, password_hash: str) -> None:
        with self._lock:
            self._users[reg_no] = replace(self.get_user(reg_no), password_hash=password_hash)

    def login_state(self, reg_no: str) -> tuple[int, datetime | None]:
        return self._failures.get(reg_no, (0, None))

    def record_login_failure(self, reg_no: str, at: datetime) -> int:
        with self._lock:
            count = self._failures.get(reg_no, (0, None))[0] + 1
            self._failures[reg_no] = (count, at)
            return count

    def clear_login_failures(self, reg_no: str) -> None:
        with self._lock:
            self._failures.pop(reg_no, None)

    def add_request(self, request: Request, actor: str) -> Request:
        with self._lock:
            stored = replace(request, id=max(self._requests, default=0) + 1)
            self._requests[stored.id] = stored
            self._history.append(HistoryEntry(stored.id, None, stored.status, actor, stored.created_at, "submitted"))
            return stored

    def get_request(self, request_id: int) -> Request:
        try:
            return self._requests[request_id]
        except KeyError:
            raise NotFoundError(f"request {request_id}") from None

    def list_requests(self, reporter: str | None = None, assignee: str | None = None) -> list[Request]:
        return [r for _, r in sorted(self._requests.items())
                if (reporter is None or r.reporter == reporter) and (assignee is None or r.assignee == assignee)]

    def save_change(self, updated: Request, expected_status: Status, entry: HistoryEntry) -> None:
        with self._lock:
            if self.get_request(updated.id).status != expected_status:
                raise ConcurrentUpdateError(f"request {updated.id} changed; reload")
            self._requests[updated.id] = updated
            self._history.append(entry)

    def history(self, request_id: int) -> list[HistoryEntry]:
        return [h for h in self._history if h.request_id == request_id]

    def add_reset_token(self, token_hash: str, reg_no: str, expires_at: datetime) -> None:
        with self._lock:
            self._tokens[token_hash] = (reg_no, expires_at, False)

    def consume_reset_token(self, token_hash: str, now: datetime) -> str | None:
        with self._lock:
            row = self._tokens.get(token_hash)
            if row is None or row[2] or now > row[1]:
                return None
            self._tokens[token_hash] = (row[0], row[1], True)
            return row[0]


SCHEMA = """
CREATE TABLE IF NOT EXISTS rooms (
    code TEXT PRIMARY KEY, block TEXT NOT NULL, capacity INTEGER NOT NULL CHECK (capacity > 0));
CREATE TABLE IF NOT EXISTS users (
    reg_no TEXT PRIMARY KEY, name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('resident', 'warden', 'technician')),
    room_code TEXT REFERENCES rooms(code), password_hash TEXT NOT NULL,
    failed_logins INTEGER NOT NULL DEFAULT 0, last_failed_at TEXT);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT, room_code TEXT NOT NULL REFERENCES rooms(code),
    reporter TEXT NOT NULL REFERENCES users(reg_no), category TEXT NOT NULL, description TEXT NOT NULL,
    priority TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL,
    assignee TEXT REFERENCES users(reg_no), resolved_at TEXT);
CREATE TABLE IF NOT EXISTS status_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INTEGER NOT NULL REFERENCES requests(id),
    old_status TEXT, new_status TEXT NOT NULL, actor TEXT NOT NULL, at TEXT NOT NULL, note TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS reset_tokens (
    token_hash TEXT PRIMARY KEY, reg_no TEXT NOT NULL REFERENCES users(reg_no),
    expires_at TEXT NOT NULL, used INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS ix_requests_reporter ON requests(reporter);
CREATE INDEX IF NOT EXISTS ix_requests_assignee ON requests(assignee);
CREATE INDEX IF NOT EXISTS ix_history_request ON status_history(request_id);
"""


def _dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


class SqliteRepository(HostelRepository):
    """Every query is parameterised. Multi-statement changes run in one transaction."""

    def __init__(self, path: str) -> None:
        self._conn = sqlite3.connect(path, isolation_level=None, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(SCHEMA)

    def close(self) -> None:
        self._conn.close()

    def _tx(self) -> "_Transaction":
        return _Transaction(self._conn)

    def _one(self, sql: str, params: tuple, what: str) -> sqlite3.Row:
        row = self._conn.execute(sql, params).fetchone()
        if row is None:
            raise NotFoundError(what)
        return row

    def add_room(self, room: Room) -> None:
        try:
            with self._tx():
                self._conn.execute("INSERT INTO rooms VALUES (?, ?, ?)", (room.code, room.block, room.capacity))
        except sqlite3.IntegrityError as exc:
            raise ValidationError(f"room {room.code}: {exc}") from None

    def get_room(self, code: str) -> Room:
        row = self._one("SELECT * FROM rooms WHERE code = ?", (code,), f"room {code}")
        return Room(row["code"], row["block"], row["capacity"])

    def list_rooms(self) -> list[Room]:
        return [Room(r["code"], r["block"], r["capacity"])
                for r in self._conn.execute("SELECT * FROM rooms ORDER BY code")]

    @staticmethod
    def _user(row: sqlite3.Row) -> User:
        return User(row["reg_no"], row["name"], Role(row["role"]), row["room_code"], row["password_hash"])

    def add_user(self, user: User) -> None:
        try:
            with self._tx():
                self._conn.execute(
                    "INSERT INTO users (reg_no, name, role, room_code, password_hash) VALUES (?, ?, ?, ?, ?)",
                    (user.reg_no, user.name, user.role.value, user.room_code, user.password_hash))
        except sqlite3.IntegrityError as exc:
            raise ValidationError(f"user {user.reg_no}: {exc}") from None

    def get_user(self, reg_no: str) -> User:
        return self._user(self._one("SELECT * FROM users WHERE reg_no = ?", (reg_no,), f"user {reg_no}"))

    def list_users(self, role: Role | None = None) -> list[User]:
        if role is None:
            rows = self._conn.execute("SELECT * FROM users ORDER BY reg_no")
        else:
            rows = self._conn.execute("SELECT * FROM users WHERE role = ? ORDER BY reg_no", (role.value,))
        return [self._user(r) for r in rows]

    def set_password_hash(self, reg_no: str, password_hash: str) -> None:
        with self._tx():
            self._conn.execute("UPDATE users SET password_hash = ? WHERE reg_no = ?", (password_hash, reg_no))

    def login_state(self, reg_no: str) -> tuple[int, datetime | None]:
        row = self._conn.execute("SELECT failed_logins, last_failed_at FROM users WHERE reg_no = ?",
                                 (reg_no,)).fetchone()
        return (0, None) if row is None else (row["failed_logins"], _dt(row["last_failed_at"]))

    def record_login_failure(self, reg_no: str, at: datetime) -> int:
        with self._tx():
            self._conn.execute("UPDATE users SET failed_logins = failed_logins + 1, last_failed_at = ? "
                               "WHERE reg_no = ?", (at.isoformat(), reg_no))
            row = self._conn.execute("SELECT failed_logins FROM users WHERE reg_no = ?", (reg_no,)).fetchone()
        return 0 if row is None else row[0]

    def clear_login_failures(self, reg_no: str) -> None:
        with self._tx():
            self._conn.execute("UPDATE users SET failed_logins = 0, last_failed_at = NULL WHERE reg_no = ?",
                               (reg_no,))

    @staticmethod
    def _request(row: sqlite3.Row) -> Request:
        return Request(row["id"], row["room_code"], row["reporter"], row["category"], row["description"],
                       Priority(row["priority"]), Status(row["status"]), datetime.fromisoformat(row["created_at"]),
                       row["assignee"], _dt(row["resolved_at"]))

    def _insert_history(self, e: HistoryEntry) -> None:
        self._conn.execute(
            "INSERT INTO status_history (request_id, old_status, new_status, actor, at, note) VALUES (?, ?, ?, ?, ?, ?)",
            (e.request_id, e.old_status.value if e.old_status else None, e.new_status.value, e.actor,
             e.at.isoformat(), e.note))

    def add_request(self, request: Request, actor: str) -> Request:
        with self._tx():
            cur = self._conn.execute(
                "INSERT INTO requests (room_code, reporter, category, description, priority, status, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (request.room_code, request.reporter, request.category, request.description,
                 request.priority.value, request.status.value, request.created_at.isoformat()))
            stored = replace(request, id=int(cur.lastrowid or 0))
            self._insert_history(HistoryEntry(stored.id, None, stored.status, actor, stored.created_at, "submitted"))
        return stored

    def get_request(self, request_id: int) -> Request:
        return self._request(self._one("SELECT * FROM requests WHERE id = ?", (request_id,),
                                       f"request {request_id}"))

    def list_requests(self, reporter: str | None = None, assignee: str | None = None) -> list[Request]:
        rows = self._conn.execute(
            "SELECT * FROM requests WHERE (? IS NULL OR reporter = ?) AND (? IS NULL OR assignee = ?) ORDER BY id",
            (reporter, reporter, assignee, assignee))
        return [self._request(r) for r in rows]

    def save_change(self, updated: Request, expected_status: Status, entry: HistoryEntry) -> None:
        with self._tx():
            cur = self._conn.execute(
                "UPDATE requests SET priority = ?, status = ?, assignee = ?, resolved_at = ? "
                "WHERE id = ? AND status = ?",          # optimistic check: fails if someone changed it first
                (updated.priority.value, updated.status.value, updated.assignee,
                 updated.resolved_at.isoformat() if updated.resolved_at else None, updated.id, expected_status.value))
            if cur.rowcount != 1:
                raise ConcurrentUpdateError(f"request {updated.id} changed; reload")
            self._insert_history(entry)
        log.info("request %s: %s -> %s by %s", updated.id, expected_status.value, updated.status.value, entry.actor)

    def history(self, request_id: int) -> list[HistoryEntry]:
        rows = self._conn.execute("SELECT * FROM status_history WHERE request_id = ? ORDER BY id", (request_id,))
        return [HistoryEntry(r["request_id"], Status(r["old_status"]) if r["old_status"] else None,
                             Status(r["new_status"]), r["actor"], datetime.fromisoformat(r["at"]), r["note"])
                for r in rows]

    def add_reset_token(self, token_hash: str, reg_no: str, expires_at: datetime) -> None:
        with self._tx():
            self._conn.execute("INSERT INTO reset_tokens (token_hash, reg_no, expires_at) VALUES (?, ?, ?)",
                               (token_hash, reg_no, expires_at.isoformat()))

    def consume_reset_token(self, token_hash: str, now: datetime) -> str | None:
        with self._tx():
            row = self._conn.execute("SELECT reg_no, expires_at FROM reset_tokens WHERE token_hash = ? AND used = 0",
                                     (token_hash,)).fetchone()
            if row is None or now > datetime.fromisoformat(row["expires_at"]):
                return None
            self._conn.execute("UPDATE reset_tokens SET used = 1 WHERE token_hash = ?", (token_hash,))
        return row["reg_no"]


class _Transaction:
    """BEGIN IMMEDIATE ... COMMIT, or ROLLBACK on any exception."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def __enter__(self) -> None:
        self._conn.execute("BEGIN IMMEDIATE")

    def __exit__(self, exc_type, exc, tb) -> None:
        self._conn.execute("COMMIT" if exc_type is None else "ROLLBACK")
