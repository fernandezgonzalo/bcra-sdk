import httpx
import pytest
from typer.testing import CliRunner

from bcra_sdk.cli import _common


@pytest.fixture
def cli(client, monkeypatch):
    monkeypatch.setattr(_common, "BCRAClient", lambda: client)
    return CliRunner()


@pytest.fixture
def http_ok():
    def _http_ok(data):
        return httpx.Response(200, json=data)

    return _http_ok
