"""Domain-specific exceptions. Callers catch these instead of generic errors."""


class LabBookError(Exception):
    """Base class for all LabBook errors."""


class ValidationError(LabBookError):
    """Input is malformed (wrong type, out of range)."""


class RuleViolation(LabBookError):
    """A booking breaks a business rule (overlap, quota, opening hours)."""

    def __init__(self, rule: str, message: str):
        super().__init__(f"{rule}: {message}")
        self.rule = rule


class InvalidTransition(LabBookError):
    """A booking cannot move from its current state to the requested one."""


class NotFound(LabBookError):
    """A requested entity does not exist."""


class PermissionDenied(LabBookError):
    """The acting user may not perform this operation."""
