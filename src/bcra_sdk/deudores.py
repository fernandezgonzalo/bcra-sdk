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
        spec = self._resolve_version("get_deudas", version)
        logger.info("Consultando deudas para CUIT %s", cuit)
        r = self._t.request("GET", spec.path.format(cuit=cuit))
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Deudas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    def get_deudas_historicas(
        self, identification: str, *, version: str | None = None
    ) -> ResultGetDeudasHistoricasV1:
        spec = self._resolve_version("get_deudas_historicas", version)
        logger.info(
            "Consultando deudas históricas para identificación %s", identification
        )
        r = self._t.request("GET", spec.path.format(identification=identification))
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Deudas históricas obtenidas: identificacion=%s, periodos=%d",
            result.identificacion,
            len(result.periodos),
        )
        return result

    def get_cheques_rechazados(
        self, identification: str, *, version: str | None = None
    ) -> ResultGetChequesRechazadosV1:
        spec = self._resolve_version("get_cheques_rechazados", version)
        logger.info("Consultando cheques rechazados para %s", identification)
        r = self._t.request("GET", spec.path.format(identification=identification))
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Cheques rechazados obtenidos: identificacion=%s, causales=%d",
            result.identificacion,
            len(result.causales),
        )
        return result
