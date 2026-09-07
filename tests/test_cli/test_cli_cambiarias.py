import httpx

from bcra_sdk.cli import app
from bcra_sdk.exceptions import BCRAHTTPError


def _divisas_data():
    return {
        "status": 200,
        "results": [
            {"codigo": "ARS", "denominacion": "PESO ARGENTINO"},
            {"codigo": "USD", "denominacion": "DOLAR"},
        ],
    }


def _cotizaciones_data():
    return {
        "status": 200,
        "results": {
            "fecha": "2024-06-12",
            "detalle": [
                {
                    "codigoMoneda": "USD",
                    "descripcion": "Dolar",
                    "tipoPase": 903.0,
                    "tipoCotizacion": 910.0,
                }
            ],
        },
    }


def _evolucion_data():
    return {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 10}},
        "results": [
            {
                "fecha": "2024-06-12",
                "detalle": [
                    {
                        "codigoMoneda": "USD",
                        "descripcion": "Dolar",
                        "tipoPase": 903.0,
                        "tipoCotizacion": 910.0,
                    }
                ],
            }
        ],
    }


def test_divisas_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_divisas_data()),
    )
    result = cli.invoke(app, ["cambiarias", "divisas"])
    assert result.exit_code == 0, result.output
    assert '"codigo": "ARS"' in result.output


def test_cotizaciones_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_cotizaciones_data()),
    )
    result = cli.invoke(app, ["cambiarias", "cotizaciones", "--fecha", "2024-06-12"])
    assert result.exit_code == 0, result.output
    assert '"fecha": "2024-06-12"' in result.output


def test_evolucion_moneda_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.estadisticas_cambiarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_evolucion_data()),
    )
    result = cli.invoke(
        app,
        [
            "cambiarias",
            "evolucion-moneda",
            "USD",
            "--desde",
            "2024-06-01",
            "--hasta",
            "2024-06-12",
            "--limit",
            "10",
            "--offset",
            "0",
        ],
    )
    assert result.exit_code == 0, result.output
    assert '"count": 1' in result.output


def test_evolucion_moneda_error(cli, monkeypatch, client):
    def _raise(*a, **k):
        raise BCRAHTTPError(404, "Moneda no encontrada")

    monkeypatch.setattr(client.estadisticas_cambiarias._t, "request", _raise)
    result = cli.invoke(app, ["cambiarias", "evolucion-moneda", "XXX"])
    assert result.exit_code == 1
    assert "Moneda no encontrada" in result.output
