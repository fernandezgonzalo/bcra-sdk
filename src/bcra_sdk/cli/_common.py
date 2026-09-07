from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from typing import Any, NoReturn

import typer

from bcra_sdk import BCRAClient
from bcra_sdk.exceptions import BCRAError

from ._output import emit_table, to_json


class OutputFormat(str, Enum):
    JSON = "json"
    TABLE = "table"


def emit_error(exc: BaseException) -> NoReturn:
    """Imprime un error en stderr y aborta con código de salida 1."""
    typer.echo(f"Error: {exc}", err=True)
    raise typer.Exit(code=1)


def emit_ctx(
    ctx: typer.Context, result: Any, rows: list[dict[str, Any]], columns: list[str]
) -> None:
    """Vuelca el resultado según el formato elegido en la línea de comandos."""
    if ctx.obj["format"] is OutputFormat.TABLE:
        emit_table(rows, columns)
    else:
        typer.echo(to_json(result))


def execute(
    ctx: typer.Context,
    fn: Callable[[BCRAClient], Any],
    row_fn: Callable[[Any], list[dict[str, Any]]],
    columns: list[str],
) -> None:
    """Corre un comando: arma el cliente, llama a la API y emite el resultado."""
    with BCRAClient() as client:
        try:
            result = fn(client)
        except (BCRAError, ValueError) as exc:
            emit_error(exc)
        rows = row_fn(result)
    emit_ctx(ctx, result, rows, columns)
