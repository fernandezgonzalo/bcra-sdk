from __future__ import annotations

from typing import Self

from ._transport import Transport
from .deudores import Deudores

_DEFAULT_BASE_URL = "https://api.bcra.gob.ar"


class BCRAClient:
    """Cliente unico, sync y async, conviven en la misma instancia.
    Cada endpoint resulve su propia version mas reciente de forma independiente
    de los demas endpoints del mismo resource.

    client = BCRAClient()
    client.deudores.get_deudas(cuit="123")
    client.deudores.get_deudas(cuit="123", version="1.0)
    await client.deudores.aget_deudas(cuit)
    """

    def __init__(self, base_url: str = _DEFAULT_BASE_URL, **httpx_kwargs):
        self._transport = Transport(base_url, **httpx_kwargs)
        self.deudores = Deudores(self._transport)

    def close(self) -> None:
        self._transport.close()

    async def aclose(self) -> None:
        await self._transport.aclose()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()
