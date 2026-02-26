class Trading212Error(Exception):
    """Base exception for all Trading 212 API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(Trading212Error):
    """Raised on HTTP 401 — bad API key."""


class ForbiddenError(Trading212Error):
    """Raised on HTTP 403 — missing scope or permission."""


class NotFoundError(Trading212Error):
    """Raised on HTTP 404 — resource not found."""


class ValidationError(Trading212Error):
    """Raised on HTTP 400 — bad request / failed validation."""


class RateLimitError(Trading212Error):
    """Raised on HTTP 429 — rate limit exceeded."""


class TimeoutError(Trading212Error):
    """Raised on HTTP 408 — request timed out."""


class ServerError(Trading212Error):
    """Raised on HTTP 5xx — server-side error."""
