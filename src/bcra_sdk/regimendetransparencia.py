import logging

from ._base import Resource
from .models.transparencia import (
    ResultGetCajasAhorrosV1,
    ResultGetPaquetesProductosV1,
    ResultGetPlazosFijosV1,
    ResultGetPrestamosHipotecariosV1,
    ResultGetPrestamosPrendariosV1,
)

logger = logging.getLogger("bcra_sdk.regimendetransparencia")


class RegimenDeTransparencia(Resource):
    """Endpoints del Régimen de Transparencia del BCRA.

    Expuesto como ``client.regimen_de_transparencia``. API pública (sin
    autenticación) que informa los productos de cada entidad financiera.
    Todos los endpoints aceptan el filtro opcional ``codigoEntidad``.
    """

    def __init__(self, transport):
        super().__init__(transport)
        self._register_version(
            "get_cajas_ahorros",
            "1.0",
            path="/transparencia/v1.0/CajasAhorros",
            model=ResultGetCajasAhorrosV1,
        )
        self._register_version(
            "get_paquetes_productos",
            "1.0",
            path="/transparencia/v1.0/PaquetesProductos",
            model=ResultGetPaquetesProductosV1,
        )
        self._register_version(
            "get_plazos_fijos",
            "1.0",
            path="/transparencia/v1.0/PlazosFijos",
            model=ResultGetPlazosFijosV1,
        )
        self._register_version(
            "get_prestamos_prendarios",
            "1.0",
            path="/transparencia/v1.0/Prestamos/Prendarios",
            model=ResultGetPrestamosPrendariosV1,
        )
        self._register_version(
            "get_prestamos_hipotecarios",
            "1.0",
            path="/transparencia/v1.0/Prestamos/Hipotecarios",
            model=ResultGetPrestamosHipotecariosV1,
        )

    def get_cajas_ahorros(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetCajasAhorrosV1:
        """Devuelve los productos de cajas de ahorro de las entidades.

        Args:
            codigoEntidad: Código de la entidad para filtrar el listado.
                Opcional; si no se informa, devuelve todas las entidades.
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetCajasAhorrosV1: listado de `CajaAhorro`.
        """
        logger.info("Consultando cajas de ahorro (codigoEntidad=%s)", codigoEntidad)
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = self._fetch(
            self._t.request,
            endpoint="get_cajas_ahorros",
            version=version,
            params=params,
            model=ResultGetCajasAhorrosV1,
        )
        logger.debug(
            "Cajas de ahorro obtenidas: total=%d",
            len(result.cajas_ahorros),
        )
        return result

    async def aget_cajas_ahorros(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetCajasAhorrosV1:
        """Versión asíncrona de `get_cajas_ahorros`."""
        logger.info("Consultando cajas de ahorro (codigoEntidad=%s)", codigoEntidad)
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_cajas_ahorros",
            version=version,
            params=params,
            model=ResultGetCajasAhorrosV1,
        )
        logger.debug(
            "Cajas de ahorro obtenidas: total=%d",
            len(result.cajas_ahorros),
        )
        return result

    def get_paquetes_productos(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPaquetesProductosV1:
        """Devuelve los paquetes de productos de las entidades.

        Args:
            codigoEntidad: Código de la entidad para filtrar el listado.
                Opcional; si no se informa, devuelve todas las entidades.
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetPaquetesProductosV1: listado de `PaqueteProducto`.
        """
        logger.info(
            "Consultando paquetes de productos (codigoEntidad=%s)", codigoEntidad
        )
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = self._fetch(
            self._t.request,
            endpoint="get_paquetes_productos",
            version=version,
            params=params,
            model=ResultGetPaquetesProductosV1,
        )
        logger.debug(
            "Paquetes de productos obtenidos: total=%d",
            len(result.paquetes_productos),
        )
        return result

    async def aget_paquetes_productos(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPaquetesProductosV1:
        """Versión asíncrona de `get_paquetes_productos`."""
        logger.info(
            "Consultando paquetes de productos (codigoEntidad=%s)", codigoEntidad
        )
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_paquetes_productos",
            version=version,
            params=params,
            model=ResultGetPaquetesProductosV1,
        )
        logger.debug(
            "Paquetes de productos obtenidos: total=%d",
            len(result.paquetes_productos),
        )
        return result

    def get_plazos_fijos(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPlazosFijosV1:
        """Devuelve los plazos fijos ofrecidos por las entidades.

        Args:
            codigoEntidad: Código de la entidad para filtrar el listado.
                Opcional; si no se informa, devuelve todas las entidades.
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetPlazosFijosV1: listado de `PlazoFijo`.
        """
        logger.info("Consultando plazos fijos (codigoEntidad=%s)", codigoEntidad)
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = self._fetch(
            self._t.request,
            endpoint="get_plazos_fijos",
            version=version,
            params=params,
            model=ResultGetPlazosFijosV1,
        )
        logger.debug(
            "Plazos fijos obtenidos: total=%d",
            len(result.plazos_fijos),
        )
        return result

    async def aget_plazos_fijos(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPlazosFijosV1:
        """Versión asíncrona de `get_plazos_fijos`."""
        logger.info("Consultando plazos fijos (codigoEntidad=%s)", codigoEntidad)
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_plazos_fijos",
            version=version,
            params=params,
            model=ResultGetPlazosFijosV1,
        )
        logger.debug(
            "Plazos fijos obtenidos: total=%d",
            len(result.plazos_fijos),
        )
        return result

    def get_prestamos_prendarios(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPrestamosPrendariosV1:
        """Devuelve los préstamos prendarios ofrecidos por las entidades.

        Args:
            codigoEntidad: Código de la entidad para filtrar el listado.
                Opcional; si no se informa, devuelve todas las entidades.
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetPrestamosPrendariosV1: listado de `PrestamoPrendario`.
        """
        logger.info(
            "Consultando préstamos prendarios (codigoEntidad=%s)", codigoEntidad
        )
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = self._fetch(
            self._t.request,
            endpoint="get_prestamos_prendarios",
            version=version,
            params=params,
            model=ResultGetPrestamosPrendariosV1,
        )
        logger.debug(
            "Préstamos prendarios obtenidos: total=%d",
            len(result.prestamos_prendarios),
        )
        return result

    async def aget_prestamos_prendarios(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPrestamosPrendariosV1:
        """Versión asíncrona de `get_prestamos_prendarios`."""
        logger.info(
            "Consultando préstamos prendarios (codigoEntidad=%s)", codigoEntidad
        )
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_prestamos_prendarios",
            version=version,
            params=params,
            model=ResultGetPrestamosPrendariosV1,
        )
        logger.debug(
            "Préstamos prendarios obtenidos: total=%d",
            len(result.prestamos_prendarios),
        )
        return result

    def get_prestamos_hipotecarios(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPrestamosHipotecariosV1:
        """Devuelve los préstamos hipotecarios ofrecidos por las entidades.

        Args:
            codigoEntidad: Código de la entidad para filtrar el listado.
                Opcional; si no se informa, devuelve todas las entidades.
            version: Versión del endpoint a usar. El default es la más
                reciente; buscá las disponibles con `Resource.versions`.

        Returns:
            ResultGetPrestamosHipotecariosV1: listado de `PrestamoHipotecario`.
        """
        logger.info(
            "Consultando préstamos hipotecarios (codigoEntidad=%s)", codigoEntidad
        )
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = self._fetch(
            self._t.request,
            endpoint="get_prestamos_hipotecarios",
            version=version,
            params=params,
            model=ResultGetPrestamosHipotecariosV1,
        )
        logger.debug(
            "Préstamos hipotecarios obtenidos: total=%d",
            len(result.prestamos_hipotecarios),
        )
        return result

    async def aget_prestamos_hipotecarios(
        self,
        codigoEntidad: int | None = None,
        *,
        version: str | None = None,
    ) -> ResultGetPrestamosHipotecariosV1:
        """Versión asíncrona de `get_prestamos_hipotecarios`."""
        logger.info(
            "Consultando préstamos hipotecarios (codigoEntidad=%s)", codigoEntidad
        )
        params = {"codigoEntidad": codigoEntidad} if codigoEntidad is not None else None
        result = await self._fetch(
            self._t.arequest,
            endpoint="get_prestamos_hipotecarios",
            version=version,
            params=params,
            model=ResultGetPrestamosHipotecariosV1,
        )
        logger.debug(
            "Préstamos hipotecarios obtenidos: total=%d",
            len(result.prestamos_hipotecarios),
        )
        return result
