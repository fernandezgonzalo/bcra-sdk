from __future__ import annotations

import email.utils
from dataclasses import dataclass
from datetime import UTC, datetime

import httpx

_RETRYABLE_STATUSES: tuple[int, ...] = (429, 500, 502, 503, 504)


def _retry_after_seconds(resp: httpx.Response | None) -> float | None:
    if resp is None:
        return None
    value = resp.headers.get("Retry-After")
    if value is None:
        return None
    value = value.strip()
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        parsed = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    delay = (parsed - datetime.now(UTC)).total_seconds()
    return max(0.0, delay)


@dataclass(frozen=True)
class RetryPolicy:
    """Politica de reintentos para errores transitorios.

    ``max_retries`` es la cantidad de reintentos (0 desactiva el retry).
    El espera entre intentos crece de forma exponencial (``backoff * 2**n``)
    salvo que el servidor indique ``Retry-After``.
    """

    max_retries: int = 2
    backoff: float = 0.5
    retry_on_timeout: bool = True
    statuses: tuple[int, ...] = _RETRYABLE_STATUSES

    def delay(self, attempt: int) -> float:
        return self.backoff * (2**attempt)
