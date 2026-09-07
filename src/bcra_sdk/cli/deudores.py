from __future__ import annotations

from typing import Annotated

import typer

from bcra_sdk.cli._common import execute

app = typer.Typer(help="Central de deudores del BCRA.")

_DEUDAS_COLUMNS = [
    "periodo",
    "entidad",
    "situacion",
    "fechaSit1",
    "monto",
    "diasAtrasoPago",
]

_DEUDAS_HISTORICAS_COLUMNS = ["periodo", "entidad", "situacion", "monto"]

_CHEQUES_RECHAZADOS_COLUMNS = [
    "causal",
    "entidad",
    "nroCheque",
    "fechaRechazo",
    "monto",
    "fechaPago",
    "estadoMulta",
    "ctaPersonal",
]


def _deudas_rows(result) -> list[dict]:
    rows = []
    for periodo in result.periodos:
        for entidad in periodo.entidades:
            rows.append(
                {
                    "periodo": periodo.periodo,
                    "entidad": entidad.entidad,
                    "situacion": entidad.situacion,
                    "fechaSit1": entidad.fechaSit1,
                    "monto": entidad.monto,
                    "diasAtrasoPago": entidad.diasAtrasoPago,
                }
            )
    return rows


def _deudas_historicas_rows(result) -> list[dict]:
    rows = []
    for periodo in result.periodos:
        for entidad in periodo.entidades:
            rows.append(
                {
                    "periodo": periodo.periodo,
                    "entidad": entidad.entidad,
                    "situacion": entidad.situacion,
                    "monto": entidad.monto,
                }
            )
    return rows


def _cheques_rechazados_rows(result) -> list[dict]:
    rows = []
    for causal in result.causales:
        for entidad in causal.entidades:
            for cheque in entidad.detalle:
                rows.append(
                    {
                        "causal": causal.causal,
                        "entidad": entidad.entidad,
                        "nroCheque": cheque.nroCheque,
                        "fechaRechazo": cheque.fechaRechazo,
                        "monto": cheque.monto,
                        "fechaPago": cheque.fechaPago,
                        "estadoMulta": cheque.estadoMulta,
                        "ctaPersonal": cheque.ctaPersonal,
                    }
                )
    return rows


@app.command("deudas")
def deudas(
    ctx: typer.Context,
    cuit: Annotated[
        str, typer.Argument(help="CUIT de 11 dígitos (con o sin guiones).")
    ],
) -> None:
    """Devuelve la situación de deudas vigente de una persona o empresa."""
    execute(
        ctx,
        lambda client: client.deudores.get_deudas(cuit=cuit),
        _deudas_rows,
        _DEUDAS_COLUMNS,
    )


@app.command("deudas-historicas")
def deudas_historicas(
    ctx: typer.Context,
    identification: Annotated[
        str, typer.Argument(help="Identificador (CUIT o CUIL) a consultar.")
    ],
) -> None:
    """Devuelve el histórico de deudas de un identificador."""
    execute(
        ctx,
        lambda client: client.deudores.get_deudas_historicas(
            identification=identification
        ),
        _deudas_historicas_rows,
        _DEUDAS_HISTORICAS_COLUMNS,
    )


@app.command("cheques-rechazados")
def cheques_rechazados(
    ctx: typer.Context,
    identification: Annotated[
        str, typer.Argument(help="Identificador (CUIT o CUIL) a consultar.")
    ],
) -> None:
    """Devuelve los cheques rechazados de un identificador."""
    execute(
        ctx,
        lambda client: client.deudores.get_cheques_rechazados(
            identification=identification
        ),
        _cheques_rechazados_rows,
        _CHEQUES_RECHAZADOS_COLUMNS,
    )
