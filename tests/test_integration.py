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
