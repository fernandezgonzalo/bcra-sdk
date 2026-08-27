import pytest
from unittest.mock import MagicMock
from typing import Any

import httpx

from bcra_sdk.exceptions import BCRAHTTPError


def test_get_entidades(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {"codigoEntidad": 11, "denominacion": "BANCO DE LA NACION ARGENTINA"},
            {
                "codigoEntidad": 7,
                "denominacion": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.cheques._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.cheques.get_entidades()

    assert len(data.entidades) == 2
    assert data.entidades[0].codigoEntidad == 11
    assert data.entidades[0].denominacion == "BANCO DE LA NACION ARGENTINA"
    assert data.entidades[1].codigoEntidad == 7
    assert data.entidades[1].denominacion == "BANCO DE GALICIA Y BUENOS AIRES S.A."


def test_get_entidades_vacio(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.cheques._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.cheques.get_entidades()

    assert data.entidades == []


def test_get_entidades_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Error al consultar Maestros."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.cheques._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.cheques.get_entidades()
    assert exc_info.value.status_code == 500
