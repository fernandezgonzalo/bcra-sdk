from __future__ import annotations

from typing import Annotated

import typer

from bcra_sdk.cli._common import execute

app = typer.Typer(help="Sistema de cheques del BCRA.")

_ENTIDADES_COLUMNS = ["codigoEntidad", "denominacion"]

_CHEQUE_DENUNCIADO_COLUMNS = [
    "numeroCheque",
    "denunciado",
    "sucursal",
    "numeroCuenta",
    "causal",
]


def _entidades_rows(result) -> list[dict]:
    return [
        {"codigoEntidad": e.codigoEntidad, "denominacion": e.denominacion}
        for e in result.entidades
    ]


def _cheque_denunciado_rows(result) -> list[dict]:
    return [
        {
            "numeroCheque": result.numeroCheque,
            "denunciado": result.denunciado,
            "sucursal": detalle.sucursal,
            "numeroCuenta": detalle.numeroCuenta,
            "causal": detalle.causal,
        }
        for detalle in result.detalles
    ]


@app.command("entidades")
def entidades(ctx: typer.Context) -> None:
    """Lista las entidades bancarias vigentes."""
    execute(
        ctx,
        lambda client: client.cheques.get_entidades(),
        _entidades_rows,
        _ENTIDADES_COLUMNS,
    )


@app.command("cheque-denunciado")
def cheque_denunciado(
    ctx: typer.Context,
    codigo_entidad: Annotated[
        int, typer.Argument(help="Código de la entidad bancaria.")
    ],
    numero_cheque: Annotated[int, typer.Argument(help="Número del cheque.")],
) -> None:
    """Consulta el estado de denuncia de un cheque."""
    execute(
        ctx,
        lambda client: client.cheques.get_cheque_denunciado(
            codigo_entidad=codigo_entidad, numero_cheque=numero_cheque
        ),
        _cheque_denunciado_rows,
        _CHEQUE_DENUNCIADO_COLUMNS,
    )
