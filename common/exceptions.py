"""Exceptions which is common to all Apps."""


class BadRequest(Exception):
    """Request method is invalid."""

    def __init__(self, message):
        """Initial values."""
        self.message = message
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class UnauthorizedAccess(Exception):
    """user Authorization failed."""

    def __init__(self, message):
        """Initial values."""
        self.message = message
        self.status_code = 401

    def __str__(self):
        """Object returning."""
        return self.message


class AccessForbidden(Exception):
    """User is not allowed to access."""

    def __init__(self, message):
        """Initial values."""
        self.message = message
        self.status_code = 403

    def __str__(self):
        """Object returning."""
        return self.message


class Conflict(Exception):
    """Conflict occurred."""

    def __init__(self, message):
        """Initial values."""
        self.message = message
        self.status_code = 409

    def __str__(self):
        """Object returning."""
        return self.message


class NotFound(Exception):
    """NotFound occurred."""

    def __init__(self, message):
        """Initial values."""
        self.message = message
        self.status_code = 404

    def __str__(self):
        """Object returning."""
        return self.message
