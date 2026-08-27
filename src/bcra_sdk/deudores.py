import logging

from ._base import Resource
from .models.cheques import ResultGetChequesRechazadosV1
from .models.deudores import ResultGetDeudasHistoricasV1, ResultGetDeudasV1

logger = logging.getLogger("bcra_sdk.deudores")


class Deudores(Resource):
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
