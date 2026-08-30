import pytest

from bcra_sdk import BCRAClient
from bcra_sdk.exceptions import BCRAHTTPError

pytestmark = pytest.mark.integration

CUIT_SIN_DATOS = "20111111112"
FECHA_REFERENCIA = "2024-06-12"


def test_integration_get_divisas():
    with BCRAClient() as bcra:
        data = bcra.estadisticas_cambiarias.get_divisas()
    assert len(data.divisas) >= 10


def test_integration_get_cotizaciones():
    with BCRAClient() as bcra:
        data = bcra.estadisticas_cambiarias.get_cotizaciones(fecha=FECHA_REFERENCIA)
    assert data.fecha == FECHA_REFERENCIA
    assert data.detalle


def test_integration_get_evolucion_moneda():
    with BCRAClient() as bcra:
        data = bcra.estadisticas_cambiarias.get_evolucion_moneda(
            moneda="USD",
            fechadesde="2024-06-10",
            fechahasta="2024-06-12",
            limit=10,
        )
    assert data.resultset.count >= 1
    assert data.cotizaciones


def test_integration_get_entidades():
    with BCRAClient() as bcra:
        data = bcra.cheques.get_entidades()
    assert data.entidades


def test_integration_get_cajas_ahorros():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_cajas_ahorros(codigoEntidad=11)
    assert data.cajas_ahorros
    assert data.cajas_ahorros[0].codigoEntidad == 11


def test_integration_get_paquetes_productos():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_paquetes_productos(codigoEntidad=14)
    assert data.paquetes_productos
    assert data.paquetes_productos[0].codigoEntidad == 14


def test_integration_get_plazos_fijos():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_plazos_fijos(codigoEntidad=7)
    assert data.plazos_fijos
    assert data.plazos_fijos[0].codigoEntidad == 7


def test_integration_get_prestamos_prendarios():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_prestamos_prendarios(codigoEntidad=7)
    assert data.prestamos_prendarios
    assert data.prestamos_prendarios[0].codigoEntidad == 7


def test_integration_get_prestamos_hipotecarios():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_prestamos_hipotecarios(codigoEntidad=7)
    assert data.prestamos_hipotecarios
    assert data.prestamos_hipotecarios[0].codigoEntidad == 7


def test_integration_get_prestamos_personales():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_prestamos_personales(codigoEntidad=7)
    assert data.prestamos_personales
    assert data.prestamos_personales[0].codigoEntidad == 7


def test_integration_get_tarjetas_credito():
    with BCRAClient() as bcra:
        data = bcra.regimen_de_transparencia.get_tarjetas_credito(codigoEntidad=7)
    assert data.tarjetas_credito
    assert data.tarjetas_credito[0].codigoEntidad == 7


def test_integration_get_monetarias():
    with BCRAClient() as bcra:
        data = bcra.monetarias.get_monetarias()
    assert data.resultset.count >= 1
    assert data.variables


def test_integration_get_evolucion_variable():
    with BCRAClient() as bcra:
        data = bcra.monetarias.get_evolucion_variable(
            idVariable=1,
            desde="2025-05-20",
            hasta="2025-05-26",
            limit=5,
        )
    assert data.resultset.count >= 1
    assert data.series[0].idVariable == 1
    assert data.series[0].detalle


def test_integration_get_metodologias():
    with BCRAClient() as bcra:
        data = bcra.monetarias.get_metodologias(limit=5)
    assert data.resultset.count >= 1
    assert data.metodologias


def test_integration_get_metodologia():
    with BCRAClient() as bcra:
        data = bcra.monetarias.get_metodologia(idVariable=1)
    assert data.metodologia.id == 1
    assert data.metodologia.detalle


def test_integration_get_deudas_sin_datos():
    with BCRAClient() as bcra, pytest.raises(BCRAHTTPError) as exc_info:
        bcra.deudores.get_deudas(cuit=CUIT_SIN_DATOS)
    assert exc_info.value.status_code == 404


def test_integration_get_cheque_denunciado():
    with BCRAClient() as bcra:
        data = bcra.cheques.get_cheque_denunciado(
            codigo_entidad=17, numero_cheque=752395
        )
    assert data.numeroCheque == 752395
    assert data.denunciado is False
