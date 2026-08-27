from __future__ import annotations

import asyncio
import logging
import time

import httpx

from ._retry import RetryPolicy, _retry_after_seconds
from .exceptions import BCRAConnectionError, BCRAHTTPError, BCRATimeoutError

logger = logging.getLogger("bcra_sdk.transport")


class Transport:
    """Capa HTTP compartida entre todos los resources, sync y async"""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        retries: RetryPolicy | None = None,
        **httpx_kwargs,
    ):
        self._base_url = base_url
        self._timeout = timeout
        self._retries = retries if retries is not None else RetryPolicy()
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
        logger.debug("%s %s", method, path)
        attempt = 0
        while True:
            try:
                resp = self._perform(self.client, method, path, **kw)
                self._raise_for_status(resp)
                return resp
            except BCRATimeoutError:
                if (
                    not self._retries.retry_on_timeout
                    or attempt >= self._retries.max_retries
                ):
                    raise
                delay = self._retries.delay(attempt)
                logger.warning(
                    "Timeout en intento %d de %s: reintento en %.2fs",
                    attempt + 1,
                    path,
                    delay,
                )
                time.sleep(delay)
                attempt += 1
            except BCRAHTTPError as err:
                if (
                    err.status_code not in self._retries.statuses
                    or attempt >= self._retries.max_retries
                ):
                    raise
                delay = _retry_after_seconds(err.response)
                if delay is None:
                    delay = self._retries.delay(attempt)
                logger.warning(
                    "HTTP %s en intento %d de %s: reintento en %.2fs",
                    err.status_code,
                    attempt + 1,
                    path,
                    delay,
                )
                time.sleep(delay)
                attempt += 1

    async def arequest(self, method: str, path: str, **kw) -> httpx.Response:
        logger.debug("%s %s", method, path)
        attempt = 0
        while True:
            try:
                resp = await self._aperform(self.aclient, method, path, **kw)
                self._raise_for_status(resp)
                return resp
            except BCRATimeoutError:
                if (
                    not self._retries.retry_on_timeout
                    or attempt >= self._retries.max_retries
                ):
                    raise
                delay = self._retries.delay(attempt)
                logger.warning(
                    "Timeout en intento %d de %s: reintento en %.2fs",
                    attempt + 1,
                    path,
                    delay,
                )
                await asyncio.sleep(delay)
                attempt += 1
            except BCRAHTTPError as err:
                if (
                    err.status_code not in self._retries.statuses
                    or attempt >= self._retries.max_retries
                ):
                    raise
                delay = _retry_after_seconds(err.response)
                if delay is None:
                    delay = self._retries.delay(attempt)
                logger.warning(
                    "HTTP %s en intento %d de %s: reintento en %.2fs",
                    err.status_code,
                    attempt + 1,
                    path,
                    delay,
                )
                await asyncio.sleep(delay)
                attempt += 1

    @staticmethod
    def _perform(client: httpx.Client, method: str, path: str, **kw) -> httpx.Response:
        try:
            return client.request(method, path, **kw)
        except httpx.TimeoutException as exc:
            raise BCRATimeoutError(f"Timeout en {method} {path}") from exc
        except httpx.RequestError as exc:
            raise BCRAConnectionError(f"Error de red en {method} {path}") from exc

    @staticmethod
    async def _aperform(
        client: httpx.AsyncClient, method: str, path: str, **kw
    ) -> httpx.Response:
        try:
            return await client.request(method, path, **kw)
        except httpx.TimeoutException as exc:
            raise BCRATimeoutError(f"Timeout en {method} {path}") from exc
        except httpx.RequestError as exc:
            raise BCRAConnectionError(f"Error de red en {method} {path}") from exc

    @staticmethod
    def _raise_for_status(resp: httpx.Response) -> None:
        if resp.is_error:
            logger.error("HTTP %s %s", resp.status_code, resp.text)
            raise BCRAHTTPError(resp.status_code, resp.text, response=resp)

    def close(self) -> None:
        if self._client:
            self._client.close()

    async def aclose(self) -> None:
        if self._aclient:
            await self._aclient.aclose()
