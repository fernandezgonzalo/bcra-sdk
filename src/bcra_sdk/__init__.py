from importlib.metadata import PackageNotFoundError, version

from ._retry import RetryPolicy
from .client import BCRAClient
from .exceptions import (
    BCRAConnectionError,
    BCRAEndpointVersionError,
    BCRAError,
    BCRAHTTPError,
    BCRATimeoutError,
)

try:
    __version__ = version("bcra-sdk")
except PackageNotFoundError:
    __version__ = "0.0.0.dev"

__all__ = [
    "BCRAClient",
    "BCRAConnectionError",
    "BCRAEndpointVersionError",
    "BCRAError",
    "BCRAHTTPError",
    "BCRATimeoutError",
    "RetryPolicy",
]
