import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

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


def test_get_cheque_denunciado(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "numeroCheque": 20377516,
            "denunciado": True,
            "fechaProcesamiento": "2026-08-26",
            "denominacionEntidad": "BANCO DE LA NACION ARGENTINA",
            "detalles": [
                {
                    "sucursal": 524,
                    "numeroCuenta": 5240055962,
                    "causal": "Denunciado por tercero",
                }
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.cheques._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.cheques.get_cheque_denunciado(
        codigo_entidad=11, numero_cheque=20377516
    )

    assert data.numeroCheque == 20377516
    assert data.denunciado is True
    assert data.fechaProcesamiento == "2026-08-26"
    assert data.denominacionEntidad == "BANCO DE LA NACION ARGENTINA"
    assert len(data.detalles) == 1
    assert data.detalles[0].sucursal == 524
    assert data.detalles[0].numeroCuenta == 5240055962
    assert data.detalles[0].causal == "Denunciado por tercero"


def test_get_cheque_denunciado_multiples_detalles(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "numeroCheque": 507,
            "denunciado": True,
            "fechaProcesamiento": "2024-05-24",
            "denominacionEntidad": "BANCO DE LA NACION ARGENTINA",
            "detalles": [
                {
                    "sucursal": 89,
                    "numeroCuenta": 890036218,
                    "causal": "Denunciado por titular",
                },
                {
                    "sucursal": 275,
                    "numeroCuenta": 2750016469,
                    "causal": "Denunciado por tercero",
                },
                {
                    "sucursal": 391,
                    "numeroCuenta": 3910038583,
                    "causal": "Denunciado por tercero",
                },
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.cheques._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.cheques.get_cheque_denunciado(codigo_entidad=11, numero_cheque=507)

    assert data.denunciado is True
    assert len(data.detalles) == 3
    assert data.detalles[0].causal == "Denunciado por titular"
    assert data.detalles[1].sucursal == 275
    assert data.detalles[2].numeroCuenta == 3910038583


def test_get_cheque_no_denunciado(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "numeroCheque": 203775991,
            "denunciado": False,
            "fechaProcesamiento": "2024-05-24",
            "denominacionEntidad": "BANCO DE LA NACION ARGENTINA",
            "detalles": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.cheques._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.cheques.get_cheque_denunciado(
        codigo_entidad=11, numero_cheque=203775991
    )

    assert data.numeroCheque == 203775991
    assert data.denunciado is False
    assert data.detalles == []


def test_get_cheque_denunciado_400(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 400,
        "errorMessages": ["Validar formato de los parámetros enviados."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(400, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.cheques._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.cheques.get_cheque_denunciado(codigo_entidad="a", numero_cheque="b")
    assert exc_info.value.status_code == 400


def test_get_cheque_denunciado_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["Entidad informada inexistente."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.cheques._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.cheques.get_cheque_denunciado(codigo_entidad=999, numero_cheque=123)
    assert exc_info.value.status_code == 404


def test_get_cheque_denunciado_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Error al consultar Cheques."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.cheques._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.cheques.get_cheque_denunciado(codigo_entidad=11, numero_cheque=123)
    assert exc_info.value.status_code == 500


def test_aget_entidades(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {"codigoEntidad": 11, "denominacion": "BANCO DE LA NACION ARGENTINA"},
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.cheques._t, "arequest", AsyncMock(return_value=mock_response)
    )

    async def run():
        return await client.cheques.aget_entidades()

    data = asyncio.run(run())

    assert len(data.entidades) == 1
    assert data.entidades[0].codigoEntidad == 11


def test_aget_cheque_denunciado(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": {
            "numeroCheque": 20377516,
            "denunciado": True,
            "fechaProcesamiento": "2026-08-26",
            "denominacionEntidad": "BANCO DE LA NACION ARGENTINA",
            "detalles": [
                {
                    "sucursal": 524,
                    "numeroCuenta": 5240055962,
                    "causal": "Denunciado por tercero",
                }
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.cheques._t, "arequest", AsyncMock(return_value=mock_response)
    )

    async def run():
        return await client.cheques.aget_cheque_denunciado(
            codigo_entidad=11, numero_cheque=20377516
        )

    data = asyncio.run(run())

    assert data.numeroCheque == 20377516
    assert data.denunciado is True
    assert len(data.detalles) == 1


def test_aget_entidades_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Error al consultar Maestros.")

    monkeypatch.setattr(client.cheques._t, "arequest", mock_arequest)

    async def run():
        await client.cheques.aget_entidades()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500
