from __future__ import annotations

from typing import Annotated

import typer

from bcra_sdk.cli._common import execute

app = typer.Typer(help="Estadísticas cambiarias del BCRA.")

_DIVISAS_COLUMNS = ["codigo", "denominacion"]

_COTIZACIONES_COLUMNS = [
    "codigoMoneda",
    "descripcion",
    "tipoPase",
    "tipoCotizacion",
]

_EVOLUCION_COLUMNS = ["fecha", "codigoMoneda", "tipoPase", "tipoCotizacion"]


def _divisas_rows(result) -> list[dict]:
    return [
        {"codigo": d.codigo, "denominacion": d.denominacion} for d in result.divisas
    ]


def _cotizaciones_rows(result) -> list[dict]:
    return [
        {
            "codigoMoneda": c.codigoMoneda,
            "descripcion": c.descripcion,
            "tipoPase": c.tipoPase,
            "tipoCotizacion": c.tipoCotizacion,
        }
        for c in result.detalle
    ]


def _evolucion_rows(result) -> list[dict]:
    rows = []
    for cotizacion in result.cotizaciones:
        for detalle in cotizacion.detalle:
            rows.append(
                {
                    "fecha": cotizacion.fecha,
                    "codigoMoneda": detalle.codigoMoneda,
                    "tipoPase": detalle.tipoPase,
                    "tipoCotizacion": detalle.tipoCotizacion,
                }
            )
    return rows


@app.command("divisas")
def divisas(ctx: typer.Context) -> None:
    """Lista el maestro de divisas."""
    execute(
        ctx,
        lambda client: client.estadisticas_cambiarias.get_divisas(),
        _divisas_rows,
        _DIVISAS_COLUMNS,
    )


@app.command("cotizaciones")
def cotizaciones(
    ctx: typer.Context,
    fecha: Annotated[
        str | None,
        typer.Option("--fecha", help="Fecha en formato ISO (YYYY-MM-DD)."),
    ] = None,
) -> None:
    """Devuelve las cotizaciones de todas las monedas para una fecha."""
    execute(
        ctx,
        lambda client: client.estadisticas_cambiarias.get_cotizaciones(fecha=fecha),
        _cotizaciones_rows,
        _COTIZACIONES_COLUMNS,
    )


@app.command("evolucion-moneda")
def evolucion_moneda(
    ctx: typer.Context,
    moneda: Annotated[
        str, typer.Argument(help="Código de la moneda (ARS, USD, EUR...).")
    ],
    fechadesde: Annotated[
        str | None,
        typer.Option("--desde", help="Límite inferior del período (ISO)."),
    ] = None,
    fechahasta: Annotated[
        str | None,
        typer.Option("--hasta", help="Límite superior del período (ISO)."),
    ] = None,
    limit: Annotated[
        int | None,
        typer.Option("--limit", help="Cantidad máxima de resultados (10-1000)."),
    ] = None,
    offset: Annotated[
        int | None, typer.Option("--offset", help="Resultados a saltear.")
    ] = None,
) -> None:
    """Devuelve la evolución de cotizaciones de una moneda."""
    execute(
        ctx,
        lambda client: client.estadisticas_cambiarias.get_evolucion_moneda(
            moneda=moneda,
            fechadesde=fechadesde,
            fechahasta=fechahasta,
            limit=limit,
            offset=offset,
        ),
        _evolucion_rows,
        _EVOLUCION_COLUMNS,
    )
