"""Domain layer: entities, the request lifecycle and validation rules. No I/O here."""
from __future__ import annotations

import enum
import re
from dataclasses import dataclass
from datetime import datetime, timedelta

from .errors import ValidationError


class Role(str, enum.Enum):
    RESIDENT = "resident"
    WARDEN = "warden"
    TECHNICIAN = "technician"


class Status(str, enum.Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    REOPENED = "reopened"


class Priority(str, enum.Enum):
    URGENT = "urgent"
    NORMAL = "normal"
    LOW = "low"


# The state machine from SD-08 section 10, as data. Terminal states map to an empty set.
ALLOWED: dict[Status, frozenset[Status]] = {
    Status.NEW: frozenset({Status.ASSIGNED, Status.REJECTED}),
    Status.ASSIGNED: frozenset({Status.IN_PROGRESS}),
    Status.IN_PROGRESS: frozenset({Status.RESOLVED}),
    Status.RESOLVED: frozenset({Status.CLOSED, Status.REOPENED}),
    Status.REOPENED: frozenset({Status.ASSIGNED}),
    Status.CLOSED: frozenset(),
    Status.REJECTED: frozenset(),
}

# Which role may move a request INTO each status.
ACTOR_FOR: dict[Status, Role] = {
    Status.ASSIGNED: Role.WARDEN,
    Status.REJECTED: Role.WARDEN,
    Status.CLOSED: Role.WARDEN,
    Status.IN_PROGRESS: Role.TECHNICIAN,
    Status.RESOLVED: Role.TECHNICIAN,
    Status.REOPENED: Role.RESIDENT,
}

OPEN_STATUSES = frozenset({Status.NEW, Status.ASSIGNED, Status.IN_PROGRESS, Status.REOPENED})
REOPEN_WINDOW = timedelta(days=7)

# Default priority by category; a warden can change it.
CATEGORIES: dict[str, Priority] = {
    "electrical": Priority.URGENT,
    "plumbing": Priority.NORMAL,
    "structural": Priority.NORMAL,
    "furniture": Priority.LOW,
    "other": Priority.NORMAL,
}

_ROOM = re.compile(r"[A-Z]-\d{3}")
_REG = re.compile(r"[A-Z0-9/]{5,20}")


def validate_room_code(code: str) -> str:
    code = code.strip().upper()
    if not _ROOM.fullmatch(code):
        raise ValidationError("room code must look like A-101")
    return code


def validate_reg_no(reg_no: str) -> str:
    reg_no = reg_no.strip().upper()
    if not _REG.fullmatch(reg_no):
        raise ValidationError("registration number: 5-20 characters, A-Z, 0-9 or '/'")
    return reg_no


def validate_description(text: str) -> str:
    text = " ".join(text.split())          # collapses newlines and tabs, so log lines can't be forged
    if not 10 <= len(text) <= 1000:
        raise ValidationError("description must be 10-1000 characters")
    if not text.isprintable():
        raise ValidationError("description contains control characters")
    return text


def validate_category(category: str) -> str:
    category = category.strip().lower()
    if category not in CATEGORIES:
        raise ValidationError(f"category must be one of {sorted(CATEGORIES)}")
    return category


@dataclass(frozen=True)
class Room:
    code: str
    block: str
    capacity: int


@dataclass(frozen=True)
class User:
    reg_no: str
    name: str
    role: Role
    room_code: str | None
    password_hash: str


@dataclass(frozen=True)
class Request:
    id: int
    room_code: str
    reporter: str
    category: str
    description: str
    priority: Priority
    status: Status
    created_at: datetime
    assignee: str | None = None
    resolved_at: datetime | None = None


@dataclass(frozen=True)
class HistoryEntry:
    request_id: int
    old_status: Status | None
    new_status: Status
    actor: str
    at: datetime
    note: str = ""
