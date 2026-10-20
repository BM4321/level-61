"""Command-line interface: parses arguments, authenticates, calls services, prints results.

Passwords are read with getpass when stdin is a terminal, otherwise one per line from stdin
(actor's password first), so that scripted tests never put secrets in argv or shell history.
"""
from __future__ import annotations

import argparse
import getpass
import json
import logging
import sys
from collections.abc import Callable
from typing import TextIO

from . import __version__
from .errors import HostelError
from .models import Priority, Role, Room, Status, User, validate_room_code
from .reports import summary
from .repository import SqliteRepository
from .security import PasswordHasher
from .services import AuthService, RequestService, utc_now

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hostel", description="Hostel maintenance requests")
    p.add_argument("--db", default="hostel.db", help="SQLite database file (default: hostel.db)")
    p.add_argument("--as", dest="actor", help="your registration number")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="create the database tables")
    r = sub.add_parser("add-room", help="(warden) add a room")
    r.add_argument("code"); r.add_argument("block"); r.add_argument("capacity", type=int)
    r = sub.add_parser("register", help="register a user (the first user must be a warden)")
    r.add_argument("reg_no"); r.add_argument("name"); r.add_argument("role", choices=[x.value for x in Role])
    r.add_argument("--room")
    r = sub.add_parser("submit", help="report a fault")
    r.add_argument("room"); r.add_argument("category"); r.add_argument("description")
    sub.add_parser("list", help="requests visible to you")
    r = sub.add_parser("move", help="change a request's status")
    r.add_argument("id", type=int); r.add_argument("status", choices=[x.value for x in Status])
    r.add_argument("--assignee"); r.add_argument("--note", default="")
    r = sub.add_parser("priority", help="(warden) change priority")
    r.add_argument("id", type=int); r.add_argument("priority", choices=[x.value for x in Priority])
    r = sub.add_parser("history", help="a request's audit trail")
    r.add_argument("id", type=int)
    sub.add_parser("report", help="(warden) summary report as JSON")
    return p


def _secret_reader(stdin: TextIO) -> Callable[[str], str]:
    def read(prompt: str) -> str:
        if stdin.isatty():
            return getpass.getpass(prompt)
        return stdin.readline().rstrip("\n")
    return read


def main(argv: list[str] | None = None, stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout,
         hasher: PasswordHasher | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    read_secret = _secret_reader(stdin)
    repo = SqliteRepository(args.db)
    auth = AuthService(repo, hasher or PasswordHasher(), utc_now)
    requests = RequestService(repo, utc_now)
    out = lambda text: print(text, file=stdout)  # noqa: E731

    def actor() -> User:
        if not args.actor:
            raise HostelError("this command needs --as REG_NO")
        return auth.authenticate(args.actor, read_secret(f"Password for {args.actor}: "))

    try:
        if args.command == "init":
            out(f"database ready: {args.db}")
        elif args.command == "add-room":
            if actor().role is not Role.WARDEN:
                raise HostelError("only wardens add rooms")
            repo.add_room(Room(validate_room_code(args.code), args.block.strip(), args.capacity))
            out(f"room {args.code.upper()} added")
        elif args.command == "register":
            first = not repo.list_users()
            if first and args.role != Role.WARDEN.value:
                raise HostelError("the first user must be a warden")
            if not first and actor().role is not Role.WARDEN:
                raise HostelError("only wardens register users")
            user = auth.register(args.reg_no, args.name, Role(args.role), read_secret("New user's password: "),
                                 args.room)
            out(f"registered {user.reg_no} ({user.role.value})")
        elif args.command == "submit":
            req = requests.submit(actor(), args.room, args.category, args.description)
            out(f"request {req.id} submitted ({req.priority.value})")
        elif args.command == "list":
            for r in requests.visible_to(actor()):
                out(f"{r.id:>4}  {r.status.value:<11} {r.priority.value:<6} {r.room_code}  {r.category:<10} "
                    f"{r.description[:40]}")
        elif args.command == "move":
            req = requests.transition(actor(), args.id, Status(args.status), args.assignee, args.note)
            out(f"request {req.id} is now {req.status.value}")
        elif args.command == "priority":
            req = requests.set_priority(actor(), args.id, Priority(args.priority))
            out(f"request {req.id} priority {req.priority.value}")
        elif args.command == "history":
            for h in requests.history(actor(), args.id):
                old = h.old_status.value if h.old_status else "-"
                out(f"{h.at.isoformat(timespec='seconds')}  {old} -> {h.new_status.value}  by {h.actor}  {h.note}")
        elif args.command == "report":
            if actor().role is not Role.WARDEN:
                raise HostelError("only wardens see reports")
            out(json.dumps(summary(repo.list_requests(), utc_now()), indent=2))
        return 0
    except HostelError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    finally:
        repo.close()


if __name__ == "__main__":
    raise SystemExit(main())
