import logging

from ._base import Resource, endpoint
from .models.cotizaciones import ResultGetCotizacionesV1
from .models.divisas import ResultGetDivisasV1
from .models.evolucion import ResultGetEvolucionMonedaV1, Resultset

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

    @endpoint(version="1.0", name="get_cotizaciones")
    def get_cotizaciones_v1(self, fecha: str | None = None) -> ResultGetCotizacionesV1:
        logger.info("Consultando cotizaciones (fecha=%s)", fecha)
        params = {"fecha": fecha} if fecha else None
        r = self._t.request(
            "GET",
            "/estadisticascambiarias/v1.0/Cotizaciones",
            params=params,
        )
        result = ResultGetCotizacionesV1.from_dict(r.json()["results"])
        logger.debug(
            "Cotizaciones obtenidas: fecha=%s, detalle=%d",
            result.fecha,
            len(result.detalle),
        )
        return result

    @endpoint(version="1.0", name="get_evolucion_moneda")
    def get_evolucion_moneda_v1(
        self,
        moneda: str,
        fechadesde: str | None = None,
        fechahasta: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResultGetEvolucionMonedaV1:
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
            f"/estadisticascambiarias/v1.0/Cotizaciones/{moneda}",
            params=params or None,
        )
        resultset = Resultset(**r.json()["metadata"]["resultset"])
        cotizaciones = [
            ResultGetCotizacionesV1.from_dict(c) for c in r.json()["results"]
        ]
        logger.debug(
            "Evolución obtenida: count=%d, cotizaciones=%d",
            resultset.count,
            len(cotizaciones),
        )
        return ResultGetEvolucionMonedaV1(
            resultset=resultset, cotizaciones=cotizaciones
        )
