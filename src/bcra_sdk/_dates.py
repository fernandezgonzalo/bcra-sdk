from __future__ import annotations

from datetime import date, datetime


def _coerce_date(value: str | date) -> str:
    """Normaliza una fecha (str ISO o date) a ``YYYY-MM-DD``."""
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise ValueError(
            f"Fecha inválida: {value!r}. Usá el formato ISO 8601 (YYYY-MM-DD)."
        ) from None
