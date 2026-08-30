import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from bcra_sdk.exceptions import BCRAHTTPError


def test_get_cajas_ahorros(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.U.",
                "fechaInformacion": "2019-07-10",
                "procesoSimplificadoDebidaDiligencia": "SI",
            },
            {
                "codigoEntidad": 11,
                "descripcionEntidad": "BANCO DE LA NACION ARGENTINA",
                "fechaInformacion": "2017-03-27",
                "procesoSimplificadoDebidaDiligencia": "SI",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_cajas_ahorros()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/CajasAhorros", params=None
    )
    assert len(data.cajas_ahorros) == 2
    caja = data.cajas_ahorros[1]
    assert caja.codigoEntidad == 11
    assert caja.descripcionEntidad == "BANCO DE LA NACION ARGENTINA"
    assert caja.fechaInformacion == "2017-03-27"
    assert caja.procesoSimplificadoDebidaDiligencia == "SI"


def test_get_cajas_ahorros_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "codigoEntidad": 11,
                "descripcionEntidad": "BANCO DE LA NACION ARGENTINA",
                "fechaInformacion": "2017-03-27",
                "procesoSimplificadoDebidaDiligencia": "SI",
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_cajas_ahorros(codigoEntidad=11)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/CajasAhorros",
        params={"codigoEntidad": 11},
    )
    assert data.cajas_ahorros[0].codigoEntidad == 11
    assert len(data.cajas_ahorros) == 1


def test_get_cajas_ahorros_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_cajas_ahorros()

    assert data.cajas_ahorros == []


def test_get_cajas_ahorros_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_cajas_ahorros(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_cajas_ahorros_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_cajas_ahorros()
    assert exc_info.value.status_code == 500


def test_aget_cajas_ahorros(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "codigoEntidad": 11,
                "descripcionEntidad": "BANCO DE LA NACION ARGENTINA",
                "fechaInformacion": "2017-03-27",
                "procesoSimplificadoDebidaDiligencia": "SI",
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_cajas_ahorros(
            codigoEntidad=11
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/CajasAhorros",
        params={"codigoEntidad": 11},
    )
    assert data.cajas_ahorros[0].codigoEntidad == 11


def test_aget_cajas_ahorros_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_cajas_ahorros()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/CajasAhorros", params=None
    )
    assert data.cajas_ahorros == []


def test_aget_cajas_ahorros_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_cajas_ahorros()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500
