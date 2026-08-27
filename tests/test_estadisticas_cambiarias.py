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


def test_get_cotizaciones_sin_fecha(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "fecha": "2024-06-12",
            "detalle": [
                {
                    "codigoMoneda": "ARS",
                    "descripcion": "PESO",
                    "tipoPase": 0.02289900,
                    "tipoCotizacion": 0.00000000,
                },
                {
                    "codigoMoneda": "AUD",
                    "descripcion": "DOLAR AUSTRALIANO",
                    "tipoPase": 0.69320000,
                    "tipoCotizacion": 30.27204400,
                },
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    data = client.estadisticas_cambiarias.get_cotizaciones()

    mock_request.assert_called_once_with(
        "GET", "/estadisticascambiarias/v1.0/Cotizaciones", params=None
    )
    assert data.fecha == "2024-06-12"
    assert len(data.detalle) == 2
    assert data.detalle[0].codigoMoneda == "ARS"
    assert data.detalle[0].descripcion == "PESO"
    assert data.detalle[0].tipoPase == 0.02289900
    assert data.detalle[0].tipoCotizacion == 0.0
    assert data.detalle[1].codigoMoneda == "AUD"
    assert data.detalle[1].tipoCotizacion == 30.27204400


def test_get_cotizaciones_con_fecha(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "fecha": "2024-06-12",
            "detalle": [
                {
                    "codigoMoneda": "ARS",
                    "descripcion": "PESO",
                    "tipoPase": 0.02289900,
                    "tipoCotizacion": 0.0,
                }
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    data = client.estadisticas_cambiarias.get_cotizaciones(fecha="2024-06-12")

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones",
        params={"fecha": "2024-06-12"},
    )
    assert data.fecha == "2024-06-12"


def test_get_cotizaciones_vacio(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "fecha": None,
            "detalle": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.estadisticas_cambiarias.get_cotizaciones()

    assert data.fecha is None
    assert data.detalle == []


def test_get_cotizaciones_400(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 400,
        "errorMessages": [
            "Parámetro erróneo: La fecha no puede ser mayor al día actual."
        ],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(400, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.estadisticas_cambiarias.get_cotizaciones(fecha="2024-12-31")
    assert exc_info.value.status_code == 400


def test_get_cotizaciones_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Error al consultar Cotizaciones."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.estadisticas_cambiarias.get_cotizaciones()
    assert exc_info.value.status_code == 500
