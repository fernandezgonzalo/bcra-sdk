from datetime import UTC, date, datetime

import pytest

from bcra_sdk._dates import _coerce_date


def test_coerce_date_from_date():
    assert _coerce_date(date(2024, 6, 12)) == "2024-06-12"


def test_coerce_date_from_datetime_takes_date_part():
    value = datetime(2024, 6, 12, 15, 30, tzinfo=UTC)
    assert _coerce_date(value) == "2024-06-12"


def test_coerce_date_from_iso_string():
    assert _coerce_date("2024-06-12") == "2024-06-12"


def test_coerce_date_from_compact_iso_string():
    assert _coerce_date("20240612") == "2024-06-12"


def test_coerce_date_rejects_invalid_string():
    with pytest.raises(ValueError, match="Fecha inválida"):
        _coerce_date("12/06/2024")
