import logging
import re

from ._base import Resource
from .models.cheques import ResultGetChequesRechazadosV1
from .models.deudores import ResultGetDeudasHistoricasV1, ResultGetDeudasV1

logger = logging.getLogger("bcra_sdk.deudores")

_CUIT_RE = re.compile(r"^\d{2}-?\d{8}-?\d$")


def _normalize_cuit(cuit: str) -> str:
    if not _CUIT_RE.fullmatch(cuit):
        raise ValueError(
            f"CUIT inválido: {cuit!r}. Debe contener 11 dígitos (ej. '20111111112')."
        )
    return cuit.replace("-", "")


class Deudores(Resource):
    """Endpoints de la Central de Deudores del BCRA.

    Expuesto como ``client.deudores``. Incluye la situación de deudas por
    CUIT, el histórico y los cheques rechazados de un identificador.
    """

    def __init__(self, transport):
        super().__init__(transport)
        self._register_version(
            "get_deudas",
            "1.0",
            path="/centraldedeudores/v1.0/Deudas/{cuit}",
            model=ResultGetDeudasV1,
        )
        self._register_version(
            "get_deudas_historicas",
            "1.0",
            path="/CentralDeDeudores/v1.0/Deudas/Historicas/{identification}",
            model=ResultGetDeudasHistoricasV1,
        )
        self._register_version(
            "get_cheques_rechazados",
            "1.0",
            path="/centraldedeudores/v1.0/Deudas/ChequesRechazados/{identification}",
            model=ResultGetChequesRechazadosV1,
        )

    def get_deudas(self, cuit: str, *, version: str | None = None) -> ResultGetDeudasV1:
        """Devuelve la situación de deudas vigente de una persona o empresa.

        Args:
            cuit: CUIT de 11 dígitos; se aceptan los guiones opcionales
                (``20-11111111-2`` o ``20111111112``).
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetDeudasV1: identificación y el detalle por
                `Periodo`/`Entidad`.

        Raises:
            ValueError: si el CUIT no tiene un formato válido.
            BCRAHTTPError: si la API responde con error (por ejemplo, 404
                cuando el CUIT no tiene datos cargados).
        """
        cuit = _normalize_cuit(cuit)
        logger.info("Consultando deudas para CUIT %s", cuit)
        result = self._fetch(
            self._t.request,
            endpoint="get_deudas",
            version=version,
            path_vars={"cuit": cuit},
            model=ResultGetDeudasV1,
        )
        logger.debug(
            "Deudas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    async def aget_deudas(
        self, cuit: str, *, version: str | None = None
    ) -> ResultGetDeudasV1:
        """Versión asíncrona de `get_deudas`."""
        cuit = _normalize_cuit(cuit)
        logger.info("Consultando deudas para CUIT %s", cuit)
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_deudas",
            version=version,
            path_vars={"cuit": cuit},
            model=ResultGetDeudasV1,
        )
        logger.debug(
            "Deudas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    def get_deudas_historicas(
        self, identification: str, *, version: str | None = None
    ) -> ResultGetDeudasHistoricasV1:
        """Devuelve el histórico de deudas de un identificador.

        Args:
            identification: Identificador (CUIT o CUIL) a consultar.
            version: Versión del endpoint a usar. El default es la más
                reciente.

        Returns:
            ResultGetDeudasHistoricasV1: identificación y el histórico por
                `PeriodoHistorica`/`EntidadHistorica`.

        Raises:
            BCRAHTTPError: si la API responde con error (por ejemplo, 404
                cuando el identificador no tiene datos cargados).
        """
        logger.info(
            "Consultando deudas históricas para identificación %s", identification
        )
        result = self._fetch(
            self._t.request,
            endpoint="get_deudas_historicas",
            version=version,
            path_vars={"identification": identification},
            model=ResultGetDeudasHistoricasV1,
        )
        logger.debug(
            "Deudas históricas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    async def aget_deudas_historicas(
        self, identification: str, *, version: str | None = None
    ) -> ResultGetDeudasHistoricasV1:
        """Versión asíncrona de `get_deudas_historicas`."""
        logger.info(
            "Consultando deudas históricas para identificación %s", identification
        )
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_deudas_historicas",
            version=version,
            path_vars={"identification": identification},
            model=ResultGetDeudasHistoricasV1,
        )
        logger.debug(
            "Deudas históricas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    def get_cheques_rechazados(
        self, identification: str, *, version: str | None = None
    ) -> ResultGetChequesRechazadosV1:
        """Devuelve los cheques rechazados de un identificador.

        Args:
            identification: Identificador (CUIT o CUIL) a consultar.
            version: Versión del endpoint a usar. El default es la más
                reciente.

        Returns:
            ResultGetChequesRechazadosV1: los causales de rechazo con sus
                `Causal`/`EntidadCheque`.

        Raises:
            BCRAHTTPError: si la API responde con error (por ejemplo, 404
                cuando el identificador no tiene datos cargados).
        """
        logger.info("Consultando cheques rechazados para %s", identification)
        result = self._fetch(
            self._t.request,
            endpoint="get_cheques_rechazados",
            version=version,
            path_vars={"identification": identification},
            model=ResultGetChequesRechazadosV1,
        )
        logger.debug(
            "Cheques rechazados obtenidos: identificacion=%s, causales=%d",
            result.identificacion,
            len(result.causales),
        )
        return result

    async def aget_cheques_rechazados(
        self, identification: str, *, version: str | None = None
    ) -> ResultGetChequesRechazadosV1:
        """Versión asíncrona de `get_cheques_rechazados`."""
        logger.info("Consultando cheques rechazados para %s", identification)
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_cheques_rechazados",
            version=version,
            path_vars={"identification": identification},
            model=ResultGetChequesRechazadosV1,
        )
        logger.debug(
            "Cheques rechazados obtenidos: identificacion=%s, causales=%d",
            result.identificacion,
            len(result.causales),
        )
        return result
