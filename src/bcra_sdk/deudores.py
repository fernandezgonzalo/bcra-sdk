import logging

from ._base import Resource, endpoint
from .models.cheques import ResultGetChequesRechazadosV1
from .models.deudores import ResultGetDeudasHistoricasV1, ResultGetDeudasV1

logger = logging.getLogger("bcra_sdk.deudores")


class Deudores(Resource):
    @endpoint(version="1.0", name="get_deudas")
    def get_deudas_v1(self, cuit: str) -> ResultGetDeudasV1:
        logger.info("Consultando deudas para CUIT %s", cuit)
        r = self._t.request("GET", f"/centraldedeudores/v1.0/Deudas/{cuit}")
        result = ResultGetDeudasV1.from_dict(r.json()["results"])
        logger.debug(
            "Deudas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    @endpoint(version="1.0", name="get_deudas_historicas")
    def get_deudas_historicas_v1(
        self, identification: str
    ) -> ResultGetDeudasHistoricasV1:
        logger.info(
            "Consultando deudas históricas para identificación %s", identification
        )
        r = self._t.request(
            "GET",
            f"/CentralDeDeudores/v1.0/Deudas/Historicas/{identification}",
        )
        result = ResultGetDeudasHistoricasV1.from_dict(r.json()["results"])
        logger.debug(
            "Deudas históricas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    @endpoint(version="1.0", name="get_cheques_rechazados")
    def get_cheques_rechazados_v1(
        self, identification: str
    ) -> ResultGetChequesRechazadosV1:
        logger.info("Consultando cheques rechazados para %s", identification)
        r = self._t.request(
            "GET",
            f"/centraldedeudores/v1.0/Deudas/ChequesRechazados/{identification}",
        )
        result = ResultGetChequesRechazadosV1.from_dict(r.json()["results"])
        logger.debug(
            "Cheques rechazados obtenidos: identificacion=%s, causales=%d",
            result.identificacion,
            len(result.causales),
        )
        return result
