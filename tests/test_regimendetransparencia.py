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
