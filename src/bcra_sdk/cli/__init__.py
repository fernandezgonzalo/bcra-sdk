from __future__ import annotations

from typing import Annotated

import typer

from bcra_sdk import __version__ as sdk_version
from bcra_sdk.cli import cambiarias, cheques, deudores, monetarias, transparencia
from bcra_sdk.cli._common import OutputFormat

app = typer.Typer(
    help="Herramienta de línea de comandos para las APIs públicas del BCRA.",
    add_completion=True,
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(sdk_version)
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Muestra la versión del SDK.",
            callback=_version_callback,
        ),
    ] = False,
    format: Annotated[
        OutputFormat,
        typer.Option(
            "--format",
            "-f",
            help="Formato de salida de los resultados.",
        ),
    ] = OutputFormat.JSON,
) -> None:
    ctx.obj = {"format": format}


app.add_typer(deudores.app, name="deudores", help="Central de deudores.")
app.add_typer(cheques.app, name="cheques", help="Sistema de cheques.")
app.add_typer(cambiarias.app, name="cambiarias", help="Estadísticas cambiarias.")
app.add_typer(monetarias.app, name="monetarias", help="Estadísticas monetarias.")
app.add_typer(
    transparencia.app,
    name="transparencia",
    help="Régimen de transparencia.",
)
