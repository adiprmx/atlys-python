"""Typed exceptions for the Atlys API client."""


class AtlysError(Exception):
    """Base error for all Atlys API failures."""

    def __init__(self, message, code=None, request_id=None, status=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.request_id = request_id
        self.status = status

    def __str__(self):
        parts = []
        if self.code:
            parts.append("[%s]" % self.code)
        parts.append(self.message)
        if self.request_id:
            parts.append("(request_id=%s)" % self.request_id)
        return " ".join(parts)


class AuthError(AtlysError):
    """Raised on HTTP 401 — missing or invalid API key."""


class NotFoundError(AtlysError):
    """Raised on HTTP 404 — unknown endpoint or resource."""


class ValidationError(AtlysError):
    """Raised on HTTP 400/422 — bad parameters."""


class RateLimitError(AtlysError):
    """Raised on HTTP 429 — quota exhausted.

    Carries ``retry_after`` (seconds) taken from the ``retry-after``
    response header when the server provides one.
    """

    def __init__(self, message, code=None, request_id=None, status=None,
                 retry_after=None):
        super().__init__(message, code=code, request_id=request_id,
                         status=status)
        self.retry_after = retry_after


class ServerError(AtlysError):
    """Raised on HTTP 5xx — the API itself failed."""


def raise_for_response(status, payload, headers):
    """Map an error payload to the right exception type and raise it."""
    err = (payload or {}).get("error") or {}
    meta = (payload or {}).get("meta") or {}
    code = err.get("code")
    message = err.get("message") or ("HTTP %s" % status)
    request_id = meta.get("request_id")

    if status == 401:
        raise AuthError(message, code=code, request_id=request_id,
                        status=status)
    if status == 404:
        raise NotFoundError(message, code=code, request_id=request_id,
                            status=status)
    if status in (400, 422):
        raise ValidationError(message, code=code, request_id=request_id,
                              status=status)
    if status == 429:
        retry_after = None
        raw = None
        try:
            raw = headers.get("retry-after") or headers.get("Retry-After")
        except Exception:
            raw = None
        if raw is not None:
            try:
                retry_after = int(str(raw).split(",")[0].strip())
            except (ValueError, TypeError):
                retry_after = None
        raise RateLimitError(message, code=code, request_id=request_id,
                             status=status, retry_after=retry_after)
    if status and 500 <= status < 600:
        raise ServerError(message, code=code, request_id=request_id,
                          status=status)
    raise AtlysError(message, code=code, request_id=request_id, status=status)
