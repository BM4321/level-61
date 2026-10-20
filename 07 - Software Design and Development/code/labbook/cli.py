"""Thin command-line adapter. It parses input and formats output; all decisions are in the service."""
from __future__ import annotations

import argparse
from datetime import datetime

from .app import create_app
from .domain import TimeSlot
from .errors import LabBookError


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="labbook", description="LabBook demo (in-memory)")
    p.add_argument("--user", required=True)
    p.add_argument("--ws", required=True)
    p.add_argument("--start", required=True, help="YYYY-MM-DDTHH:MM")
    p.add_argument("--end", required=True, help="YYYY-MM-DDTHH:MM")
    a = p.parse_args(argv)
    service, outbox, _audit = create_app()
    try:
        b = service.book(a.user, a.ws, TimeSlot(datetime.fromisoformat(a.start), datetime.fromisoformat(a.end)))
    except (LabBookError, ValueError) as exc:
        print(f"error: {exc}")
        return 1
    print(f"booking #{b.booking_id} {b.status.value}")
    for m in outbox.messages:
        print("notify", m)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
