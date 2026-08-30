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


def test_get_paquetes_productos(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "comisionMaximaMantenimiento": 725,
                "ingresoMinimoMensual": 20100,
                "antiguedadLaboralMinimaMeses": 3,
                "edadMaximaSolicitada": 59,
                "beneficiarios": "Personas humanas Monotributistas",
                "segmento": "Básico",
                "productosIntegrantes": "CAJA DE AHORRO DOLARES, TARJETA DE CREDITO",
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.U.",
                "fechaInformacion": "2019-07-10",
                "nombreCompleto": "SERVICIO CLASSIC",
                "nombreCorto": "CLASSIC",
                "territorioValidez": "0",
                "masInformacion": None,
            },
            {
                "comisionMaximaMantenimiento": 380.69,
                "ingresoMinimoMensual": 12500,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 100,
                "beneficiarios": "Clientes que acrediten sueldos en la entidad",
                "segmento": "Básico",
                "productosIntegrantes": "CUENTA SUELDO TARJETA DE CREDITO",
                "codigoEntidad": 11,
                "descripcionEntidad": "BANCO DE LA NACION ARGENTINA",
                "fechaInformacion": "2019-06-04",
                "nombreCompleto": "PAQUETE DE SERVICIOS CUENTA NACION SIMPLE",
                "nombreCorto": "CTA NACION SIMPLE",
                "territorioValidez": "0",
                "masInformacion": "COMISION DE MANTENIMIENTO BONIFICADA",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_paquetes_productos()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/PaquetesProductos", params=None
    )
    assert len(data.paquetes_productos) == 2
    paquete = data.paquetes_productos[1]
    assert paquete.codigoEntidad == 11
    assert paquete.descripcionEntidad == "BANCO DE LA NACION ARGENTINA"
    assert paquete.fechaInformacion == "2019-06-04"
    assert paquete.nombreCompleto == "PAQUETE DE SERVICIOS CUENTA NACION SIMPLE"
    assert paquete.nombreCorto == "CTA NACION SIMPLE"
    assert paquete.comisionMaximaMantenimiento == 380.69
    assert paquete.ingresoMinimoMensual == 12500
    assert paquete.antiguedadLaboralMinimaMeses == 0
    assert paquete.edadMaximaSolicitada == 100
    assert paquete.beneficiarios == "Clientes que acrediten sueldos en la entidad"
    assert paquete.segmento == "Básico"
    assert paquete.productosIntegrantes == "CUENTA SUELDO TARJETA DE CREDITO"
    assert paquete.territorioValidez == "0"
    assert data.paquetes_productos[0].masInformacion is None
    assert paquete.masInformacion == "COMISION DE MANTENIMIENTO BONIFICADA"


def test_get_paquetes_productos_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "comisionMaximaMantenimiento": 770,
                "ingresoMinimoMensual": 56000,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 100,
                "beneficiarios": "Personas humanas Responsables Inscriptos",
                "segmento": "Premium platinum",
                "productosIntegrantes": "CAJA DE AHORROS EN DOLARES, CUENTA CORRIENTE",
                "codigoEntidad": 14,
                "descripcionEntidad": "BANCO DE LA PROVINCIA DE BUENOS AIRES",
                "fechaInformacion": "2019-05-08",
                "nombreCompleto": "EVOLUCION",
                "nombreCorto": "EVOLUCION",
                "territorioValidez": "1",
                "masInformacion": "COMISION BONIFICADA HASTA EL 31.12.2019.",
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_paquetes_productos(codigoEntidad=14)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/PaquetesProductos",
        params={"codigoEntidad": 14},
    )
    assert data.paquetes_productos[0].codigoEntidad == 14
    assert len(data.paquetes_productos) == 1


def test_get_paquetes_productos_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_paquetes_productos()

    assert data.paquetes_productos == []


def test_get_paquetes_productos_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_paquetes_productos(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_paquetes_productos_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_paquetes_productos()
    assert exc_info.value.status_code == 500


def test_aget_paquetes_productos(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "comisionMaximaMantenimiento": 770,
                "ingresoMinimoMensual": 56000,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 100,
                "beneficiarios": "Personas humanas Responsables Inscriptos",
                "segmento": "Premium platinum",
                "productosIntegrantes": "CAJA DE AHORROS EN DOLARES, CUENTA CORRIENTE",
                "codigoEntidad": 14,
                "descripcionEntidad": "BANCO DE LA PROVINCIA DE BUENOS AIRES",
                "fechaInformacion": "2019-05-08",
                "nombreCompleto": "EVOLUCION",
                "nombreCorto": "EVOLUCION",
                "territorioValidez": "1",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_paquetes_productos(
            codigoEntidad=14
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/PaquetesProductos",
        params={"codigoEntidad": 14},
    )
    assert data.paquetes_productos[0].codigoEntidad == 14


def test_aget_paquetes_productos_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_paquetes_productos()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/PaquetesProductos", params=None
    )
    assert data.paquetes_productos == []


def test_aget_paquetes_productos_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_paquetes_productos()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_plazos_fijos(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "denominacion": None,
                "montoMinimoInvertir": 1000,
                "plazoMinimoInvertirDias": 1,
                "canalConstitucion": "Línea telefónica",
                "tasaEfectivaAnualMinima": 10.47,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.U.",
                "fechaInformacion": "2019-07-16",
                "nombreCompleto": "PLAZOFIJOTRADICIONAL",
                "nombreCorto": "PFTRADICIONAL",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": None,
            },
            {
                "denominacion": "Pesos",
                "montoMinimoInvertir": 5000,
                "plazoMinimoInvertirDias": 30,
                "canalConstitucion": "Home banking",
                "tasaEfectivaAnualMinima": 15.01,
                "codigoEntidad": 303,
                "descripcionEntidad": "BANCO FINANSUR S.A.",
                "fechaInformacion": "2017-06-08",
                "nombreCompleto": "PLAZO FIJO",
                "nombreCorto": "P. FIJO",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": "BONIFICADO",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_plazos_fijos()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/PlazosFijos", params=None
    )
    assert len(data.plazos_fijos) == 2
    plazo = data.plazos_fijos[1]
    assert plazo.codigoEntidad == 303
    assert plazo.descripcionEntidad == "BANCO FINANSUR S.A."
    assert plazo.fechaInformacion == "2017-06-08"
    assert plazo.nombreCompleto == "PLAZO FIJO"
    assert plazo.nombreCorto == "P. FIJO"
    assert plazo.denominacion == "Pesos"
    assert plazo.montoMinimoInvertir == 5000
    assert plazo.plazoMinimoInvertirDias == 30
    assert plazo.canalConstitucion == "Home banking"
    assert plazo.tasaEfectivaAnualMinima == 15.01
    assert plazo.territorioValidez == "Todo el territorio nacional"
    assert data.plazos_fijos[0].denominacion is None
    assert data.plazos_fijos[0].masInformacion is None
    assert plazo.masInformacion == "BONIFICADO"


def test_get_plazos_fijos_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "denominacion": None,
                "montoMinimoInvertir": 1000,
                "plazoMinimoInvertirDias": 1,
                "canalConstitucion": "Línea telefónica",
                "tasaEfectivaAnualMinima": 10.47,
                "codigoEntidad": 303,
                "descripcionEntidad": "BANCO FINANSUR S.A.",
                "fechaInformacion": "2019-07-16",
                "nombreCompleto": "PLAZOFIJOTRADICIONAL",
                "nombreCorto": "PFTRADICIONAL",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_plazos_fijos(codigoEntidad=303)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/PlazosFijos",
        params={"codigoEntidad": 303},
    )
    assert data.plazos_fijos[0].codigoEntidad == 303
    assert len(data.plazos_fijos) == 1


def test_get_plazos_fijos_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_plazos_fijos()

    assert data.plazos_fijos == []


def test_get_plazos_fijos_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_plazos_fijos(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_plazos_fijos_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_plazos_fijos()
    assert exc_info.value.status_code == 500


def test_aget_plazos_fijos(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "denominacion": None,
                "montoMinimoInvertir": 1000,
                "plazoMinimoInvertirDias": 1,
                "canalConstitucion": "Línea telefónica",
                "tasaEfectivaAnualMinima": 10.47,
                "codigoEntidad": 303,
                "descripcionEntidad": "BANCO FINANSUR S.A.",
                "fechaInformacion": "2019-07-16",
                "nombreCompleto": "PLAZOFIJOTRADICIONAL",
                "nombreCorto": "PFTRADICIONAL",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_plazos_fijos(
            codigoEntidad=303
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/PlazosFijos",
        params={"codigoEntidad": 303},
    )
    assert data.plazos_fijos[0].codigoEntidad == 303


def test_aget_plazos_fijos_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_plazos_fijos()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/PlazosFijos", params=None
    )
    assert data.plazos_fijos == []


def test_aget_plazos_fijos_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_plazos_fijos()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_prestamos_prendarios(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "relacionMontoTasacion": 90,
                "destinoFondos": "Adquisición automotores 0 km",
                "montoMinimoOtorgable": 500000,
                "denominacion": "Pesos",
                "montoMaximoOtorgable": 39200000,
                "plazoMaximoOtorgable": 60,
                "ingresoMinimoMensual": 310000,
                "antiguedadLaboralMinimaMeses": 3,
                "edadMaximaSolicitada": 70,
                "relacionCuotaIngreso": 40,
                "beneficiario": "Clientes con cuenta en la entidad",
                "cargoMaximoCancelacionAnticipada": 5,
                "tasaEfectivaAnualMaxima": 72.86,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 93.32,
                "cuotaInicial": 1215,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-04-11",
                "nombreCompleto": "PRESTAMOPRENDARIO",
                "nombreCorto": "PRENDARIO",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": "ANTIGUEDAD PRENDA 0 A 3 AÑOS",
            },
            {
                "relacionMontoTasacion": 90,
                "destinoFondos": "Adquisición automotores 0 km",
                "montoMinimoOtorgable": 500000,
                "denominacion": "UVA",
                "montoMaximoOtorgable": 39200000,
                "plazoMaximoOtorgable": 60,
                "ingresoMinimoMensual": 310000,
                "antiguedadLaboralMinimaMeses": 3,
                "edadMaximaSolicitada": 70,
                "relacionCuotaIngreso": 40,
                "beneficiario": "Clientes con cuenta en la entidad",
                "cargoMaximoCancelacionAnticipada": 5,
                "tasaEfectivaAnualMaxima": 20.75,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 25.57,
                "cuotaInicial": 965,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-04-11",
                "nombreCompleto": "PRESTAMOPRENDARIOUVA",
                "nombreCorto": "PRENDARIOUVA",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": "ANTIGUEDAD PRENDA 0 A 3 AÑOS",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_prestamos_prendarios()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/Prestamos/Prendarios", params=None
    )
    assert len(data.prestamos_prendarios) == 2
    prestamo = data.prestamos_prendarios[1]
    assert prestamo.relacionMontoTasacion == 90
    assert prestamo.destinoFondos == "Adquisición automotores 0 km"
    assert prestamo.montoMinimoOtorgable == 500000
    assert prestamo.denominacion == "UVA"
    assert prestamo.montoMaximoOtorgable == 39200000
    assert prestamo.plazoMaximoOtorgable == 60
    assert prestamo.ingresoMinimoMensual == 310000
    assert prestamo.antiguedadLaboralMinimaMeses == 3
    assert prestamo.edadMaximaSolicitada == 70
    assert prestamo.relacionCuotaIngreso == 40
    assert prestamo.beneficiario == "Clientes con cuenta en la entidad"
    assert prestamo.cargoMaximoCancelacionAnticipada == 5
    assert prestamo.tasaEfectivaAnualMaxima == 20.75
    assert prestamo.tipoTasa == "Fija"
    assert prestamo.costoFinancieroEfectivoTotalMaximo == 25.57
    assert prestamo.cuotaInicial == 965
    assert prestamo.codigoEntidad == 7
    assert prestamo.descripcionEntidad == "BANCO DE GALICIA Y BUENOS AIRES S.A."
    assert prestamo.fechaInformacion == "2025-04-11"
    assert prestamo.nombreCompleto == "PRESTAMOPRENDARIOUVA"
    assert prestamo.nombreCorto == "PRENDARIOUVA"
    assert prestamo.territorioValidez == "Todo el territorio nacional"
    assert prestamo.masInformacion == "ANTIGUEDAD PRENDA 0 A 3 AÑOS"


def test_get_prestamos_prendarios_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "relacionMontoTasacion": 70,
                "destinoFondos": "Adquisición para capital de trabajo",
                "montoMinimoOtorgable": 15000,
                "denominacion": "Dólares estadounidenses",
                "montoMaximoOtorgable": 10266281,
                "plazoMaximoOtorgable": 60,
                "ingresoMinimoMensual": 0,
                "antiguedadLaboralMinimaMeses": 36,
                "edadMaximaSolicitada": 100,
                "relacionCuotaIngreso": 25,
                "beneficiario": "MiPyMEs",
                "cargoMaximoCancelacionAnticipada": 2,
                "tasaEfectivaAnualMaxima": 5.04,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 5.79,
                "cuotaInicial": 1200,
                "codigoEntidad": 44096,
                "descripcionEntidad": "JOHN DEERE CREDIT COMPAÑÍA FINANCIERA S.A.",
                "fechaInformacion": "2025-12-01",
                "nombreCompleto": "PRENDARIO NUEVO USD FIJA 4,90",
                "nombreCorto": "5PDNU PN USD 4,90",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_prestamos_prendarios(codigoEntidad=44096)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/Prestamos/Prendarios",
        params={"codigoEntidad": 44096},
    )
    assert data.prestamos_prendarios[0].codigoEntidad == 44096
    assert len(data.prestamos_prendarios) == 1


def test_get_prestamos_prendarios_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_prestamos_prendarios()

    assert data.prestamos_prendarios == []


def test_get_prestamos_prendarios_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_prestamos_prendarios(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_prestamos_prendarios_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_prestamos_prendarios()
    assert exc_info.value.status_code == 500


def test_aget_prestamos_prendarios(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "relacionMontoTasacion": 90,
                "destinoFondos": "Adquisición automotores 0 km",
                "montoMinimoOtorgable": 500000,
                "denominacion": "Pesos",
                "montoMaximoOtorgable": 39200000,
                "plazoMaximoOtorgable": 60,
                "ingresoMinimoMensual": 310000,
                "antiguedadLaboralMinimaMeses": 3,
                "edadMaximaSolicitada": 70,
                "relacionCuotaIngreso": 40,
                "beneficiario": "Clientes con cuenta en la entidad",
                "cargoMaximoCancelacionAnticipada": 5,
                "tasaEfectivaAnualMaxima": 72.86,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 93.32,
                "cuotaInicial": 1215,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-04-11",
                "nombreCompleto": "PRESTAMOPRENDARIO",
                "nombreCorto": "PRENDARIO",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_prestamos_prendarios(
            codigoEntidad=7
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/Prestamos/Prendarios",
        params={"codigoEntidad": 7},
    )
    assert data.prestamos_prendarios[0].codigoEntidad == 7


def test_aget_prestamos_prendarios_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_prestamos_prendarios()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/Prestamos/Prendarios", params=None
    )
    assert data.prestamos_prendarios == []


def test_aget_prestamos_prendarios_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_prestamos_prendarios()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_prestamos_hipotecarios(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "relacionMontoTasacion": 70,
                "destinoFondos": "Vivienda propia, única y permanente",
                "denominacion": "Pesos",
                "montoMaximoOtorgable": 1000000,
                "plazoMaximoOtorgable": 120,
                "ingresoMinimoMensual": 26000,
                "antiguedadLaboralMinimaMeses": 12,
                "edadMaximaSolicitada": 76,
                "relacionCuotaIngreso": 35,
                "beneficiario": "Todos los beneficiarios",
                "cargoMaximoCancelacionAnticipada": 3,
                "tasaEfectivaAnualMaxima": 69.47,
                "tipoTasa": "Variable",
                "costoFinancieroEfectivoTotalMaximo": 69.47,
                "cuotaInicial": 4615.88,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.U.",
                "fechaInformacion": "2019-07-17",
                "nombreCompleto": "PRESTAMOHIPOTECARIOTRADICIONALCOMPRADEVIVIENDA",
                "nombreCorto": "PRESTHIPOTRADICIONAL",
                "territorioValidez": "0",
                "masInformacion": None,
            },
            {
                "relacionMontoTasacion": 70,
                "destinoFondos": "Vivienda propia, única y permanente",
                "denominacion": "UVA",
                "montoMaximoOtorgable": 5000000,
                "plazoMaximoOtorgable": 360,
                "ingresoMinimoMensual": 0,
                "antiguedadLaboralMinimaMeses": 24,
                "edadMaximaSolicitada": 64,
                "relacionCuotaIngreso": 25,
                "beneficiario": "Empleados públicos",
                "cargoMaximoCancelacionAnticipada": 3,
                "tasaEfectivaAnualMaxima": 8.19,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 8.33,
                "cuotaInicial": 719.3,
                "codigoEntidad": 93,
                "descripcionEntidad": "BANCO DE LA PAMPA SOCIEDAD DE ECONOMÍA MIXTA",
                "fechaInformacion": "2018-05-04",
                "nombreCompleto": "PRESTAMO HIPOTECARIO UVA",
                "nombreCorto": "SEGM SUELDOS II",
                "territorioValidez": "4",
                "masInformacion": "EL CFT NO INCLUYE SEGURO CONTRA DANOS A LA PROPIEDAD",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_prestamos_hipotecarios()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/Prestamos/Hipotecarios", params=None
    )
    assert len(data.prestamos_hipotecarios) == 2
    prestamo = data.prestamos_hipotecarios[1]
    assert prestamo.relacionMontoTasacion == 70
    assert prestamo.destinoFondos == "Vivienda propia, única y permanente"
    assert prestamo.denominacion == "UVA"
    assert prestamo.montoMaximoOtorgable == 5000000
    assert prestamo.plazoMaximoOtorgable == 360
    assert prestamo.ingresoMinimoMensual == 0
    assert prestamo.antiguedadLaboralMinimaMeses == 24
    assert prestamo.edadMaximaSolicitada == 64
    assert prestamo.relacionCuotaIngreso == 25
    assert prestamo.beneficiario == "Empleados públicos"
    assert prestamo.cargoMaximoCancelacionAnticipada == 3
    assert prestamo.tasaEfectivaAnualMaxima == 8.19
    assert prestamo.tipoTasa == "Fija"
    assert prestamo.costoFinancieroEfectivoTotalMaximo == 8.33
    assert prestamo.cuotaInicial == 719.3
    assert prestamo.codigoEntidad == 93
    assert prestamo.descripcionEntidad == "BANCO DE LA PAMPA SOCIEDAD DE ECONOMÍA MIXTA"
    assert prestamo.fechaInformacion == "2018-05-04"
    assert prestamo.nombreCompleto == "PRESTAMO HIPOTECARIO UVA"
    assert prestamo.nombreCorto == "SEGM SUELDOS II"
    assert prestamo.territorioValidez == "4"
    assert (
        prestamo.masInformacion
        == "EL CFT NO INCLUYE SEGURO CONTRA DANOS A LA PROPIEDAD"
    )
    assert data.prestamos_hipotecarios[0].masInformacion is None


def test_get_prestamos_hipotecarios_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "relacionMontoTasacion": 70,
                "destinoFondos": "Vivienda propia, única y permanente",
                "denominacion": "UVA",
                "montoMaximoOtorgable": 5000000,
                "plazoMaximoOtorgable": 360,
                "ingresoMinimoMensual": 0,
                "antiguedadLaboralMinimaMeses": 24,
                "edadMaximaSolicitada": 64,
                "relacionCuotaIngreso": 25,
                "beneficiario": "Empleados públicos",
                "cargoMaximoCancelacionAnticipada": 3,
                "tasaEfectivaAnualMaxima": 8.19,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 8.33,
                "cuotaInicial": 719.3,
                "codigoEntidad": 93,
                "descripcionEntidad": "BANCO DE LA PAMPA SOCIEDAD DE ECONOMÍA MIXTA",
                "fechaInformacion": "2018-05-04",
                "nombreCompleto": "PRESTAMO HIPOTECARIO UVA",
                "nombreCorto": "SEGM SUELDOS II",
                "territorioValidez": "4",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_prestamos_hipotecarios(codigoEntidad=93)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/Prestamos/Hipotecarios",
        params={"codigoEntidad": 93},
    )
    assert data.prestamos_hipotecarios[0].codigoEntidad == 93
    assert len(data.prestamos_hipotecarios) == 1


def test_get_prestamos_hipotecarios_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_prestamos_hipotecarios()

    assert data.prestamos_hipotecarios == []


def test_get_prestamos_hipotecarios_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_prestamos_hipotecarios(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_prestamos_hipotecarios_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_prestamos_hipotecarios()
    assert exc_info.value.status_code == 500


def test_aget_prestamos_hipotecarios(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "relacionMontoTasacion": 70,
                "destinoFondos": "Vivienda propia, única y permanente",
                "denominacion": "UVA",
                "montoMaximoOtorgable": 5000000,
                "plazoMaximoOtorgable": 360,
                "ingresoMinimoMensual": 0,
                "antiguedadLaboralMinimaMeses": 24,
                "edadMaximaSolicitada": 64,
                "relacionCuotaIngreso": 25,
                "beneficiario": "Empleados públicos",
                "cargoMaximoCancelacionAnticipada": 3,
                "tasaEfectivaAnualMaxima": 8.19,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 8.33,
                "cuotaInicial": 719.3,
                "codigoEntidad": 93,
                "descripcionEntidad": "BANCO DE LA PAMPA SOCIEDAD DE ECONOMÍA MIXTA",
                "fechaInformacion": "2018-05-04",
                "nombreCompleto": "PRESTAMO HIPOTECARIO UVA",
                "nombreCorto": "SEGM SUELDOS II",
                "territorioValidez": "4",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_prestamos_hipotecarios(
            codigoEntidad=93
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/Prestamos/Hipotecarios",
        params={"codigoEntidad": 93},
    )
    assert data.prestamos_hipotecarios[0].codigoEntidad == 93


def test_aget_prestamos_hipotecarios_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_prestamos_hipotecarios()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/Prestamos/Hipotecarios", params=None
    )
    assert data.prestamos_hipotecarios == []


def test_aget_prestamos_hipotecarios_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_prestamos_hipotecarios()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_prestamos_personales(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "montoMinimoOtorgable": 500,
                "denominacion": "UVA",
                "montoMaximoOtorgable": 2000000,
                "plazoMaximoOtorgable": 24,
                "ingresoMinimoMensual": 310000,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 80,
                "relacionCuotaIngreso": 30,
                "beneficiario": "Todos los beneficiarios",
                "cargoMaximoCancelacionAnticipada": 4,
                "tasaEfectivaAnualMaxima": 29.33,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 36.42,
                "cuotaInicial": 956,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-08-19",
                "nombreCompleto": "PRESTAMOPERSONALUVA",
                "nombreCorto": "PPUVA",
                "territorioValidez": "0",
                "masInformacion": None,
            },
            {
                "montoMinimoOtorgable": 5000,
                "denominacion": "Pesos",
                "montoMaximoOtorgable": 100000,
                "plazoMaximoOtorgable": 12,
                "ingresoMinimoMensual": 70000,
                "antiguedadLaboralMinimaMeses": 12,
                "edadMaximaSolicitada": 65,
                "relacionCuotaIngreso": 20,
                "beneficiario": "Personas humanas Monotributistas",
                "cargoMaximoCancelacionAnticipada": 0,
                "tasaEfectivaAnualMaxima": 264,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 267.67,
                "cuotaInicial": 0,
                "codigoEntidad": 55236,
                "descripcionEntidad": "Dourat S.R.L.",
                "fechaInformacion": "2023-05-29",
                "nombreCompleto": "MONOTRIBUTOEFECTIVO",
                "nombreCorto": "MVSE2",
                "territorioValidez": "2",
                "masInformacion": None,
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_prestamos_personales()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/Prestamos/Personales", params=None
    )
    assert len(data.prestamos_personales) == 2
    prestamo = data.prestamos_personales[0]
    assert prestamo.montoMinimoOtorgable == 500
    assert prestamo.denominacion == "UVA"
    assert prestamo.montoMaximoOtorgable == 2000000
    assert prestamo.plazoMaximoOtorgable == 24
    assert prestamo.ingresoMinimoMensual == 310000
    assert prestamo.antiguedadLaboralMinimaMeses == 0
    assert prestamo.edadMaximaSolicitada == 80
    assert prestamo.relacionCuotaIngreso == 30
    assert prestamo.beneficiario == "Todos los beneficiarios"
    assert prestamo.cargoMaximoCancelacionAnticipada == 4
    assert prestamo.tasaEfectivaAnualMaxima == 29.33
    assert prestamo.tipoTasa == "Fija"
    assert prestamo.costoFinancieroEfectivoTotalMaximo == 36.42
    assert prestamo.cuotaInicial == 956
    assert prestamo.codigoEntidad == 7
    assert prestamo.descripcionEntidad == "BANCO DE GALICIA Y BUENOS AIRES S.A."
    assert prestamo.fechaInformacion == "2025-08-19"
    assert prestamo.nombreCompleto == "PRESTAMOPERSONALUVA"
    assert prestamo.nombreCorto == "PPUVA"
    assert prestamo.territorioValidez == "0"
    assert prestamo.masInformacion is None
    assert data.prestamos_personales[1].codigoEntidad == 55236
    assert data.prestamos_personales[1].descripcionEntidad == "Dourat S.R.L."


def test_get_prestamos_personales_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "montoMinimoOtorgable": 5000,
                "denominacion": "Pesos",
                "montoMaximoOtorgable": 100000,
                "plazoMaximoOtorgable": 12,
                "ingresoMinimoMensual": 70000,
                "antiguedadLaboralMinimaMeses": 12,
                "edadMaximaSolicitada": 65,
                "relacionCuotaIngreso": 20,
                "beneficiario": "Personas humanas Monotributistas",
                "cargoMaximoCancelacionAnticipada": 0,
                "tasaEfectivaAnualMaxima": 264,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 267.67,
                "cuotaInicial": 0,
                "codigoEntidad": 55236,
                "descripcionEntidad": "Dourat S.R.L.",
                "fechaInformacion": "2023-05-29",
                "nombreCompleto": "MONOTRIBUTOEFECTIVO",
                "nombreCorto": "MVSE2",
                "territorioValidez": "2",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_prestamos_personales(codigoEntidad=55236)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/Prestamos/Personales",
        params={"codigoEntidad": 55236},
    )
    assert data.prestamos_personales[0].codigoEntidad == 55236
    assert len(data.prestamos_personales) == 1


def test_get_prestamos_personales_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_prestamos_personales()

    assert data.prestamos_personales == []


def test_get_prestamos_personales_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_prestamos_personales(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_prestamos_personales_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_prestamos_personales()
    assert exc_info.value.status_code == 500


def test_aget_prestamos_personales(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "montoMinimoOtorgable": 500,
                "denominacion": "UVA",
                "montoMaximoOtorgable": 2000000,
                "plazoMaximoOtorgable": 24,
                "ingresoMinimoMensual": 310000,
                "antiguedadLaboralMinimaMeses": 0,
                "edadMaximaSolicitada": 80,
                "relacionCuotaIngreso": 30,
                "beneficiario": "Todos los beneficiarios",
                "cargoMaximoCancelacionAnticipada": 4,
                "tasaEfectivaAnualMaxima": 29.33,
                "tipoTasa": "Fija",
                "costoFinancieroEfectivoTotalMaximo": 36.42,
                "cuotaInicial": 956,
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-08-19",
                "nombreCompleto": "PRESTAMOPERSONALUVA",
                "nombreCorto": "PPUVA",
                "territorioValidez": "0",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_prestamos_personales(
            codigoEntidad=7
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/Prestamos/Personales",
        params={"codigoEntidad": 7},
    )
    assert data.prestamos_personales[0].codigoEntidad == 7


def test_aget_prestamos_personales_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_prestamos_personales()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/Prestamos/Personales", params=None
    )
    assert data.prestamos_personales == []


def test_aget_prestamos_personales_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_prestamos_personales()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500


def test_get_tarjetas_credito(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "comisionMaximaAdministracionMantenimiento": 31500,
                "comisionMaximaRenovacion": 457600,
                "tasaEfectivaAnualMaximaFinanciacion": 184.5,
                "tasaEfectivaAnualMaximaAdelantoEfectivo": 184.5,
                "ingresoMinimoMensual": 999999,
                "antiguedadLaboralMinimaMeses": 6,
                "edadMaximaSolicitada": 100,
                "segmento": "Premium gold",
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-11-17",
                "nombreCompleto": "AMERICAN EXPRESS PLATINUM",
                "nombreCorto": "AMEX PLATINUM",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": "EL INGRESO MENSUAL MINIMO ES 2.150.000 PESOS",
            },
            {
                "comisionMaximaAdministracionMantenimiento": 21500,
                "comisionMaximaRenovacion": 326000,
                "tasaEfectivaAnualMaximaFinanciacion": 184.5,
                "tasaEfectivaAnualMaximaAdelantoEfectivo": 184.5,
                "ingresoMinimoMensual": 900000,
                "antiguedadLaboralMinimaMeses": 6,
                "edadMaximaSolicitada": 100,
                "segmento": "Premium gold",
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-11-17",
                "nombreCompleto": "VISA GOLD",
                "nombreCorto": "VISA GOLD",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": "0",
            },
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_tarjetas_credito()

    mock_request.assert_called_once_with(
        "GET", "/transparencia/v1.0/TarjetasCredito", params=None
    )
    assert len(data.tarjetas_credito) == 2
    tarjeta = data.tarjetas_credito[0]
    assert tarjeta.comisionMaximaAdministracionMantenimiento == 31500
    assert tarjeta.comisionMaximaRenovacion == 457600
    assert tarjeta.tasaEfectivaAnualMaximaFinanciacion == 184.5
    assert tarjeta.tasaEfectivaAnualMaximaAdelantoEfectivo == 184.5
    assert tarjeta.ingresoMinimoMensual == 999999
    assert tarjeta.antiguedadLaboralMinimaMeses == 6
    assert tarjeta.edadMaximaSolicitada == 100
    assert tarjeta.segmento == "Premium gold"
    assert tarjeta.codigoEntidad == 7
    assert tarjeta.descripcionEntidad == "BANCO DE GALICIA Y BUENOS AIRES S.A."
    assert tarjeta.fechaInformacion == "2025-11-17"
    assert tarjeta.nombreCompleto == "AMERICAN EXPRESS PLATINUM"
    assert tarjeta.nombreCorto == "AMEX PLATINUM"
    assert tarjeta.territorioValidez == "Todo el territorio nacional"
    assert tarjeta.masInformacion == "EL INGRESO MENSUAL MINIMO ES 2.150.000 PESOS"
    assert data.tarjetas_credito[1].nombreCorto == "VISA GOLD"


def test_get_tarjetas_credito_con_codigo_entidad(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "comisionMaximaAdministracionMantenimiento": 7982.7,
                "comisionMaximaRenovacion": 93444.97,
                "tasaEfectivaAnualMaximaFinanciacion": 171.27,
                "tasaEfectivaAnualMaximaAdelantoEfectivo": 171.27,
                "ingresoMinimoMensual": 900,
                "antiguedadLaboralMinimaMeses": 3,
                "edadMaximaSolicitada": 80,
                "segmento": "Internacional",
                "codigoEntidad": 341,
                "descripcionEntidad": "BANCO MASVENTAS S.A.",
                "fechaInformacion": "2025-10-03",
                "nombreCompleto": "000DVISA INTERNACIONAL",
                "nombreCorto": "VISA INT",
                "territorioValidez": "Provincia de Salta",
                "masInformacion": "000A",
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_request = MagicMock(return_value=mock_response)

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    data = client.regimen_de_transparencia.get_tarjetas_credito(codigoEntidad=341)

    mock_request.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/TarjetasCredito",
        params={"codigoEntidad": 341},
    )
    assert data.tarjetas_credito[0].codigoEntidad == 341
    assert len(data.tarjetas_credito) == 1


def test_get_tarjetas_credito_vacio(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.regimen_de_transparencia._t,
        "request",
        MagicMock(return_value=mock_response),
    )

    data = client.regimen_de_transparencia.get_tarjetas_credito()

    assert data.tarjetas_credito == []


def test_get_tarjetas_credito_404(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 404,
        "errorMessages": ["No se encontraron datos para su consulta."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(404, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_tarjetas_credito(codigoEntidad=999999)
    assert exc_info.value.status_code == 404
    assert "No se encontraron datos para su consulta." in exc_info.value.message


def test_get_tarjetas_credito_500(client, monkeypatch):
    fake_data: dict[str, Any] = {
        "status": 500,
        "errorMessages": ["Ocurrió un error al procesar la solicitud."],
    }

    def mock_request(*args, **kwargs):
        raise BCRAHTTPError(500, fake_data["errorMessages"][0])

    monkeypatch.setattr(client.regimen_de_transparencia._t, "request", mock_request)

    with pytest.raises(BCRAHTTPError) as exc_info:
        client.regimen_de_transparencia.get_tarjetas_credito()
    assert exc_info.value.status_code == 500


def test_aget_tarjetas_credito(client, monkeypatch):
    fake_data = {
        "status": 200,
        "results": [
            {
                "comisionMaximaAdministracionMantenimiento": 31500,
                "comisionMaximaRenovacion": 457600,
                "tasaEfectivaAnualMaximaFinanciacion": 184.5,
                "tasaEfectivaAnualMaximaAdelantoEfectivo": 184.5,
                "ingresoMinimoMensual": 999999,
                "antiguedadLaboralMinimaMeses": 6,
                "edadMaximaSolicitada": 100,
                "segmento": "Premium gold",
                "codigoEntidad": 7,
                "descripcionEntidad": "BANCO DE GALICIA Y BUENOS AIRES S.A.",
                "fechaInformacion": "2025-11-17",
                "nombreCompleto": "AMERICAN EXPRESS PLATINUM",
                "nombreCorto": "AMEX PLATINUM",
                "territorioValidez": "Todo el territorio nacional",
                "masInformacion": None,
            }
        ],
    }
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_tarjetas_credito(
            codigoEntidad=7
        )

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET",
        "/transparencia/v1.0/TarjetasCredito",
        params={"codigoEntidad": 7},
    )
    assert data.tarjetas_credito[0].codigoEntidad == 7
    assert data.tarjetas_credito[0].masInformacion is None


def test_aget_tarjetas_credito_sin_filtro(client, monkeypatch):
    fake_data = {"status": 200, "results": []}
    mock_response = httpx.Response(200, json=fake_data)
    mock_arequest = AsyncMock(return_value=mock_response)
    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        return await client.regimen_de_transparencia.aget_tarjetas_credito()

    data = asyncio.run(run())

    mock_arequest.assert_called_once_with(
        "GET", "/transparencia/v1.0/TarjetasCredito", params=None
    )
    assert data.tarjetas_credito == []


def test_aget_tarjetas_credito_500(client, monkeypatch):
    async def mock_arequest(*args, **kwargs):
        raise BCRAHTTPError(500, "Ocurrió un error al procesar la solicitud.")

    monkeypatch.setattr(client.regimen_de_transparencia._t, "arequest", mock_arequest)

    async def run():
        await client.regimen_de_transparencia.aget_tarjetas_credito()

    with pytest.raises(BCRAHTTPError) as exc_info:
        asyncio.run(run())
    assert exc_info.value.status_code == 500
