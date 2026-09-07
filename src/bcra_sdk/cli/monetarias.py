from __future__ import annotations

from typing import Annotated

import typer

from bcra_sdk.cli._common import execute

app = typer.Typer(help="Estadísticas monetarias del BCRA.")

_MONETARIAS_COLUMNS = [
    "idVariable",
    "descripcion",
    "categoria",
    "periodicidad",
    "unidadExpresion",
    "ultValorInformado",
]

_EVOLUCION_VARIABLE_COLUMNS = ["idVariable", "fecha", "valor"]

_METODOLOGIAS_COLUMNS = ["id", "detalle"]


def _monetarias_rows(result) -> list[dict]:
    return [
        {
            "idVariable": v.idVariable,
            "descripcion": v.descripcion,
            "categoria": v.categoria,
            "periodicidad": v.periodicidad,
            "unidadExpresion": v.unidadExpresion,
            "ultValorInformado": v.ultValorInformado,
        }
        for v in result.variables
    ]


def _evolucion_variable_rows(result) -> list[dict]:
    rows = []
    for serie in result.series:
        for punto in serie.detalle:
            rows.append(
                {
                    "idVariable": serie.idVariable,
                    "fecha": punto.fecha,
                    "valor": punto.valor,
                }
            )
    return rows


def _metodologias_rows(result) -> list[dict]:
    return [{"id": m.id, "detalle": m.detalle} for m in result.metodologias]


def _metodologia_rows(result) -> list[dict]:
    return [{"id": result.metodologia.id, "detalle": result.metodologia.detalle}]


@app.command("monetarias")
def monetarias(ctx: typer.Context) -> None:
    """Lista las variables monetarias del BCRA."""
    execute(
        ctx,
        lambda client: client.monetarias.get_monetarias(),
        _monetarias_rows,
        _MONETARIAS_COLUMNS,
    )


@app.command("evolucion-variable")
def evolucion_variable(
    ctx: typer.Context,
    id_variable: Annotated[int, typer.Argument(help="ID de la variable.")],
    desde: Annotated[
        str | None,
        typer.Option("--desde", help="Fecha de inicio del rango (ISO)."),
    ] = None,
    hasta: Annotated[
        str | None,
        typer.Option("--hasta", help="Fecha de fin del rango (ISO)."),
    ] = None,
    offset: Annotated[
        int | None, typer.Option("--offset", help="Registros a descartar.")
    ] = None,
    limit: Annotated[
        int | None, typer.Option("--limit", help="Cantidad máxima de registros.")
    ] = None,
) -> None:
    """Devuelve la evolución de una variable monetaria."""
    execute(
        ctx,
        lambda client: client.monetarias.get_evolucion_variable(
            idVariable=id_variable,
            desde=desde,
            hasta=hasta,
            offset=offset,
            limit=limit,
        ),
        _evolucion_variable_rows,
        _EVOLUCION_VARIABLE_COLUMNS,
    )


@app.command("metodologias")
def metodologias(
    ctx: typer.Context,
    offset: Annotated[
        int | None, typer.Option("--offset", help="Registros a descartar.")
    ] = None,
    limit: Annotated[
        int | None, typer.Option("--limit", help="Cantidad máxima de registros.")
    ] = None,
) -> None:
    """Lista las metodologías de las variables monetarias."""
    execute(
        ctx,
        lambda client: client.monetarias.get_metodologias(offset=offset, limit=limit),
        _metodologias_rows,
        _METODOLOGIAS_COLUMNS,
    )


@app.command("metodologia")
def metodologia(
    ctx: typer.Context,
    id_variable: Annotated[int, typer.Argument(help="ID de la variable.")],
) -> None:
    """Devuelve la metodología de una variable monetaria."""
    execute(
        ctx,
        lambda client: client.monetarias.get_metodologia(idVariable=id_variable),
        _metodologia_rows,
        _METODOLOGIAS_COLUMNS,
    )
