from __future__ import annotations

import logging
from typing import Self

from ._transport import Transport
from .cheques import Cheques
from .deudores import Deudores
from .estadisticascambiarias import EstadisticasCambiarias

logger = logging.getLogger("bcra_sdk.client")

_DEFAULT_BASE_URL = "https://api.bcra.gob.ar"


class BCRAClient:
    """Cliente unico, sync y async, conviven en la misma instancia.
    Cada endpoint resuelve su propia version mas reciente de forma independiente
    de los demas endpoints del mismo resource.

    client = BCRAClient()
    client.deudores.get_deudas(cuit="123")
    client.estadisticas_cambiarias.get_cotizaciones(fecha="2024-06-12")
    await client.estadisticas_cambiarias.aget_cotizaciones(fecha="2024-06-12")

    # Consultar versiones disponibles de un endpoint
    client.estadisticas_cambiarias.versions("get_cotizaciones")
    """

    def __init__(self, base_url: str = _DEFAULT_BASE_URL, **httpx_kwargs):
        self._transport = Transport(base_url, **httpx_kwargs)
        self.deudores = Deudores(self._transport)
        self.cheques = Cheques(self._transport)
        self.estadisticas_cambiarias = EstadisticasCambiarias(self._transport)
        logger.debug("BCRAClient inicializado con base_url=%s", base_url)

    def close(self) -> None:
        self._transport.close()
        logger.debug("BCRAClient cerrado")

    async def aclose(self) -> None:
        await self._transport.aclose()
        logger.debug("BCRAClient async cerrado")

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()
