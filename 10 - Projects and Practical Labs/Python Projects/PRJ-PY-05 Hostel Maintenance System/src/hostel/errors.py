"""Exception hierarchy: callers catch HostelError, or a specific subclass."""


class HostelError(Exception):
    """Base class for every error this package raises on purpose."""


class ValidationError(HostelError):
    """Input failed a validation rule."""


class NotFoundError(HostelError):
    """A room, user or request does not exist."""


class PermissionDenied(HostelError):
    """The actor's role or relationship to the request does not allow the action."""


class TransitionError(HostelError):
    """The requested status change is not allowed from the current status."""


class ConcurrentUpdateError(HostelError):
    """The request changed after it was read; reload and retry."""


class AuthError(HostelError):
    """Authentication failed. The message is deliberately generic."""


class ThrottledError(AuthError):
    """Too many failed logins; retry after `retry_after` seconds."""

    def __init__(self, retry_after: int) -> None:
        super().__init__(f"too many attempts; retry in {retry_after} s")
        self.retry_after = retry_after
