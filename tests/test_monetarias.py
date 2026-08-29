import asyncio
from datetime import date
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from bcra_sdk.exceptions import BCRAHTTPError


def test_get_monetarias(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 2, "offset": 0, "limit": 1000}},
        "results": [
            {
                "idVariable": 1,
                "descripcion": "Reservas internacionales",
                "categoria": "Principales Variables",
                "tipoSerie": "Saldos",
                "periodicidad": "D",
                "unidadExpresion": "En millones de USD",
                "moneda": "ME",
                "primerFechaInformada": "1996-01-03",
                "ultFechaInformada": "2025-05-26",
                "ultValorInformado": 38384.0,
            },
            {
                "idVariable": 4,
                "descripcion": "Tipo de cambio minorista (promedio vendedor)",
                "categoria": "Principales Variables",
                "tipoSerie": "Tipo de cambio",
                "periodicidad": "D",
                "unidadExpresion": "Pesos argentinos por dólar estadounidense",
                "moneda": "ML",
                "primerFechaInformada": "2010-06-01",
                "ultFechaInformada": "2025-05-26",
                "ultValorInformado": 1215.5,
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    data = client.monetarias.get_monetarias()

    mock_request.assert_called_once_with(
        "GET", "/estadisticas/v4.0/monetarias", params=None
    )
    assert data.resultset.count == 2
    assert data.resultset.offset == 0
    assert data.resultset.limit == 1000
    assert len(data.variables) == 2
    assert data.variables[0].idVariable == 1
    assert data.variables[0].descripcion == "Reservas internacionales"
    assert data.variables[0].categoria == "Principales Variables"
    assert data.variables[0].tipoSerie == "Saldos"
    assert data.variables[0].periodicidad == "D"
    assert data.variables[0].unidadExpresion == "En millones de USD"
    assert data.variables[0].moneda == "ME"
    assert data.variables[0].primerFechaInformada == "1996-01-03"
    assert data.variables[0].ultFechaInformada == "2025-05-26"
    assert data.variables[0].ultValorInformado == 38384.0
    assert data.variables[1].idVariable == 4
    assert data.variables[1].ultValorInformado == 1215.5


def test_get_monetarias_vacio(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 0, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.monetarias.get_monetarias()

    assert data.resultset.count == 0
    assert data.variables == []


def test_get_monetarias_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Se produjo un error al ejecutar la acción."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.monetarias.get_monetarias()
    assert exc_info.value.status_code == 500
    assert fake_data["errorMessages"][0] in exc_info.value.message


def test_aget_monetarias(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [
            {
                "idVariable": 1,
                "descripcion": "Reservas internacionales",
                "categoria": "Principales Variables",
                "tipoSerie": "Saldos",
                "periodicidad": "D",
                "unidadExpresion": "En millones de USD",
                "moneda": "ME",
                "primerFechaInformada": "1996-01-03",
                "ultFechaInformada": "2025-05-26",
                "ultValorInformado": 38384.0,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.monetarias._t, "arequest", mock_arequest)

    async def run():
        return await client.monetarias.aget_monetarias()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/estadisticas/v4.0/monetarias", params=None
    )
    assert data.resultset.count == 1
    assert len(data.variables) == 1
    assert data.variables[0].idVariable == 1
    assert data.variables[0].ultValorInformado == 38384.0


def test_aget_monetarias_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Se produjo un error al ejecutar la acción.")

    monkeypatch.setattr(client.monetarias._t, "arequest", mock_arequest)

    async def run():
        await client.monetarias.aget_monetarias()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_evolucion_variable_basico(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 2, "offset": 0, "limit": 1000}},
        "results": [
            {
                "idVariable": 1,
                "detalle": [
                    {"fecha": "2025-05-26", "valor": 38384.0},
                    {"fecha": "2025-05-23", "valor": 38428.0},
                ],
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    data = client.monetarias.get_evolucion_variable(idVariable=1)

    mock_request.assert_called_once_with(
        "GET", "/estadisticas/v4.0/monetarias/1", params=None
    )
    assert data.resultset.count == 2
    assert data.resultset.offset == 0
    assert data.resultset.limit == 1000
    assert len(data.series) == 1
    assert data.series[0].idVariable == 1
    assert len(data.series[0].detalle) == 2
    assert data.series[0].detalle[0].fecha == "2025-05-26"
    assert data.series[0].detalle[0].valor == 38384.0
    assert data.series[0].detalle[1].valor == 38428.0


def test_get_evolucion_variable_con_params(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 10, "limit": 100}},
        "results": [
            {
                "idVariable": 4,
                "detalle": [{"fecha": "2025-05-26", "valor": 1163.94}],
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    data = client.monetarias.get_evolucion_variable(
        idVariable=4,
        desde="2025-05-20",
        hasta="2025-05-26",
        offset=10,
        limit=100,
    )

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticas/v4.0/monetarias/4",
        params={
            "desde": "2025-05-20",
            "hasta": "2025-05-26",
            "offset": 10,
            "limit": 100,
        },
    )
    assert data.resultset.limit == 100
    assert data.resultset.offset == 10
    assert data.series[0].idVariable == 4
    assert data.series[0].detalle[0].valor == 1163.94


def test_get_evolucion_variable_con_dates(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)
    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    client.monetarias.get_evolucion_variable(
        idVariable=1,
        desde=date(2025, 5, 20),
        hasta=date(2025, 5, 26),
    )

    mock_request.assert_called_once_with(
        "GET",
        "/estadisticas/v4.0/monetarias/1",
        params={"desde": "2025-05-20", "hasta": "2025-05-26"},
    )


def test_get_evolucion_variable_vacio(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 0, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.monetarias.get_evolucion_variable(idVariable=1)

    assert data.resultset.count == 0
    assert data.series == []


def test_get_evolucion_variable_desde_invalida(client, monkeypatch):
    mock_request = MagicMock()
    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    with pytest.raises(ValueError, match="Fecha inválida"):
        client.monetarias.get_evolucion_variable(idVariable=1, desde="20/05/2025")

    mock_request.assert_not_called()


def test_get_evolucion_variable_400(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 400,
        "errorMessages": [
            "Parámetro erróneo: La fecha desde no puede ser mayor a la fecha hasta."
        ],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(400, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.monetarias.get_evolucion_variable(
            idVariable=1,
            desde="2025-05-26",
            hasta="2025-05-20",
        )
    assert exc_info.value.status_code == 400


def test_get_evolucion_variable_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["IdVariable invalida."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.monetarias.get_evolucion_variable(idVariable=999999)
    assert exc_info.value.status_code == 404
    assert "IdVariable invalida." in exc_info.value.message


def test_get_evolucion_variable_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Se produjo un error al ejecutar la acción."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.monetarias._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.monetarias.get_evolucion_variable(idVariable=1)
    assert exc_info.value.status_code == 500


def test_aget_evolucion_variable(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [
            {
                "idVariable": 1,
                "detalle": [
                    {"fecha": "2025-05-26", "valor": 38384.0},
                ],
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.monetarias._t, "arequest", mock_arequest)

    async def run():
        return await client.monetarias.aget_evolucion_variable(
            idVariable=1,
            desde="2025-05-20",
            hasta="2025-05-26",
            offset=10,
            limit=5,
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/estadisticas/v4.0/monetarias/1",
        params={
            "desde": "2025-05-20",
            "hasta": "2025-05-26",
            "offset": 10,
            "limit": 5,
        },
    )
    assert data.resultset.count == 1
    assert data.series[0].idVariable == 1
    assert data.series[0].detalle[0].valor == 38384.0


def test_aget_evolucion_variable_con_dates(client, monkeypatch):
    fake_data = {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.monetarias._t, "arequest", mock_arequest)

    async def run():
        return await client.monetarias.aget_evolucion_variable(
            idVariable=1,
            desde=date(2025, 5, 20),
            hasta=date(2025, 5, 26),
        )

    asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/estadisticas/v4.0/monetarias/1",
        params={"desde": "2025-05-20", "hasta": "2025-05-26"},
    )


def test_aget_evolucion_variable_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Se produjo un error al ejecutar la acción.")

    monkeypatch.setattr(client.monetarias._t, "arequest", mock_arequest)

    async def run():
        await client.monetarias.aget_evolucion_variable(idVariable=1)

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500
