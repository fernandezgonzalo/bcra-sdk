import logging

from ._base import Resource, endpoint
from .models.denunciados import ResultGetChequeDenunciadoV1
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

    @endpoint(version="1.0", name="get_cheque_denunciado")
    def get_cheque_denunciado_v1(
        self, codigo_entidad: int, numero_cheque: int
    ) -> ResultGetChequeDenunciadoV1:
        logger.info(
            "Consultando cheque denunciado: entidad=%s, cheque=%s",
            codigo_entidad,
            numero_cheque,
        )
        r = self._t.request(
            "GET",
            f"/cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}",
        )
        result = ResultGetChequeDenunciadoV1.from_dict(r.json()["results"])
        logger.debug(
            "Cheque %s: denunciado=%s, detalles=%d",
            result.numeroCheque,
            result.denunciado,
            len(result.detalles),
        )
        return result
