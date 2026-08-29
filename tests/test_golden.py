import asyncio
import json
import pathlib
from dataclasses import asdict
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from bcra_sdk.exceptions import BCRAHTTPError

_CASSETTES = pathlib.Path(__file__).parent / "cassettes"


def load_cassette(name: str) -> dict:
    target = _CASSETTES / f"{name}.json"
    return json.loads(target.read_text(encoding="utf-8"))


def http_response(cassette: dict) -> httpx.Response:
    return httpx.Response(cassette["status_code"], json=cassette["json"])


def test_get_divisas_golden(client, monkeypatch):
    cassette = load_cassette("estadisticascambiarias.get_divisas")
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=http_response(cassette)),
    )
    data = client.estadisticas_cambiarias.get_divisas()
    assert asdict(data) == {"divisas": cassette["json"]["results"]}


def test_get_cotizaciones_golden(client, monkeypatch):
    cassette = load_cassette("estadisticascambiarias.get_cotizaciones")
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=http_response(cassette)),
    )
    data = client.estadisticas_cambiarias.get_cotizaciones(fecha="2024-06-12")
    assert data.fecha == "2024-06-12"
    assert asdict(data) == cassette["json"]["results"]


def test_get_evolucion_moneda_golden(client, monkeypatch):
    cassette = load_cassette("estadisticascambiarias.get_evolucion_moneda")
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        MagicMock(return_value=http_response(cassette)),
    )
    data = client.estadisticas_cambiarias.get_evolucion_moneda(
        moneda="EUR",
        fechadesde="2024-06-10",
        fechahasta="2024-06-12",
        limit=10,
    )
    parsed = {
        "metadata": {"resultset": asdict(data.resultset)},
        "results": [asdict(c) for c in data.cotizaciones],
    }
    raw = {
        "metadata": cassette["json"]["metadata"],
        "results": cassette["json"]["results"],
    }
    assert parsed == raw


def test_get_entidades_golden(client, monkeypatch):
    cassette = load_cassette("cheques.get_entidades")
    monkeypatch.setattr(
        client.cheques._t,
        "request",
        MagicMock(return_value=http_response(cassette)),
    )
    data = client.cheques.get_entidades()
    assert asdict(data) == {"entidades": cassette["json"]["results"]}


def test_get_monetarias_golden(client, monkeypatch):
    cassette = load_cassette("monetarias.get_monetarias")
    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        MagicMock(return_value=http_response(cassette)),
    )
    data = client.monetarias.get_monetarias()
    parsed = {
        "metadata": {"resultset": asdict(data.resultset)},
        "results": [asdict(v) for v in data.variables],
    }
    raw = {
        "metadata": cassette["json"]["metadata"],
        "results": cassette["json"]["results"],
    }
    assert parsed == raw


def test_get_deudas_error_golden(client, monkeypatch):
    cassette = load_cassette("deudores.get_deudas")
    message = cassette["json"]["errorMessages"][0]

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(cassette["status_code"], message)

    monkeypatch.setattr(client.deudores._t, "request", mock_request)
    with pytest.raises(BCRAHTTPError) as exc_info:
        client.deudores.get_deudas(cuit="20111111112")
    assert exc_info.value.status_code == cassette["status_code"]
    assert message in exc_info.value.message


def test_aget_cotizaciones_golden(client, monkeypatch):
    cassette = load_cassette("estadisticascambiarias.get_cotizaciones")
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "arequest",
        AsyncMock(return_value=http_response(cassette)),
    )

    async def run():
        return await client.estadisticas_cambiarias.aget_cotizaciones(
            fecha="2024-06-12"
        )

    data = asyncio.run(run())
    assert asdict(data) == cassette["json"]["results"]


def test_aget_deudas_error_golden(client, monkeypatch):
    cassette = load_cassette("deudores.get_deudas")
    message = cassette["json"]["errorMessages"][0]

    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(cassette["status_code"], message)

    monkeypatch.setattr(client.deudores._t, "arequest", mock_arequest)

    async def run():
        await client.deudores.aget_deudas(cuit="20111111112")

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == cassette["status_code"]
    assert message in exc_info.value.message
