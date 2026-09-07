from __future__ import annotations

from typing import Annotated

import typer

from bcra_sdk.cli._common import execute

app = typer.Typer(help="Régimen de transparencia del BCRA.")

_ENTIDAD = "codigoEntidad"
_DESCRIPCION = "descripcionEntidad"
_NOMBRE_CORTO = "nombreCorto"
_NOMBRE = "nombreCompleto"
_FECHA = "fechaInformacion"


def _base_rows(items, columns) -> list[dict]:
    return [{column: getattr(item, column) for column in columns} for item in items]


def _cajas_ahorros_rows(result) -> list[dict]:
    return _base_rows(
        result.cajas_ahorros,
        [_ENTIDAD, _DESCRIPCION, _FECHA, "procesoSimplificadoDebidaDiligencia"],
    )


def _paquetes_productos_rows(result) -> list[dict]:
    return _base_rows(
        result.paquetes_productos,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _NOMBRE, "segmento", _FECHA],
    )


def _plazos_fijos_rows(result) -> list[dict]:
    return _base_rows(
        result.plazos_fijos,
        [
            _ENTIDAD,
            _DESCRIPCION,
            _NOMBRE_CORTO,
            "denominacion",
            "montoMinimoInvertir",
            "plazoMinimoInvertirDias",
            "tasaEfectivaAnualMinima",
        ],
    )


def _prestamos_prendarios_rows(result) -> list[dict]:
    return _base_rows(
        result.prestamos_prendarios,
        [
            _ENTIDAD,
            _DESCRIPCION,
            _NOMBRE_CORTO,
            "denominacion",
            "montoMinimoOtorgable",
            "montoMaximoOtorgable",
            "plazoMaximoOtorgable",
            "tasaEfectivaAnualMaxima",
        ],
    )


def _prestamos_hipotecarios_rows(result) -> list[dict]:
    return _base_rows(
        result.prestamos_hipotecarios,
        [
            _ENTIDAD,
            _DESCRIPCION,
            _NOMBRE_CORTO,
            "denominacion",
            "montoMaximoOtorgable",
            "plazoMaximoOtorgable",
            "tasaEfectivaAnualMaxima",
        ],
    )


def _prestamos_personales_rows(result) -> list[dict]:
    return _base_rows(
        result.prestamos_personales,
        [
            _ENTIDAD,
            _DESCRIPCION,
            _NOMBRE_CORTO,
            "denominacion",
            "montoMinimoOtorgable",
            "montoMaximoOtorgable",
            "tasaEfectivaAnualMaxima",
        ],
    )


def _tarjetas_credito_rows(result) -> list[dict]:
    return _base_rows(
        result.tarjetas_credito,
        [
            _ENTIDAD,
            _DESCRIPCION,
            _NOMBRE_CORTO,
            "segmento",
            "tasaEfectivaAnualMaximaFinanciacion",
            _FECHA,
        ],
    )


@app.command("cajas-ahorros")
def cajas_ahorros(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista los productos de cajas de ahorro de las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_cajas_ahorros(
            codigoEntidad=entidad
        ),
        _cajas_ahorros_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _FECHA],
    )


@app.command("paquetes-productos")
def paquetes_productos(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista los paquetes de productos de las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_paquetes_productos(
            codigoEntidad=entidad
        ),
        _paquetes_productos_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _NOMBRE, _FECHA],
    )


@app.command("plazos-fijos")
def plazos_fijos(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista los plazos fijos ofrecidos por las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_plazos_fijos(
            codigoEntidad=entidad
        ),
        _plazos_fijos_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _FECHA],
    )


@app.command("prestamos-prendarios")
def prestamos_prendarios(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista los préstamos prendarios ofrecidos por las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_prestamos_prendarios(
            codigoEntidad=entidad
        ),
        _prestamos_prendarios_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _FECHA],
    )


@app.command("prestamos-hipotecarios")
def prestamos_hipotecarios(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista los préstamos hipotecarios ofrecidos por las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_prestamos_hipotecarios(
            codigoEntidad=entidad
        ),
        _prestamos_hipotecarios_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _FECHA],
    )


@app.command("prestamos-personales")
def prestamos_personales(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista los préstamos personales ofrecidos por las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_prestamos_personales(
            codigoEntidad=entidad
        ),
        _prestamos_personales_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _FECHA],
    )


@app.command("tarjetas-credito")
def tarjetas_credito(
    ctx: typer.Context,
    entidad: Annotated[
        int | None,
        typer.Option("--entidad", "-e", help="Código de la entidad (opcional)."),
    ] = None,
) -> None:
    """Lista las tarjetas de crédito ofrecidas por las entidades."""
    execute(
        ctx,
        lambda client: client.regimen_de_transparencia.get_tarjetas_credito(
            codigoEntidad=entidad
        ),
        _tarjetas_credito_rows,
        [_ENTIDAD, _DESCRIPCION, _NOMBRE_CORTO, _FECHA],
    )
