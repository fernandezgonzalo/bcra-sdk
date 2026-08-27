import asyncio

import httpx
import pytest

from bcra_sdk._transport import Transport
from bcra_sdk.exceptions import BCRAHTTPError


def _sync_handler(request):
    return httpx.Response(200, json={"ok": True})


def test_client_lazy_creation_and_cache():
    transport = Transport(
        "https://api.bcra.gob.ar", transport=httpx.MockTransport(_sync_handler)
    )
    assert transport._client is None
    first = transport.client
    second = transport.client
    assert second is first
    assert transport._client is not None


def test_request_success():
    transport = Transport(
        "https://api.bcra.gob.ar", transport=httpx.MockTransport(_sync_handler)
    )
    resp = transport.request("GET", "/foo", params={"a": 1})
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_request_raises_on_error():
    def handler(request):
        return httpx.Response(500, text="boom")

    transport = Transport(
        "https://api.bcra.gob.ar", transport=httpx.MockTransport(handler)
    )
    with pytest.raises(BCRAHTTPError) as exc_info:
        transport.request("GET", "/foo")
    assert exc_info.value.status_code == 500


def test_close_only_when_client_exists():
    transport = Transport("https://api.bcra.gob.ar")
    transport.close()


def test_close_closes_lazy_client():
    transport = Transport(
        "https://api.bcra.gob.ar", transport=httpx.MockTransport(_sync_handler)
    )
    transport.client
    transport.close()


def test_aclient_lazy_creation_and_cache():
    async def run():
        transport = Transport(
            "https://api.bcra.gob.ar", transport=httpx.MockTransport(_sync_handler)
        )
        assert transport._aclient is None
        first = transport.aclient
        second = transport.aclient
        await transport.aclose()
        return second is first

    assert asyncio.run(run())


def test_arequest_success():
    async def run():
        transport = Transport(
            "https://api.bcra.gob.ar", transport=httpx.MockTransport(_sync_handler)
        )
        resp = await transport.arequest("GET", "/foo")
        return resp.status_code

    assert asyncio.run(run()) == 200


def test_arequest_raises_on_error():
    def handler(request):
        return httpx.Response(404, text="nope")

    async def run():
        transport = Transport(
            "https://api.bcra.gob.ar", transport=httpx.MockTransport(handler)
        )
        with pytest.raises(BCRAHTTPError) as exc_info:
            await transport.arequest("GET", "/foo")
        return exc_info.value.status_code

    assert asyncio.run(run()) == 404


def test_aclose_only_when_aclient_exists():
    async def run():
        transport = Transport("https://api.bcra.gob.ar")
        await transport.aclose()

    asyncio.run(run())
