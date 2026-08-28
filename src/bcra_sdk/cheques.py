import logging

from ._base import Resource
from .models.denunciados import ResultGetChequeDenunciadoV1
from .models.entidades import ResultGetEntidadesV1

logger = logging.getLogger("bcra_sdk.cheques")


class Cheques(Resource):
    """Endpoints del sistema de cheques del BCRA.

    Expuesto como ``client.cheques``. Incluye el maestro de entidades
    bancarias y la consulta de cheques denunciados.
    """

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
        """Devuelve el listado de entidades bancarias vigente.

        Args:
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con
                `Resource.versions`.

        Returns:
            ResultGetEntidadesV1: listado de `EntidadBancaria`.
        """
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
        """Versión asíncrona de `get_entidades`."""
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
        """Consulta el estado de denuncia de un cheque.

        Args:
            codigo_entidad: Código de la entidad bancaria (ver
                `get_entidades`).
            numero_cheque: Número del cheque a consultar.
            version: Versión del endpoint a usar. El default es la más
                reciente.

        Returns:
            ResultGetChequeDenunciadoV1: datos del cheque, incluyendo si
                figura como denunciado y sus detalles.
        """
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
        """Versión asíncrona de `get_cheque_denunciado`."""
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
