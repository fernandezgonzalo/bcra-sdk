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
    """Política de reintentos ante errores transitorios.

    ``max_retries`` es la cantidad de reintentos; con ``0`` el retry queda
    desactivado. La espera entre intentos crece de forma exponencial
    (``backoff * 2**n``), salvo que el servidor indique ``Retry-After``.

    Args:
        max_retries: Cantidad máxima de reintentos.
        backoff: Base (en segundos) para el backoff exponencial.
        retry_on_timeout: Si también reintentar peticiones que exceden el
            timeout configurado.
        statuses: Códigos HTTP considerados transitorios y reintentables.
    """

    max_retries: int = 2
    backoff: float = 0.5
    retry_on_timeout: bool = True
    statuses: tuple[int, ...] = _RETRYABLE_STATUSES

    def delay(self, attempt: int) -> float:
        """Espera en segundos antes del intento ``attempt``."""
        return self.backoff * (2**attempt)
