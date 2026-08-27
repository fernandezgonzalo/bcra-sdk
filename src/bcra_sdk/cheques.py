import logging

from ._base import Resource
from .models.denunciados import ResultGetChequeDenunciadoV1
from .models.entidades import ResultGetEntidadesV1

logger = logging.getLogger("bcra_sdk.cheques")


class Cheques(Resource):
    def __init__(self, transport):
        super().__init__(transport)
        self._register_version(
            "get_entidades",
            "1.0",
            path="/cheques/v1.0/entidades",
            model=ResultGetEntidadesV1,
        )
        self._register_version(
            "get_cheque_denunciado",
            "1.0",
            path="/cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}",
            model=ResultGetChequeDenunciadoV1,
        )

    def get_entidades(self, *, version: str | None = None) -> ResultGetEntidadesV1:
        spec = self._resolve_version("get_entidades", version)
        logger.info("Consultando entidades bancarias")
        r = self._t.request("GET", spec.path)
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Entidades obtenidas: total=%d",
            len(result.entidades),
        )
        return result

    def get_cheque_denunciado(
        self,
        codigo_entidad: int,
        numero_cheque: int,
        *,
        version: str | None = None,
    ) -> ResultGetChequeDenunciadoV1:
        spec = self._resolve_version("get_cheque_denunciado", version)
        logger.info(
            "Consultando cheque denunciado: entidad=%s, cheque=%s",
            codigo_entidad,
            numero_cheque,
        )
        r = self._t.request(
            "GET",
            spec.path.format(
                codigo_entidad=codigo_entidad, numero_cheque=numero_cheque
            ),
        )
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Cheque %s: denunciado=%s, detalles=%d",
            result.numeroCheque,
            result.denunciado,
            len(result.detalles),
        )
        return result
