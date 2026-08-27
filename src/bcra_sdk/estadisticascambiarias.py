import logging

from ._base import Resource
from .models.cotizaciones import ResultGetCotizacionesV1
from .models.divisas import ResultGetDivisasV1
from .models.evolucion import ResultGetEvolucionMonedaV1

logger = logging.getLogger("bcra_sdk.estadisticas_cambiarias")


class EstadisticasCambiarias(Resource):
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
        spec = self._resolve_version("get_divisas", version)
        logger.info("Consultando divisas")
        r = self._t.request("GET", spec.path)
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Divisas obtenidas: total=%d",
            len(result.divisas),
        )
        return result

    def get_cotizaciones(
        self, fecha: str | None = None, *, version: str | None = None
    ) -> ResultGetCotizacionesV1:
        spec = self._resolve_version("get_cotizaciones", version)
        logger.info("Consultando cotizaciones (fecha=%s)", fecha)
        params = {"fecha": fecha} if fecha else None
        r = self._t.request("GET", spec.path, params=params)
        result = spec.model.from_dict(r.json()["results"])
        logger.debug(
            "Cotizaciones obtenidas: fecha=%s, detalle=%d",
            result.fecha,
            len(result.detalle),
        )
        return result

    def get_evolucion_moneda(
        self,
        moneda: str,
        fechadesde: str | None = None,
        fechahasta: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetEvolucionMonedaV1:
        spec = self._resolve_version("get_evolucion_moneda", version)
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
            params["fechadesde"] = fechadesde
        if fechahasta:
            params["fechahasta"] = fechahasta
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        r = self._t.request(
            "GET",
            spec.path.format(moneda=moneda),
            params=params or None,
        )
        result = spec.model.from_dict(r.json())
        logger.debug(
            "Evolución obtenida: count=%d, cotizaciones=%d",
            result.resultset.count,
            len(result.cotizaciones),
        )
        return result
