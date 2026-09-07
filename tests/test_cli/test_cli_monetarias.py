import httpx

from bcra_sdk.cli import app
from bcra_sdk.exceptions import BCRAHTTPError


def _monetarias_data():
    return {
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


def _evolucion_data():
    return {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 1000}},
        "results": [
            {
                "idVariable": 16,
                "detalle": [
                    {"fecha": "2025-05-26", "valor": 38384.0},
                    {"fecha": "2025-05-23", "valor": 38328.0},
                ],
            }
        ],
    }


def _metodologias_data():
    return {
        "status": 200,
        "metadata": {"resultset": {"count": 1, "offset": 0, "limit": 250}},
        "results": [
            {"id": 1, "detalle": "Metodología de las reservas internacionales."}
        ],
    }


def _metodologia_data():
    return {
        "status": 200,
        "results": [{"id": 1, "detalle": "Metodología de las reservas."}],
    }


def test_monetarias_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_monetarias_data()),
    )
    result = cli.invoke(app, ["monetarias", "monetarias"])
    assert result.exit_code == 0, result.output
    assert "Reservas internacionales" in result.output


def test_evolucion_variable_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_evolucion_data()),
    )
    result = cli.invoke(
        app,
        [
            "monetarias",
            "evolucion-variable",
            "16",
            "--desde",
            "2025-05-01",
            "--hasta",
            "2025-05-26",
            "--offset",
            "0",
            "--limit",
            "1000",
        ],
    )
    assert result.exit_code == 0, result.output
    assert '"fecha": "2025-05-26"' in result.output


def test_metodologias_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_metodologias_data()),
    )
    result = cli.invoke(app, ["monetarias", "metodologias"])
    assert result.exit_code == 0, result.output
    assert "Metodología de las reservas internacionales." in result.output


def test_metodologia_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_metodologia_data()),
    )
    result = cli.invoke(app, ["monetarias", "metodologia", "1"])
    assert result.exit_code == 0, result.output
    assert '"id": 1' in result.output


def test_metodologias_table(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.monetarias._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_metodologias_data()),
    )
    result = cli.invoke(app, ["--format", "table", "monetarias", "metodologias"])
    assert result.exit_code == 0, result.output
    assert "reservas" in result.output


def test_monetarias_error(cli, monkeypatch, client):
    def _raise(*a, **k):
        raise BCRAHTTPError(500, "Error interno")

    monkeypatch.setattr(client.monetarias._t, "request", _raise)
    result = cli.invoke(app, ["monetarias", "monetarias"])
    assert result.exit_code == 1
    assert "Error interno" in result.output
