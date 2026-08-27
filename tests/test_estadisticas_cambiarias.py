from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest

from bcra_sdk.exceptions import BCRAHTTPError


def test_get_divisas(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {"codigo": "ARS", "denominacion": "PESO"},
            {"codigo": "USD", "denominacion": "DOLAR E.E.U.U."},
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.estadisticas_cambiarias.get_divisas()

    assert len(data.divisas) == 2
    assert data.divisas[0].codigo == "ARS"
    assert data.divisas[0].denominacion == "PESO"
    assert data.divisas[1].codigo == "USD"
    assert data.divisas[1].denominacion == "DOLAR E.E.U.U."


def test_get_divisas_vacio(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.estadisticas_cambiarias.get_divisas()

    assert data.divisas == []


def test_get_divisas_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Error al consultar Divisas."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.estadisticas_cambiarias.get_divisas()
    assert exc_info.value.status_code == 500
