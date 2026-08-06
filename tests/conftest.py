import pytest

from bcra_sdk import BCRAClient


@pytest.fixture
def client():
    with BCRAClient() as client:
        yield client
