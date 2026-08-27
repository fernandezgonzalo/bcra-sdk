import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from bcra_sdk.exceptions import BCRAHTTPError


def test_get_deudas(client, monkeypatch):
    cuit = "1234567890"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": int(cuit),
            "denominacion": "PEPE",
            "periodos": [
                {
                    "periodo": "202606",
                    "entidades": [
                        {
                            "entidad": "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.",
                            "situacion": 1,
                            "fechaSit1": "2017-05-30",
                            "monto": 1121.0,
                            "diasAtrasoPago": 0,
                            "refinanciaciones": False,
                            "recategorizacionOblig": False,
                            "situacionJuridica": False,
                            "irrecDisposicionTecnica": False,
                            "enRevision": False,
                            "procesoJud": False,
                        }
                    ],
                }
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.deudores._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.deudores.get_deudas(cuit=cuit)

    assert str(data.identificacion) == cuit


def test_get_deudas_historicas(client, monkeypatch):
    identification = "20234567891"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": "20234567891",
            "denominacion": "PEPE",
            "periodos": [
                {
                    "periodo": "202403",
                    "entidades": [
                        {
                            "entidad": "BANCO DE LA NACION ARGENTINA",
                            "situacion": 1,
                            "monto": 35.0,
                            "enRevision": False,
                            "procesoJud": False,
                        }
                    ],
                },
                {
                    "periodo": "202402",
                    "entidades": [
                        {
                            "entidad": "BANCO DE LA NACION ARGENTINA",
                            "situacion": 1,
                            "monto": 41.0,
                            "enRevision": False,
                            "procesoJud": False,
                        }
                    ],
                },
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.deudores._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.deudores.get_deudas_historicas(identification=identification)

    assert data.identificacion == "20234567891"
    assert data.denominacion == "PEPE"
    assert len(data.periodos) == 2
    assert data.periodos[0].periodo == "202403"
    assert data.periodos[0].entidades[0].entidad == "BANCO DE LA NACION ARGENTINA"
    assert data.periodos[0].entidades[0].monto == 35.0
    assert data.periodos[1].periodo == "202402"
    assert data.periodos[1].entidades[0].monto == 41.0


def test_get_deudas_historicas_empty_periodos(client, monkeypatch):
    identification = "20234567891"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": "20234567891",
            "denominacion": "PEPE",
            "periodos": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.deudores._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.deudores.get_deudas_historicas(identification=identification)

    assert data.identificacion == "20234567891"
    assert data.periodos == []


def test_get_deudas_historicas_400(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 400,
        "errorMessages": [
            "Parámetro erróneo: Ingresar 11 dígitos para realizar la consulta."
        ],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(400, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.deudores._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_deudas_historicas(identification="123")
    assert exc_info.value.status_code == 400


def test_get_deudas_historicas_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontró datos para la identificación ingresada."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.deudores._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_deudas_historicas(identification="20234567891")
    assert exc_info.value.status_code == 404


def test_get_deudas_historicas_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Se produjo un error al ejecutar la acción."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.deudores._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_deudas_historicas(identification="20234567891")
    assert exc_info.value.status_code == 500


def test_get_cheques_rechazados(client, monkeypatch):
    identification = "20111111112"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": 20111111112,
            "causales": [
                {
                    "causal": "SIN FONDOS",
                    "entidades": [
                        {
                            "entidad": 1,
                            "detalle": [
                                {
                                    "nroCheque": 752395,
                                    "fechaRechazo": "2024-04-08",
                                    "monto": 115000.00,
                                    "fechaPago": None,
                                    "fechaPagoMulta": None,
                                    "estadoMulta": "IMPAGA",
                                    "ctaPersonal": False,
                                    "denomJuridica": "HM COLON MONTAJES INDUSTRIALES S. R. L.",
                                    "enRevision": False,
                                    "procesoJud": False,
                                }
                            ],
                        }
                    ],
                }
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.deudores._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.deudores.get_cheques_rechazados(identification=identification)

    assert data.identificacion == 20111111112
    assert len(data.causales) == 1
    assert data.causales[0].causal == "SIN FONDOS"
    assert data.causales[0].entidades[0].entidad == 1
    cheque = data.causales[0].entidades[0].detalle[0]
    assert cheque.nroCheque == 752395
    assert cheque.monto == 115000.00
    assert cheque.estadoMulta == "IMPAGA"
    assert cheque.ctaPersonal is False
    assert cheque.denomJuridica == "HM COLON MONTAJES INDUSTRIALES S. R. L."


def test_get_cheques_rechazados_vacio(client, monkeypatch):
    identification = "20111111112"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": 20111111112,
            "causales": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.deudores._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.deudores.get_cheques_rechazados(identification=identification)

    assert data.identificacion == 20111111112
    assert data.causales == []


def test_get_cheques_rechazados_400(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 400,
        "errorMessages": [
            "Parámetro erróneo: Ingresar 11 dígitos para realizar la consulta."
        ],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(400, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.deudores._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_cheques_rechazados(identification="123")
    assert exc_info.value.status_code == 400


def test_get_cheques_rechazados_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontró datos para la identificación ingresada."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.deudores._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_cheques_rechazados(identification="20111111112")
    assert exc_info.value.status_code == 404


def test_get_cheques_rechazados_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Se produjo un error al ejecutar la acción."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.deudores._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_cheques_rechazados(identification="20111111112")
    assert exc_info.value.status_code == 500


def test_aget_deudas(client, monkeypatch):
    cuit = "1234567890"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": int(cuit),
            "denominacion": "PEPE",
            "periodos": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.deudores._t, "arequest", AsyncMock(return_value=mock_response)
    )

    async def run():
        return await client.deudores.aget_deudas(cuit=cuit)

    data = asyncio.run(run())

    assert str(data.identificacion) == cuit
    assert data.periodos == []


def test_aget_deudas_historicas(client, monkeypatch):
    identification = "20234567891"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": "20234567891",
            "denominacion": "PEPE",
            "periodos": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.deudores._t, "arequest", AsyncMock(return_value=mock_response)
    )

    async def run():
        return await client.deudores.aget_deudas_historicas(
            identification=identification
        )

    data = asyncio.run(run())

    assert data.identificacion == "20234567891"
    assert data.periodos == []


def test_aget_cheques_rechazados(client, monkeypatch):
    identification = "20111111112"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": 20111111112,
            "causales": [],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)
    monkeypatch.setattr(
        client.deudores._t, "arequest", AsyncMock(return_value=mock_response)
    )

    async def run():
        return await client.deudores.aget_cheques_rechazados(
            identification=identification
        )

    data = asyncio.run(run())

    assert data.identificacion == 20111111112
    assert data.causales == []


def test_aget_deudas_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Se produjo un error al ejecutar la acción.")

    monkeypatch.setattr(client.deudores._t, "arequest", mock_arequest)

    async def run():
        await client.deudores.aget_deudas(cuit="1234567890")

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500
