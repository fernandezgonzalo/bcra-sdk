import asyncio
from datetime import date
from typing import Any
from unittest.mock import AsyncMock, MagicMock

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


def test_get_evolucion_moneda_basico(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [
            {
                "fecha": "2024-06-12",
                "detalle": [
                    {
                        "codigoMoneda": "EUR",
                        "descripcion": "EURO (UNIDAD MONETARIA EUROPE",
                        "tipoPase": 1.12940000,
                        "tipoCotizacion": 49.32089800,
                    }
                ],
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    data = client.estadisticas_cambiarias.get_evolucion_moneda(moneda="EUR")

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones/EUR",
        params=None,
    )
    assert data.resultset.count == 1
    assert data.resultset.offset == 0
    assert data.resultset.limit == 1000
    assert len(data.cotizaciones) == 1
    assert data.cotizaciones[0].fecha == "2024-06-12"
    assert data.cotizaciones[0].detalle[0].codigoMoneda == "EUR"
    assert data.cotizaciones[0].detalle[0].tipoCotizacion == 49.32089800


def test_get_evolucion_moneda_con_params(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 10, "limit": 100}},
        "results": [
            {
                "fecha": "2024-06-12",
                "detalle": [
                    {
                        "codigoMoneda": "EUR",
                        "descripcion": "EURO (UNIDAD MONETARIA EUROPE",
                        "tipoPase": 1.12940000,
                        "tipoCotizacion": 49.32089800,
                    }
                ],
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    data = client.estadisticas_cambiarias.get_evolucion_moneda(
        moneda="EUR",
        fechadesde="2024-06-12",
        fechahasta="2024-06-14",
        limit=100,
        offset=10,
    )

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones/EUR",
        params={
            "fechadesde": "2024-06-12",
            "fechahasta": "2024-06-14",
            "limit": 100,
            "offset": 10,
        },
    )
    assert data.resultset.limit == 100
    assert data.resultset.offset == 10


def test_get_evolucion_moneda_vacio(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 0, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.estadisticas_cambiarias.get_evolucion_moneda(moneda="EUR")

    assert data.resultset.count == 0
    assert data.cotizaciones == []


def test_get_evolucion_moneda_400(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 400,
        "errorMessages": [
            "Parámetro erróneo: La fecha desde no puede ser mayor a la fecha hasta."
        ],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(400, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.estadisticas_cambiarias.get_evolucion_moneda(
            moneda="EUR", fechadesde="2024-06-14", fechahasta="2024-06-12"
        )
    assert exc_info.value.status_code == 400


def test_get_evolucion_moneda_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Error al consultar Evolución."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.estadisticas_cambiarias.get_evolucion_moneda(moneda="EUR")
    assert exc_info.value.status_code == 500


def test_aget_divisas(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {"codigo": "ARS", "denominacion": "PESO"},
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "arequest",
        AsyncMock(return_value=mock_response),
    )

    async def run():
        return await client.estadisticas_cambiarias.aget_divisas()

    data = asyncio.run(run())

    assert len(data.divisas) == 1
    assert data.divisas[0].codigo == "ARS"


def test_aget_cotizaciones(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "fecha": "2024-06-12",
            "detalle": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.estadisticas_cambiarias._t, "arequest", mock_arequest)

    async def run():
        return await client.estadisticas_cambiarias.aget_cotizaciones(
            fecha="2024-06-12"
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones",
        params={"fecha": "2024-06-12"},
    )
    assert data.fecha == "2024-06-12"
    assert data.detalle == []


def test_aget_evolucion_moneda(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [
            {
                "fecha": "2024-06-12",
                "detalle": [
                    {
                        "codigoMoneda": "EUR",
                        "descripcion": "EURO (UNIDAD MONETARIA EUROPE",
                        "tipoPase": 1.12940000,
                        "tipoCotizacion": 49.32089800,
                    }
                ],
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "arequest",
        AsyncMock(return_value=mock_response),
    )

    async def run():
        return await client.estadisticas_cambiarias.aget_evolucion_moneda(
            moneda="EUR",
            fechadesde="2024-06-12",
            fechahasta="2024-06-14",
            limit=100,
            offset=10,
        )

    data = asyncio.run(run())

    assert data.resultset.count == 1
    assert data.cotizaciones[0].fecha == "2024-06-12"
    assert data.cotizaciones[0].detalle[0].codigoMoneda == "EUR"


def test_aget_divisas_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Error al consultar Divisas.")

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "arequest", mock_arequest)

    async def run():
        await client.estadisticas_cambiarias.aget_divisas()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_cotizaciones_con_date(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {"fecha": "2024-06-12", "detalle": []},
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)
    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    client.estadisticas_cambiarias.get_cotizaciones(fecha=date(2024, 6, 12))

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones",
        params={"fecha": "2024-06-12"},
    )


def test_aget_cotizaciones_con_date(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {"fecha": "2024-06-12", "detalle": []},
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.estadisticas_cambiarias._t, "arequest", mock_arequest)

    async def run():
        return await client.estadisticas_cambiarias.aget_cotizaciones(
            fecha=date(2024, 6, 12)
        )

    asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones",
        params={"fecha": "2024-06-12"},
    )


def test_get_cotizaciones_fecha_invalida(client, monkeypatch):
    mock_request = MagicMock()
    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    with pytest.raises(ValueError, match="Fecha inválida"):
        client.estadisticas_cambiarias.get_cotizaciones(fecha="12/06/2024")

    mock_request.assert_not_called()


def test_get_evolucion_moneda_con_dates(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)
    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", mock_request)

    client.estadisticas_cambiarias.get_evolucion_moneda(
        moneda="EUR",
        fechadesde=date(2024, 6, 12),
        fechahasta=date(2024, 6, 14),
    )

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones/EUR",
        params={"fechadesde": "2024-06-12", "fechahasta": "2024-06-14"},
    )


def test_aget_evolucion_moneda_con_dates(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.estadisticas_cambiarias._t, "arequest", mock_arequest)

    async def run():
        return await client.estadisticas_cambiarias.aget_evolucion_moneda(
            moneda="EUR",
            fechadesde=date(2024, 6, 12),
            fechahasta=date(2024, 6, 14),
        )

    asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/estadisticascambiarias/v1.0/Cotizaciones/EUR",
        params={"fechadesde": "2024-06-12", "fechahasta": "2024-06-14"},
    )
