from __future__ import annotations
import httpx
from .exceptions import BCRAHTTPError


class Transport:
    """Capa HTTP compartida entre todos los resources, sync y async"""

    def __init__(self, base_url: str, timeout: float = 10.0, **httpx_kwargs):
        self._base_url = base_url
        self._timeout = timeout
        self._httpx_kwargs = httpx_kwargs
        self._client: httpx.Client | None = None
        self._aclient: httpx.AsyncClient | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url, timeout=self._timeout, **self._httpx_kwargs
            )
        return self._client

    @property
    def aclient(self) -> httpx.AsyncClient:
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(
                base_url=self._base_url, timeout=self._timeout, **self._httpx_kwargs
            )
        return self._aclient

    def request(self, method: str, path: str, **kw) -> httpx.Response:
        resp = self.client.request(method, path, **kw)
        self._raise_for_status(resp)

        return resp

    async def arequest(self, method: str, path: str, **kw) -> httpx.Response:
        resp = await self.aclient.request(method, path, **kw)
        self._raise_for_status(resp)

        return resp

    @staticmethod
    def _raise_for_status(resp: httpx.Response) -> None:
        if resp.is_error:
            raise BCRAHTTPError(resp.status_code, resp.text)

    def close(self) -> None:
        if self._client:
            self._client.close()

    async def aclose(self) -> None:
        if self._aclient:
            await self._aclient.aclose()
