import asyncio

import httpx
import pytest

from bcra_sdk._retry import RetryPolicy, _retry_after_seconds
from bcra_sdk._transport import Transport
from bcra_sdk.exceptions import (
    BCRAConnectionError,
    BCRAHTTPError,
    BCRATimeoutError,
)


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
    client = transport.client
    transport.close()
    assert client.is_closed


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


def _transport(retries=None, **kwargs):
    return Transport("https://api.bcra.gob.ar", retries=retries, **kwargs)


def test_default_retry_policy():
    transport = _transport()
    assert transport._retries == RetryPolicy()


def test_retry_policy_delay():
    policy = RetryPolicy(backoff=0.5)
    assert policy.delay(0) == 0.5
    assert policy.delay(1) == 1.0
    assert policy.delay(2) == 2.0
    assert RetryPolicy().statuses == (429, 500, 502, 503, 504)


def test_retry_after_seconds_with_seconds():
    resp = httpx.Response(429, headers={"Retry-After": "5"})
    assert _retry_after_seconds(resp) == 5.0


def test_retry_after_seconds_with_http_date():
    resp = httpx.Response(429, headers={"Retry-After": "Wed, 21 Oct 2099 07:28:00 GMT"})
    delay = _retry_after_seconds(resp)
    assert isinstance(delay, float)
    assert delay >= 0


def test_retry_after_seconds_invalid():
    resp = httpx.Response(429, headers={"Retry-After": "abc"})
    assert _retry_after_seconds(resp) is None


def test_retry_after_seconds_missing_header():
    resp = httpx.Response(429)
    assert _retry_after_seconds(resp) is None


def test_retry_after_seconds_no_response():
    assert _retry_after_seconds(None) is None


def test_http_error_exposes_response_and_reason():
    def handler(request):
        return httpx.Response(503, json={"error": "x"}, request=request)

    transport = _transport(transport=httpx.MockTransport(handler))
    with pytest.raises(BCRAHTTPError) as exc_info:
        transport.request("GET", "/foo")
    err = exc_info.value
    assert err.status_code == 503
    assert err.response is not None
    assert err.response.status_code == 503
    assert err.reason == "Service Unavailable"


def test_http_error_without_response():
    err = BCRAHTTPError(400, "bad")
    assert err.response is None
    assert err.reason is None


def test_connect_error_wrapped_sync():
    def handler(request):
        raise httpx.ConnectError("connection refused", request=request)

    transport = _transport(
        retries=RetryPolicy(retry_on_timeout=False),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(BCRAConnectionError):
        transport.request("GET", "/foo")


def test_timeout_wrapped_sync():
    def handler(request):
        raise httpx.ReadTimeout("timed out", request=request)

    transport = _transport(
        retries=RetryPolicy(retry_on_timeout=False),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(BCRATimeoutError):
        transport.request("GET", "/foo")


def test_connect_error_wrapped_async():
    def handler(request):
        raise httpx.ConnectError("connection refused", request=request)

    async def run():
        transport = _transport(
            retries=RetryPolicy(retry_on_timeout=False),
            transport=httpx.MockTransport(handler),
        )
        await transport.arequest("GET", "/foo")

    with pytest.raises(BCRAConnectionError):
        asyncio.run(run())


def test_timeout_wrapped_async():
    def handler(request):
        raise httpx.ReadTimeout("timed out", request=request)

    async def run():
        transport = _transport(
            retries=RetryPolicy(retry_on_timeout=False),
            transport=httpx.MockTransport(handler),
        )
        await transport.arequest("GET", "/foo")

    with pytest.raises(BCRATimeoutError):
        asyncio.run(run())


def test_retry_sync_on_5xx_then_success():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(503, request=request)
        return httpx.Response(200, json={"ok": True})

    transport = _transport(
        retries=RetryPolicy(max_retries=2, backoff=0.01),
        transport=httpx.MockTransport(handler),
    )
    resp = transport.request("GET", "/foo")
    assert resp.status_code == 200
    assert calls == 2


def test_retry_async_on_5xx_then_success():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(502, request=request)
        return httpx.Response(200, json={"ok": True})

    async def run():
        transport = _transport(
            retries=RetryPolicy(max_retries=2, backoff=0.01),
            transport=httpx.MockTransport(handler),
        )
        return await transport.arequest("GET", "/foo")

    resp = asyncio.run(run())
    assert resp.status_code == 200
    assert calls == 2


def test_retry_sync_exhausted_raises_last_error():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        return httpx.Response(500, request=request)

    transport = _transport(
        retries=RetryPolicy(max_retries=1, backoff=0.01),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(BCRAHTTPError) as exc_info:
        transport.request("GET", "/foo")
    assert exc_info.value.status_code == 500
    assert calls == 2


def test_retry_async_exhausted_raises_last_error():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        return httpx.Response(500, request=request)

    async def run():
        transport = _transport(
            retries=RetryPolicy(max_retries=1, backoff=0.01),
            transport=httpx.MockTransport(handler),
        )
        await transport.arequest("GET", "/foo")

    with pytest.raises(BCRAHTTPError):
        asyncio.run(run())
    assert calls == 2


def test_no_retry_on_not_retryable_status():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        return httpx.Response(400, request=request)

    transport = _transport(transport=httpx.MockTransport(handler))
    with pytest.raises(BCRAHTTPError):
        transport.request("GET", "/foo")
    assert calls == 1


def test_no_retry_when_disabled():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request)

    transport = _transport(
        retries=RetryPolicy(max_retries=0),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(BCRAHTTPError):
        transport.request("GET", "/foo")
    assert calls == 1


def test_retry_respects_retry_after_header():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429, headers={"Retry-After": "0"}, request=request)
        return httpx.Response(200, json={"ok": True})

    transport = _transport(
        retries=RetryPolicy(max_retries=1, backoff=1000),
        transport=httpx.MockTransport(handler),
    )
    resp = transport.request("GET", "/foo")
    assert resp.status_code == 200
    assert calls == 2


def test_timeout_retried_then_success_sync():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("timed out", request=request)
        return httpx.Response(200, json={"ok": True})

    transport = _transport(
        retries=RetryPolicy(max_retries=2, backoff=0.01),
        transport=httpx.MockTransport(handler),
    )
    resp = transport.request("GET", "/foo")
    assert resp.status_code == 200
    assert calls == 2


def test_timeout_retried_then_success_async():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("timed out", request=request)
        return httpx.Response(200, json={"ok": True})

    async def run():
        transport = _transport(
            retries=RetryPolicy(max_retries=2, backoff=0.01),
            transport=httpx.MockTransport(handler),
        )
        return await transport.arequest("GET", "/foo")

    resp = asyncio.run(run())
    assert resp.status_code == 200
    assert calls == 2


def test_timeout_retried_then_raises_when_exhausted():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        raise httpx.ReadTimeout("timed out", request=request)

    transport = _transport(
        retries=RetryPolicy(max_retries=0),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(BCRATimeoutError):
        transport.request("GET", "/foo")
    assert calls == 1
