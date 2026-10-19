"""Runnable, tested versions of code shown in the Cyber Security lessons (ITT06102).

Defensive teaching code. Standard library only (Python 3.10+).
"""
import hashlib
import hmac
import struct
import time

# ---------------------------------------------------------------- CS-03 HOTP / TOTP


def hotp(key: bytes, counter: int, digits: int = 6) -> str:
    """RFC 4226 HOTP with HMAC-SHA1 and dynamic truncation."""
    mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = mac[-1] & 0x0F
    code = (int.from_bytes(mac[offset:offset + 4], "big") & 0x7FFFFFFF) % 10 ** digits
    return str(code).zfill(digits)


def totp(key: bytes, at: float | None = None, step: int = 30, digits: int = 6) -> str:
    """RFC 6238 TOTP (T0 = 0)."""
    t = time.time() if at is None else at
    return hotp(key, int(t // step), digits)


def verify_totp(key: bytes, code: str, at: float, window: int = 1, step: int = 30) -> bool:
    """Accept codes within +-window time steps, compared in constant time."""
    return any(hmac.compare_digest(hotp(key, int(at // step) + d, len(code)), code)
               for d in range(-window, window + 1))


# ---------------------------------------------------------------- CS-04 RBAC + object-level checks
PERMISSIONS = {
    "student": {"view_own_requests"},
    "technician": {"view_assigned_requests", "update_status"},
    "warden": {"view_all_requests", "assign_technician", "close_request"},
}


class Forbidden(Exception):
    pass


def authorize(user: dict, action: str, req: dict | None = None) -> None:
    """Deny by default; raise Forbidden unless the role and object rules allow the action."""
    perms = PERMISSIONS.get(user.get("role"), set())
    if action == "view_request":
        if "view_all_requests" in perms:
            return
        if "view_own_requests" in perms and req and req["reporter"] == user["id"]:
            return
        if "view_assigned_requests" in perms and req and req.get("technician") == user["id"]:
            return
    elif action in perms:
        if action == "update_status" and (not req or req.get("technician") != user["id"]):
            raise Forbidden("not your assigned job")
        return
    raise Forbidden(f"{user.get('id')} may not {action}")
