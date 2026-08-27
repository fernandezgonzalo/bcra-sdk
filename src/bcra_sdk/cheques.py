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
        logger.info("Consultando entidades bancarias")
        result = self._fetch(
            self._t.request,
            endpoint="get_entidades",
            version=version,
            model=ResultGetEntidadesV1,
        )
        logger.debug(
            "Entidades obtenidas: total=%d",
            len(result.entidades),
        )
        return result

    async def aget_entidades(
        self, *, version: str | None = None
    ) -> ResultGetEntidadesV1:
        logger.info("Consultando entidades bancarias")
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_entidades",
            version=version,
            model=ResultGetEntidadesV1,
        )
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
        logger.info(
            "Consultando cheque denunciado: entidad=%s, cheque=%s",
            codigo_entidad,
            numero_cheque,
        )
        result = self._fetch(
            self._t.request,
            endpoint="get_cheque_denunciado",
            version=version,
            path_vars={
                "codigo_entidad": codigo_entidad,
                "numero_cheque": numero_cheque,
            },
            model=ResultGetChequeDenunciadoV1,
        )
        logger.debug(
            "Cheque %s: denunciado=%s, detalles=%d",
            result.numeroCheque,
            result.denunciado,
            len(result.detalles),
        )
        return result

    async def aget_cheque_denunciado(
        self,
        codigo_entidad: int,
        numero_cheque: int,
        *,
        version: str | None = None,
    ) -> ResultGetChequeDenunciadoV1:
        logger.info(
            "Consultando cheque denunciado: entidad=%s, cheque=%s",
            codigo_entidad,
            numero_cheque,
        )
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_cheque_denunciado",
            version=version,
            path_vars={
                "codigo_entidad": codigo_entidad,
                "numero_cheque": numero_cheque,
            },
            model=ResultGetChequeDenunciadoV1,
        )
        logger.debug(
            "Cheque %s: denunciado=%s, detalles=%d",
            result.numeroCheque,
            result.denunciado,
            len(result.detalles),
        )
        return result
