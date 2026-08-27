import asyncio

from bcra_sdk import BCRAClient


def test_sync_context_manager_closes():
    with BCRAClient() as client:
        assert isinstance(client, BCRAClient)
    assert client._transport._client is None


def test_close():
    client = BCRAClient()
    client.close()
    client.close()


def test_async_context_manager_closes():
    async def run():
        async with BCRAClient() as client:
            assert isinstance(client, BCRAClient)
        assert client._transport._aclient is None

    asyncio.run(run())


def test_aclose():
    async def run():
        client = BCRAClient()
        await client.aclose()
        await client.aclose()

    asyncio.run(run())
