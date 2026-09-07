import builtins
import sys

import pytest

from bcra_sdk import _cli_main
from bcra_sdk.cli import app


@pytest.fixture
def drop_cli_from_modules(monkeypatch):
    for module in list(sys.modules):
        if module == "bcra_sdk.cli" or module.startswith("bcra_sdk.cli."):
            monkeypatch.delitem(sys.modules, module, raising=False)
    yield


@pytest.fixture
def patch_import(monkeypatch):
    real_import = builtins.__import__

    def apply(stop: str, name: str):
        def fake_import(module: str, *args, **kwargs):
            if module == stop or module.startswith(stop + "."):
                raise ModuleNotFoundError(f"No module named '{name}'", name=name)
            return real_import(module, *args, **kwargs)

        return monkeypatch.setattr(builtins, "__import__", fake_import)

    return apply


def test_load_app_returns_cli_app():
    assert _cli_main._load_app_or_exit() is app


def test_main_invokes_app(monkeypatch):
    called: list[bool] = []

    def fake_app():
        called.append(True)

    monkeypatch.setattr(_cli_main, "_load_app_or_exit", lambda: fake_app)
    _cli_main.main()
    assert called == [True]


def test_missing_typer_hint(patch_import, drop_cli_from_modules):
    patch_import("typer", "typer")
    with pytest.raises(SystemExit) as exc:
        _cli_main.main()
    assert exc.value.code == _cli_main._HINT
    assert "[cli]" in exc.value.code


def test_other_missing_module_propagates(patch_import, drop_cli_from_modules):
    patch_import("rich", "rich")
    with pytest.raises(ModuleNotFoundError, match="rich"):
        _cli_main._load_app_or_exit()
