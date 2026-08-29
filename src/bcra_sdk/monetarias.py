import logging

from ._base import Resource
from .models.monetarias import ResultGetMonetariasV1

logger = logging.getLogger("bcra_sdk.monetarias")


class Monetarias(Resource):
    """Endpoints de estadísticas monetarias del BCRA.

    Expuesto como ``client.monetarias``. Incluye el maestro de variables
    monetarias (``get_monetarias``).
    """

    def __init__(self, transport):
        super().__init__(transport)
        self._register_version(
            "get_monetarias",
            "4.0",
            path="/estadisticas/v4.0/monetarias",
            model=ResultGetMonetariasV1,
        )

    def get_monetarias(self, *, version: str | None = None) -> ResultGetMonetariasV1:
        """Devuelve el listado de variables monetarias del BCRA.

        Args:
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetMonetariasV1: metadatos del paginado via `Resultset` y
                el listado de `VariableMonetaria`.
        """
        logger.info("Consultando variables monetarias")
        result = self._fetch(
            self._t.request,
            endpoint="get_monetarias",
            version=version,
            model=ResultGetMonetariasV1,
            results_key=None,
        )
        logger.debug(
            "Variables monetarias obtenidas: count=%d, variables=%d",
            result.resultset.count,
            len(result.variables),
        )
        return result

    async def aget_monetarias(
        self, *, version: str | None = None
    ) -> ResultGetMonetariasV1:
        """Versión asíncrona de `get_monetarias`."""
        logger.info("Consultando variables monetarias")
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_monetarias",
            version=version,
            model=ResultGetMonetariasV1,
            results_key=None,
        )
        logger.debug(
            "Variables monetarias obtenidas: count=%d, variables=%d",
            result.resultset.count,
            len(result.variables),
        )
        return result
