import httpx

from bcra_sdk.cli import app
from bcra_sdk.exceptions import BCRAHTTPError


def _entidades_data():
    return {
        "status": 200,
        "results": [
            {"codigoEntidad": 1, "denominacion": "BANCO DE LA NACION ARGENTINA"},
            {"codigoEntidad": 2, "denominacion": "BANCO DE LA PROVINCIA"},
        ],
    }


def _denunciado_data():
    return {
        "status": 200,
        "results": {
            "numeroCheque": 752395,
            "denunciado": True,
            "fechaProcesamiento": "2024-04-08",
            "denominacionEntidad": "BANCO NACION",
            "detalles": [
                {"sucursal": 5, "numeroCuenta": 123456, "causal": "SIN FONDOS"}
            ],
        },
    }


def test_entidades_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.cheques._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_entidades_data()),
    )
    result = cli.invoke(app, ["cheques", "entidades"])
    assert result.exit_code == 0, result.output
    assert "BANCO DE LA NACION ARGENTINA" in result.output


def test_cheque_denunciado_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.cheques._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_denunciado_data()),
    )
    result = cli.invoke(app, ["cheques", "cheque-denunciado", "1", "752395"])
    assert result.exit_code == 0, result.output
    assert '"denunciado": true' in result.output


def test_cheque_denunciado_table(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.cheques._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_denunciado_data()),
    )
    result = cli.invoke(
        app,
        ["--format", "table", "cheques", "cheque-denunciado", "1", "752395"],
    )
    assert result.exit_code == 0, result.output
    assert "SIN FONDOS" in result.output


def test_cheque_denunciado_error(cli, monkeypatch, client):
    def _raise(*a, **k):
        raise BCRAHTTPError(404, "Cheque no encontrado")

    monkeypatch.setattr(client.cheques._t, "request", _raise)
    result = cli.invoke(app, ["cheques", "cheque-denunciado", "1", "752395"])
    assert result.exit_code == 1
    assert "Cheque no encontrado" in result.output
