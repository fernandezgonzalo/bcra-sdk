import logging

from ._base import Resource, endpoint
from .models.entidades import ResultGetEntidadesV1

logger = logging.getLogger("bcra_sdk.cheques")


class Cheques(Resource):
    @endpoint(version="1.0", name="get_entidades")
    def get_entidades_v1(self) -> ResultGetEntidadesV1:
        logger.info("Consultando entidades bancarias")
        r = self._t.request("GET", "/cheques/v1.0/entidades")
        result = ResultGetEntidadesV1.from_dict(r.json()["results"])
        logger.debug(
            "Entidades obtenidas: total=%d",
            len(result.entidades),
        )
        return result
