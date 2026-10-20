"""Service layer: the use cases. Depends on the repository interface, never on SQLite directly."""
from __future__ import annotations

import logging
import math
import secrets
from collections.abc import Callable
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from .errors import AuthError, NotFoundError, PermissionDenied, ThrottledError, TransitionError, ValidationError
from .models import (ACTOR_FOR, ALLOWED, CATEGORIES, OPEN_STATUSES, REOPEN_WINDOW, HistoryEntry, Priority, Request,
                     Role, Status, User, validate_category, validate_description, validate_reg_no,
                     validate_room_code)
from .repository import HostelRepository
from .security import PasswordHasher, new_reset_token, password_problems, token_hash

log = logging.getLogger(__name__)
Clock = Callable[[], datetime]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


FREE_ATTEMPTS = 3
BASE_DELAY_S = 30
MAX_DELAY_S = 900
RESET_TTL = timedelta(minutes=30)


def login_delay(failures: int) -> int:
    """Seconds to wait after `failures` consecutive failures: 0 for the first 3, then 30, 60, 120 ... capped at 900."""
    if failures < FREE_ATTEMPTS:
        return 0
    return min(BASE_DELAY_S * 2 ** (failures - FREE_ATTEMPTS), MAX_DELAY_S)


class AuthService:
    def __init__(self, repo: HostelRepository, hasher: PasswordHasher, clock: Clock = utc_now,
                 institution: str = "University X") -> None:
        self.repo, self.hasher, self.clock = repo, hasher, clock
        self.context_words = [institution, "hostel"]
        self._dummy_hash: str | None = None

    def register(self, reg_no: str, name: str, role: Role, password: str, room_code: str | None = None) -> User:
        reg_no = validate_reg_no(reg_no)
        name = " ".join(name.split())
        if not 2 <= len(name) <= 80:
            raise ValidationError("name must be 2-80 characters")
        if role is Role.RESIDENT:
            if room_code is None:
                raise ValidationError("residents need a room")
            room_code = self.repo.get_room(validate_room_code(room_code)).code
        elif room_code is not None:
            raise ValidationError("only residents have a room")
        problems = password_problems(password, self.context_words + [reg_no, *name.split()])
        if problems:
            raise ValidationError("; ".join(problems))
        user = User(reg_no, name, role, room_code, self.hasher.hash(password))
        self.repo.add_user(user)
        log.info("registered %s as %s", reg_no, role.value)
        return user

    def authenticate(self, reg_no: str, password: str) -> User:
        reg_no = reg_no.strip().upper()
        now = self.clock()
        failures, last = self.repo.login_state(reg_no)
        wait = login_delay(failures)
        if wait and last is not None and now < last + timedelta(seconds=wait):
            raise ThrottledError(math.ceil((last + timedelta(seconds=wait) - now).total_seconds()))
        try:
            user = self.repo.get_user(reg_no)
        except NotFoundError:
            if self._dummy_hash is None:
                self._dummy_hash = self.hasher.hash(secrets.token_urlsafe(16))
            self.hasher.verify(password, self._dummy_hash)        # similar timing for unknown accounts
            raise AuthError("invalid registration number or password") from None
        if not self.hasher.verify(password, user.password_hash):
            count = self.repo.record_login_failure(reg_no, now)
            log.warning("failed login for %s (%d consecutive)", reg_no, count)   # never log the password
            raise AuthError("invalid registration number or password")
        self.repo.clear_login_failures(reg_no)
        if self.hasher.needs_rehash(user.password_hash):
            self.repo.set_password_hash(reg_no, self.hasher.hash(password))
        return user

    def issue_reset(self, reg_no: str) -> str | None:
        """Return a token to send to the user's address on file, or None for unknown users.
        The caller must show the same message either way."""
        try:
            user = self.repo.get_user(reg_no.strip().upper())
        except NotFoundError:
            return None
        token, digest = new_reset_token()
        self.repo.add_reset_token(digest, user.reg_no, self.clock() + RESET_TTL)
        return token

    def reset_password(self, token: str, new_password: str) -> None:
        problems = password_problems(new_password, self.context_words)
        if problems:                                   # checked first, so a weak choice doesn't burn the token
            raise ValidationError("; ".join(problems))
        reg_no = self.repo.consume_reset_token(token_hash(token), self.clock())
        if reg_no is None:
            raise AuthError("invalid or expired reset token")
        self.repo.set_password_hash(reg_no, self.hasher.hash(new_password))
        self.repo.clear_login_failures(reg_no)
        log.info("password reset for %s", reg_no)


class RequestService:
    def __init__(self, repo: HostelRepository, clock: Clock = utc_now) -> None:
        self.repo, self.clock = repo, clock

    def submit(self, actor: User, room_code: str, category: str, description: str) -> Request:
        room_code = validate_room_code(room_code)
        if actor.role is Role.TECHNICIAN:
            raise PermissionDenied("technicians don't submit requests")
        if actor.role is Role.RESIDENT and actor.room_code != room_code:
            raise PermissionDenied("residents report faults in their own room")
        self.repo.get_room(room_code)
        category = validate_category(category)
        request = Request(0, room_code, actor.reg_no, category, validate_description(description),
                          CATEGORIES[category], Status.NEW, self.clock())
        return self.repo.add_request(request, actor.reg_no)

    def transition(self, actor: User, request_id: int, new_status: Status, assignee: str | None = None,
                   note: str = "") -> Request:
        req = self.repo.get_request(request_id)
        if new_status not in ALLOWED[req.status]:
            raise TransitionError(f"{req.status.value} -> {new_status.value} is not allowed")
        if actor.role is not ACTOR_FOR[new_status]:
            raise PermissionDenied(f"only a {ACTOR_FOR[new_status].value} can set {new_status.value}")
        now = self.clock()
        changes: dict[str, object] = {"status": new_status}
        if new_status is Status.ASSIGNED:
            if assignee is None or self.repo.get_user(assignee).role is not Role.TECHNICIAN:
                raise ValidationError("assign to an existing technician")
            changes["assignee"] = assignee
        if new_status in (Status.IN_PROGRESS, Status.RESOLVED) and actor.reg_no != req.assignee:
            raise PermissionDenied("only the assigned technician can do this")
        if new_status is Status.RESOLVED:
            changes["resolved_at"] = now
        if new_status is Status.REOPENED:
            if actor.reg_no != req.reporter:
                raise PermissionDenied("only the reporter can reopen")
            if req.resolved_at is None or now - req.resolved_at > REOPEN_WINDOW:
                raise TransitionError("requests can be reopened within 7 days of resolution")
            changes["resolved_at"] = None
        updated = replace(req, **changes)  # type: ignore[arg-type]
        self.repo.save_change(updated, req.status,
                              HistoryEntry(req.id, req.status, new_status, actor.reg_no, now, _clean_note(note)))
        return updated

    def set_priority(self, actor: User, request_id: int, priority: Priority) -> Request:
        if actor.role is not Role.WARDEN:
            raise PermissionDenied("only wardens set priority")
        req = self.repo.get_request(request_id)
        if req.status not in OPEN_STATUSES:
            raise TransitionError("priority can only change while a request is open")
        updated = replace(req, priority=priority)
        self.repo.save_change(updated, req.status, HistoryEntry(
            req.id, req.status, req.status, actor.reg_no, self.clock(),
            f"priority {req.priority.value} -> {priority.value}"))
        return updated

    def visible_to(self, actor: User) -> list[Request]:
        if actor.role is Role.RESIDENT:
            return self.repo.list_requests(reporter=actor.reg_no)
        if actor.role is Role.TECHNICIAN:
            return self.repo.list_requests(assignee=actor.reg_no)
        return self.repo.list_requests()

    def history(self, actor: User, request_id: int) -> list[HistoryEntry]:
        req = self.repo.get_request(request_id)
        if actor.role is not Role.WARDEN and actor.reg_no not in (req.reporter, req.assignee):
            raise PermissionDenied("not your request")
        return self.repo.history(request_id)


def _clean_note(note: str) -> str:
    note = " ".join(note.split())
    if len(note) > 500 or not note.isprintable():
        raise ValidationError("note: at most 500 printable characters")
    return note
