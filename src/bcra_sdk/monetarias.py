import logging
from datetime import date

from ._base import Resource
from ._dates import _coerce_date
from .models.monetarias import (
    ResultGetEvolucionVariableV1,
    ResultGetMonetariasV1,
)

logger = logging.getLogger("bcra_sdk.monetarias")


class Monetarias(Resource):
    """Endpoints de estadísticas monetarias del BCRA.

    Expuesto como ``client.monetarias``. Incluye el maestro de variables
    monetarias (``get_monetarias``) y la evolución de una variable
    (``get_evolucion_variable``).
    """

    def __init__(self, transport):
        super().__init__(transport)
        self._register_version(
            "get_monetarias",
            "4.0",
            path="/estadisticas/v4.0/monetarias",
            model=ResultGetMonetariasV1,
        )
        self._register_version(
            "get_evolucion_variable",
            "4.0",
            path="/estadisticas/v4.0/monetarias/{idVariable}",
            model=ResultGetEvolucionVariableV1,
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

    def get_evolucion_variable(
        self,
        idVariable: int,
        desde: str | date | None = None,
        hasta: str | date | None = None,
        offset: int | None = None,
        limit: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetEvolucionVariableV1:
        """Devuelve la evolución de una variable monetaria.

        Args:
            idVariable: ID de la variable (se obtiene con `get_monetarias`).
            desde: Fecha de inicio del rango, como ``str`` ISO o
                ``datetime.date``.
            hasta: Fecha de fin del rango, como ``str`` ISO o
                ``datetime.date``.
            offset: Cantidad de registros a descartar para el paginado.
            limit: Cantidad máxima de registros (la API admite hasta 3000).
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetEvolucionVariableV1: metadatos del paginado via
                `Resultset` y la serie de `SerieMonetaria`.
        """
        logger.info(
            "Consultando evolución de variable %s (desde=%s, hasta=%s, "
            "offset=%s, limit=%s)",
            idVariable,
            desde,
            hasta,
            offset,
            limit,
        )
        params: dict[str, object] = {}
        if desde:
            params["desde"] = _coerce_date(desde)
        if hasta:
            params["hasta"] = _coerce_date(hasta)
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        result = self._fetch(
            self._t.request,
            endpoint="get_evolucion_variable",
            version=version,
            params=params,
            path_vars={"idVariable": idVariable},
            model=ResultGetEvolucionVariableV1,
            results_key=None,
        )
        logger.debug(
            "Evolución obtenida: count=%d, series=%d, puntos=%d",
            result.resultset.count,
            len(result.series),
            sum(len(s.detalle) for s in result.series),
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

    async def aget_evolucion_variable(
        self,
        idVariable: int,
        desde: str | date | None = None,
        hasta: str | date | None = None,
        offset: int | None = None,
        limit: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetEvolucionVariableV1:
        """Versión asíncrona de `get_evolucion_variable`."""
        logger.info(
            "Consultando evolución de variable %s (desde=%s, hasta=%s, "
            "offset=%s, limit=%s)",
            idVariable,
            desde,
            hasta,
            offset,
            limit,
        )
        params: dict[str, object] = {}
        if desde:
            params["desde"] = _coerce_date(desde)
        if hasta:
            params["hasta"] = _coerce_date(hasta)
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_evolucion_variable",
            version=version,
            params=params,
            path_vars={"idVariable": idVariable},
            model=ResultGetEvolucionVariableV1,
            results_key=None,
        )
        logger.debug(
            "Evolución obtenida: count=%d, series=%d, puntos=%d",
            result.resultset.count,
            len(result.series),
            sum(len(s.detalle) for s in result.series),
        )
        return result
