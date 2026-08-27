# Deudores (`bcra.deudores`)

Endpoints de la Central de Deudores del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_deudas(cuit)` | `GET /centraldedeudores/v1.0/Deudas/{cuit}` |
| `get_deudas_historicas(identification)` | `GET /CentralDeDeudores/v1.0/Deudas/Historicas/{identification}` |
| `get_cheques_rechazados(identification)` | `GET /centraldedeudores/v1.0/Deudas/ChequesRechazados/{identification}` |

## `get_deudas(cuit)`

Devuelve la situación actual de deudas para un CUIT.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `cuit` | `str` | CUIT / CUIL / CDI a consultar (obligatorio) |

Devuelve `ResultGetDeudasV1`:

- `identificacion: int`
- `denominacion: str`
- `periodos: list[Periodo]`
    - `Periodo.periodo: str`
    - `Periodo.entidades: list[Entidad]`

`Entidad` expone: `entidad`, `situacion`, `fechaSit1`, `monto`, `diasAtrasoPago`,
`refinanciaciones`, `recategorizacionOblig`, `situacionJuridica`,
`irrecDisposicionTecnica`, `enRevision`, `procesoJud`.

```python
with BCRAClient() as bcra:
    reporte = bcra.deudores.get_deudas(cuit="20111111112")
    for periodo in reporte.periodos:
        for entidad in periodo.entidades:
            print(entidad.entidad, entidad.situacion)
```

## `get_deudas_historicas(identification)`

Devuelve el historial de deudas para una identificación.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `identification` | `str` | Identificación (CUIT / CUIL / CDI) a consultar (obligatorio) |

Devuelve `ResultGetDeudasHistoricasV1`:

- `identificacion: str`
- `denominacion: str`
- `periodos: list[PeriodoHistorica]`
    - `PeriodoHistorica.periodo: str`
    - `PeriodoHistorica.entidades: list[EntidadHistorica]`

`EntidadHistorica` expone: `entidad`, `situacion`, `monto`, `enRevision`, `procesoJud`.

```python
with BCRAClient() as bcra:
    historico = bcra.deudores.get_deudas_historicas(identification="20111111112")
    print(historico.denominacion)
```

## `get_cheques_rechazados(identification)`

Devuelve los cheques rechazados para una identificación.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `identification` | `str` | Identificación a consultar (obligatorio) |

Devuelve `ResultGetChequesRechazadosV1`:

- `identificacion: int`
- `causales: list[Causal]`
    - `Causal.causal: str`
    - `Causal.entidades: list[EntidadCheque]`
        - `EntidadCheque.entidad: int`
        - `EntidadCheque.detalle: list[DetalleCheque]`

`DetalleCheque` expone: `nroCheque`, `fechaRechazo`, `monto`, `fechaPago`,
`fechaPagoMulta`, `estadoMulta`, `ctaPersonal`, `denomJuridica`, `enRevision`, `procesoJud`.

```python
with BCRAClient() as bcra:
    rechazados = bcra.deudores.get_cheques_rechazados(identification="20111111112")
    for causal in rechazados.causales:
        print(causal.causal)
```

Todos los métodos aceptan además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)).
