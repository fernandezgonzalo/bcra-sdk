import pytest
from typer.testing import CliRunner

from bcra_sdk.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip()


def test_main_help(runner):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "deudores" in result.output
    assert "cheques" in result.output
    assert "cambiarias" in result.output
    assert "monetarias" in result.output
    assert "transparencia" in result.output


def test_no_args_help(runner):
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "deudores" in result.output


def test_subcommands_help(runner):
    for sub in ["deudores", "cheques", "cambiarias", "monetarias", "transparencia"]:
        result = runner.invoke(app, [sub, "--help"])
        assert result.exit_code == 0, sub
        assert sub in result.output
