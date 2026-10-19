"""Atlys — Python SDK for the Atlys API.

https://api.atlys.my.id — ~100,000 Indonesian public-data endpoints.
"""

from .client import Atlys
from .errors import (AtlysError, AuthError, NotFoundError, RateLimitError,
                     ServerError, ValidationError)

__version__ = "0.1.0"
__all__ = [
    "Atlys",
    "AtlysError",
    "AuthError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "__version__",
]
