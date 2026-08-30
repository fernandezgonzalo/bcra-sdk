from __future__ import annotations

import logging
from typing import Any, Self

from ._retry import RetryPolicy
from ._transport import Transport
from .cheques import Cheques
from .deudores import Deudores
from .estadisticascambiarias import EstadisticasCambiarias
from .monetarias import Monetarias
from .regimendetransparencia import RegimenDeTransparencia

logger = logging.getLogger("bcra_sdk.client")

_DEFAULT_BASE_URL = "https://api.bcra.gob.ar"


class BCRAClient:
    """Cliente único que agrupa todos los endpoints públicos del BCRA.

    La misma instancia sirve para uso síncrono (``with``) y asíncrono
    (``async with``); cada endpoint ofrece además su par ``aget_*``.
    Los recursos se exponen como atributos organizados por dominio:
    ``deudores``, ``cheques``, ``estadisticas_cambiarias``, ``monetarias``
    y ``regimen_de_transparencia``.

    Example:
        with BCRAClient() as bcra:
            bcra.deudores.get_deudas(cuit="20111111112")
            bcra.estadisticas_cambiarias.get_cotizaciones(fecha="2024-06-12")

        async with BCRAClient() as bcra:
            await bcra.estadisticas_cambiarias.aget_cotizaciones(
                fecha="2024-06-12"
            )

        # Consultar versiones disponibles de un endpoint
        bcra.estadisticas_cambiarias.versions("get_cotizaciones")
    """

    def __init__(
        self,
        base_url: str = _DEFAULT_BASE_URL,
        retries: RetryPolicy | None = None,
        **httpx_kwargs: Any,
    ):
        """Crea el cliente y sus resources.

        No abre conexiones hasta la primera petición: el transporte se lanza
        de forma diferida y se cierra con ``close``/``aclose``.

        Args:
            base_url: URL base de la API. El default es la pública del BCRA.
            retries: Política de reintentos. El default es ``RetryPolicy()``;
                pasá ``RetryPolicy(max_retries=0)`` para desactivarlos.
            **httpx_kwargs: Argumentos extra que se pasan a ``httpx.Client``
                y ``httpx.AsyncClient`` (``timeout``, ``proxies``, ``verify``,
                etc.).
        """
        self._transport = Transport(base_url, retries=retries, **httpx_kwargs)
        self.deudores = Deudores(self._transport)
        self.cheques = Cheques(self._transport)
        self.estadisticas_cambiarias = EstadisticasCambiarias(self._transport)
        self.monetarias = Monetarias(self._transport)
        self.regimen_de_transparencia = RegimenDeTransparencia(self._transport)
        logger.debug("BCRAClient inicializado con base_url=%s", base_url)

    def close(self) -> None:
        """Cierra el cliente HTTP síncrono y libera sus conexiones."""
        self._transport.close()
        logger.debug("BCRAClient cerrado")

    async def aclose(self) -> None:
        """Cierra el cliente HTTP asíncrono y libera sus conexiones."""
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
