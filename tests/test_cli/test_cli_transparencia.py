import httpx

from bcra_sdk.cli import app

ENTIDAD = 325


def _cajas_data():
    return {
        "status": 200,
        "results": [
            {
                "codigoEntidad": ENTIDAD,
                "descripcionEntidad": "BANCO NACION",
                "fechaInformacion": "2025-01-01",
                "procesoSimplificadoDebidaDiligencia": "Si",
            }
        ],
    }


def _paquetes_data():
    return {
        "status": 200,
        "results": [
            {
                "codigoEntidad": ENTIDAD,
                "descripcionEntidad": "BANCO NACION",
                "fechaInformacion": "2025-01-01",
                "nombreCompleto": "Paquete Hogar",
                "nombreCorto": "Hogar",
                "comisionMaximaMantenimiento": 5000.0,
                "ingresoMinimoMensual": 0.0,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 0,
                "beneficiarios": "titular",
                "segmento": "Persona",
                "productosIntegrantes": "caja de ahorro, cuenta corriente",
                "territorioValidez": "nacional",
                "masInformacion": None,
            }
        ],
    }


def _plazos_data():
    return {
        "status": 200,
        "results": [
            {
                "codigoEntidad": ENTIDAD,
                "descripcionEntidad": "BANCO NACION",
                "fechaInformacion": "2025-01-01",
                "nombreCompleto": "Plazo Fijo Tradicional",
                "nombreCorto": "PF Tradicional",
                "denominacion": "pesos",
                "montoMinimoInvertir": 1.0,
                "plazoMinimoInvertirDias": 30,
                "canalConstitucion": "homebanking",
                "tasaEfectivaAnualMinima": 40.0,
                "territorioValidez": "nacional",
                "masInformacion": None,
            }
        ],
    }


def _prendarios_data():
    return {
        "status": 200,
        "results": [_prestamo()],
    }


def _prestamo():
    return {
        "relacionMontoTasacion": 80,
        "destinoFondos": "libre",
        "montoMinimoOtorgable": 100.0,
        "denominacion": "pesos",
        "montoMaximoOtorgable": 100000.0,
        "plazoMaximoOtorgable": 60,
        "ingresoMinimoMensual": 50000.0,
        "antiguedadLaboralMinimaMeses": 6,
        "edadMaximaSolicitada": 75,
        "relacionCuotaIngreso": 30,
        "beneficiario": "titular",
        "cargoMaximoCancelacionAnticipada": 5,
        "tasaEfectivaAnualMaxima": 60.0,
        "tipoTasa": "fija",
        "costoFinancieroEfectivoTotalMaximo": 80.0,
        "cuotaInicial": 10.0,
        "codigoEntidad": ENTIDAD,
        "descripcionEntidad": "BANCO NACION",
        "fechaInformacion": "2025-01-01",
        "nombreCompleto": "Prestamo Prendario",
        "nombreCorto": "Prendario",
        "territorioValidez": "nacional",
        "masInformacion": None,
    }


def _hipotecarios_data():
    data = _prestamo()
    data.pop("montoMinimoOtorgable")
    return {"status": 200, "results": [data]}


def _personales_data():
    data = _prestamo()
    data.pop("relacionMontoTasacion")
    data.pop("destinoFondos")
    return {"status": 200, "results": [data]}


def _tarjetas_data():
    return {
        "status": 200,
        "results": [
            {
                "comisionMaximaAdministracionMantenimiento": 5000.0,
                "comisionMaximaRenovacion": 3000.0,
                "tasaEfectivaAnualMaximaFinanciacion": 70.0,
                "tasaEfectivaAnualMaximaAdelantoEfectivo": 75.0,
                "ingresoMinimoMensual": 0.0,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 0,
                "segmento": "Persona",
                "codigoEntidad": ENTIDAD,
                "descripcionEntidad": "BANCO NACION",
                "fechaInformacion": "2025-01-01",
                "nombreCompleto": "Tarjeta Premio",
                "nombreCorto": "Premio",
                "territorioValidez": "nacional",
                "masInformacion": None,
            }
        ],
    }


def test_cajas_ahorros(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_cajas_data()),
    )
    result = cli.invoke(
        app, ["transparencia", "cajas-ahorros", "--entidad", str(ENTIDAD)]
    )
    assert result.exit_code == 0, result.output
    assert "BANCO NACION" in result.output


def test_paquetes_productos(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_paquetes_data()),
    )
    result = cli.invoke(app, ["transparencia", "paquetes-productos"])
    assert result.exit_code == 0, result.output
    assert "Paquete Hogar" in result.output


def test_plazos_fijos(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_plazos_data()),
    )
    result = cli.invoke(app, ["transparencia", "plazos-fijos"])
    assert result.exit_code == 0, result.output
    assert "PF Tradicional" in result.output


def test_prestamos_prendarios(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_prendarios_data()),
    )
    result = cli.invoke(app, ["transparencia", "prestamos-prendarios"])
    assert result.exit_code == 0, result.output
    assert "Prendario" in result.output


def test_prestamos_hipotecarios(cli, monkeypatch, client):
    data = _hipotecarios_data()
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=data),
    )
    result = cli.invoke(app, ["transparencia", "prestamos-hipotecarios"])
    assert result.exit_code == 0, result.output
    assert "montoMaximoOtorgable" in result.output


def test_prestamos_personales(cli, monkeypatch, client):
    data = _personales_data()
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=data),
    )
    result = cli.invoke(app, ["transparencia", "prestamos-personales"])
    assert result.exit_code == 0, result.output
    assert "montoMinimoOtorgable" in result.output


def test_tarjetas_credito_table(cli, monkeypatch, client):
    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        lambda *a, **k: httpx.Response(200, json=_tarjetas_data()),
    )
    result = cli.invoke(app, ["--format", "table", "transparencia", "tarjetas-credito"])
    assert result.exit_code == 0, result.output
    assert "Premio" in result.output
