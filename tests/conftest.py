import pytest


@pytest.fixture
def client():
    from bcra_sdk import BCRAClient

    with BCRAClient() as client:
        yield client
