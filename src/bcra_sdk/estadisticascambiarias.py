import logging

from ._base import Resource, endpoint
from .models.divisas import ResultGetDivisasV1

logger = logging.getLogger("bcra_sdk.estadisticas_cambiarias")


class EstadisticasCambiarias(Resource):
    @endpoint(version="1.0", name="get_divisas")
    def get_divisas_v1(self) -> ResultGetDivisasV1:
        logger.info("Consultando divisas")
        r = self._t.request("GET", "/estadisticascambiarias/v1.0/Maestros/Divisas")
        result = ResultGetDivisasV1.from_dict(r.json()["results"])
        logger.debug(
            "Divisas obtenidas: total=%d",
            len(result.divisas),
        )
        return result
