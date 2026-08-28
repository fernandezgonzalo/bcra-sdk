import logging
from datetime import date

from ._base import Resource
from ._dates import _coerce_date
from .models.cotizaciones import ResultGetCotizacionesV1
from .models.divisas import ResultGetDivisasV1
from .models.evolucion import ResultGetEvolucionMonedaV1

logger = logging.getLogger("bcra_sdk.estadisticas_cambiarias")


class EstadisticasCambiarias(Resource):
    """Endpoints de estadísticas cambiarias del BCRA.

    Expuesto como ``client.estadisticas_cambiarias``. Incluye el maestro de
    divisas, las cotizaciones por fecha y la evolución de una moneda.
    """

    def __init__(self, transport):
        super().__init__(transport)
        self._register_version(
            "get_divisas",
            "1.0",
            path="/estadisticascambiarias/v1.0/Maestros/Divisas",
            model=ResultGetDivisasV1,
        )
        self._register_version(
            "get_cotizaciones",
            "1.0",
            path="/estadisticascambiarias/v1.0/Cotizaciones",
            model=ResultGetCotizacionesV1,
        )
        self._register_version(
            "get_evolucion_moneda",
            "1.0",
            path="/estadisticascambiarias/v1.0/Cotizaciones/{moneda}",
            model=ResultGetEvolucionMonedaV1,
        )

    def get_divisas(self, *, version: str | None = None) -> ResultGetDivisasV1:
        """Devuelve el maestro de divisas del BCRA.

        Args:
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con
                `Resource.versions`.

        Returns:
            ResultGetDivisasV1: listado de `Divisa`.
        """
        logger.info("Consultando divisas")
        result = self._fetch(
            self._t.request,
            endpoint="get_divisas",
            version=version,
            model=ResultGetDivisasV1,
        )
        logger.debug(
            "Divisas obtenidas: total=%d",
            len(result.divisas),
        )
        return result

    async def aget_divisas(self, *, version: str | None = None) -> ResultGetDivisasV1:
        """Versión asíncrona de `get_divisas`."""
        logger.info("Consultando divisas")
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_divisas",
            version=version,
            model=ResultGetDivisasV1,
        )
        logger.debug(
            "Divisas obtenidas: total=%d",
            len(result.divisas),
        )
        return result

    def get_cotizaciones(
        self,
        fecha: str | date | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetCotizacionesV1:
        """Devuelve las cotizaciones de todas las monedas para una fecha.

        Args:
            fecha: Fecha de la cotización, como ``str`` ISO (``YYYY-MM-DD``)
                o ``datetime.date``. Si se omite, la API devuelve la
                cotización más reciente.
            version: Versión del endpoint a usar. El default es la más
                reciente.

        Returns:
            ResultGetCotizacionesV1: cotizaciones de la fecha, con el
                detalle por `Cotizacion`.
        """
        logger.info("Consultando cotizaciones (fecha=%s)", fecha)
        params = {"fecha": _coerce_date(fecha)} if fecha else None
        result = self._fetch(
            self._t.request,
            endpoint="get_cotizaciones",
            version=version,
            params=params,
            model=ResultGetCotizacionesV1,
        )
        logger.debug(
            "Cotizaciones obtenidas: fecha=%s, detalle=%d",
            result.fecha,
            len(result.detalle),
        )
        return result

    async def aget_cotizaciones(
        self,
        fecha: str | date | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetCotizacionesV1:
        """Versión asíncrona de `get_cotizaciones`."""
        logger.info("Consultando cotizaciones (fecha=%s)", fecha)
        params = {"fecha": _coerce_date(fecha)} if fecha else None
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_cotizaciones",
            version=version,
            params=params,
            model=ResultGetCotizacionesV1,
        )
        logger.debug(
            "Cotizaciones obtenidas: fecha=%s, detalle=%d",
            result.fecha,
            len(result.detalle),
        )
        return result

    def get_evolucion_moneda(
        self,
        moneda: str,
        fechadesde: str | date | None = None,
        fechahasta: str | date | None = None,
        limit: int | None = None,
        offset: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetEvolucionMonedaV1:
        """Devuelve la evolución de cotizaciones de una moneda.

        Args:
            moneda: Código de la moneda (``ARS``, ``EUR``, ``USD``, etc.).
            fechadesde: Límite inferior del período, como ``str`` ISO o
                ``datetime.date``.
            fechahasta: Límite superior del período, como ``str`` ISO o
                ``datetime.date``.
            limit: Cantidad máxima de resultados (la API exige valores entre
                10 y 1000).
            offset: Cantidad de resultados a saltear.
            version: Versión del endpoint a usar. El default es la más
                reciente.

        Returns:
            ResultGetEvolucionMonedaV1: metadatos del paginado via
                `Resultset` y la serie de `ResultGetCotizacionesV1`.
        """
        logger.info(
            "Consultando evolución de %s (fechadesde=%s, fechahasta=%s, "
            "limit=%s, offset=%s)",
            moneda,
            fechadesde,
            fechahasta,
            limit,
            offset,
        )
        params: dict[str, object] = {}
        if fechadesde:
            params["fechadesde"] = _coerce_date(fechadesde)
        if fechahasta:
            params["fechahasta"] = _coerce_date(fechahasta)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        result = self._fetch(
            self._t.request,
            endpoint="get_evolucion_moneda",
            version=version,
            params=params,
            path_vars={"moneda": moneda},
            model=ResultGetEvolucionMonedaV1,
            results_key=None,
        )
        logger.debug(
            "Evolución obtenida: count=%d, cotizaciones=%d",
            result.resultset.count,
            len(result.cotizaciones),
        )
        return result

    async def aget_evolucion_moneda(
        self,
        moneda: str,
        fechadesde: str | date | None = None,
        fechahasta: str | date | None = None,
        limit: int | None = None,
        offset: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetEvolucionMonedaV1:
        """Versión asíncrona de `get_evolucion_moneda`."""
        logger.info(
            "Consultando evolución de %s (fechadesde=%s, fechahasta=%s, "
            "limit=%s, offset=%s)",
            moneda,
            fechadesde,
            fechahasta,
            limit,
            offset,
        )
        params: dict[str, object] = {}
        if fechadesde:
            params["fechadesde"] = _coerce_date(fechadesde)
        if fechahasta:
            params["fechahasta"] = _coerce_date(fechahasta)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_evolucion_moneda",
            version=version,
            params=params,
            path_vars={"moneda": moneda},
            model=ResultGetEvolucionMonedaV1,
            results_key=None,
        )
        logger.debug(
            "Evolución obtenida: count=%d, cotizaciones=%d",
            result.resultset.count,
            len(result.cotizaciones),
        )
        return result
