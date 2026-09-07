import httpx

from bcra_sdk.cli import app
from bcra_sdk.exceptions import BCRAHTTPError


def _deudas_data(cuit="20111111112"):
    return {
        "status": 200,
        "results": {
            "identificacion": int(cuit),
            "denominacion": "PEPE",
            "periodos": [
                {
                    "periodo": "202606",
                    "entidades": [
                        {
                            "entidad": "BANCO NACION",
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


def _historica_data():
    return {
        "status": 200,
        "results": {
            "identificacion": "20234567891",
            "denominacion": "PEPE",
            "periodos": [
                {
                    "periodo": "202403",
                    "entidades": [
                        {
                            "entidad": "BANCO NACION",
                            "situacion": 1,
                            "monto": 35.0,
                            "enRevision": False,
                            "procesoJud": False,
                        }
                    ],
                }
            ],
        },
    }


def _rechazados_data():
    return {
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
                                    "monto": 115000.0,
                                    "fechaPago": None,
                                    "fechaPagoMulta": None,
                                    "estadoMulta": "IMPAGA",
                                    "ctaPersonal": False,
                                    "denomJuridica": "S.R.L.",
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


def test_deudas_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.deudores._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_deudas_data()),
    )
    result = cli.invoke(app, ["deudores", "deudas", "20111111112"])
    assert result.exit_code == 0, result.output
    assert '"periodo": "202606"' in result.output


def test_deudas_table(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.deudores._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_deudas_data()),
    )
    result = cli.invoke(app, ["--format", "table", "deudores", "deudas", "20111111112"])
    assert result.exit_code == 0, result.output
    assert "BANCO NACION" in result.output


def test_deudas_historicas(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.deudores._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_historica_data()),
    )
    result = cli.invoke(app, ["deudores", "deudas-historicas", "20234567891"])
    assert result.exit_code == 0, result.output
    assert '"identificacion": "20234567891"' in result.output


def test_cheques_rechazados_json(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.deudores._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_rechazados_data()),
    )
    result = cli.invoke(app, ["deudores", "cheques-rechazados", "20111111112"])
    assert result.exit_code == 0, result.output
    assert "SIN FONDOS" in result.output


def test_cheques_rechazados_table(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.deudores._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_rechazados_data()),
    )
    result = cli.invoke(
        app,
        ["--format", "table", "deudores", "cheques-rechazados", "20111111112"],
    )
    assert result.exit_code == 0, result.output
    assert "752395" in result.output
    assert "no" in result.output


def test_deudas_error(cli, monkeypatch, client):
    def _raise(*a, **k):
        raise BCRAHTTPError(404, "No encontrado")

    monkeypatch.setattr(client.deudores._t, "request", _raise)
    result = cli.invoke(app, ["deudores", "deudas", "20111111112"])
    assert result.exit_code == 1
    assert "No encontrado" in result.output


def test_deudas_cuit_invalido(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.deudores._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_deudas_data()),
    )
    result = cli.invoke(app, ["deudores", "deudas", "12345"])
    assert result.exit_code == 1
    assert "CUIT inválido" in result.output
