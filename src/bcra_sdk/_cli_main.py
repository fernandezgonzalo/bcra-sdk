from __future__ import annotations

from collections.abc import Callable
from typing import NoReturn

_HINT = (
    "Error: el comando 'bcra' requiere el extra 'cli'. "
    "Instalalo con: pip install 'bcra-sdk[cli]'"
)


def _missing_typer_error() -> NoReturn:
    raise SystemExit(_HINT)


def _load_app_or_exit() -> Callable[[], None]:
    try:
        from bcra_sdk.cli import app
    except ModuleNotFoundError as exc:
        if exc.name == "typer":
            _missing_typer_error()
        raise
    return app


def main() -> None:
    _load_app_or_exit()()
