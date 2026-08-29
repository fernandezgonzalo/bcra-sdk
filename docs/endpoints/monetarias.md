# Estadísticas monetarias (`bcra.monetarias`)

Endpoints de estadísticas monetarias del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_monetarias()` | `GET /estadisticas/v4.0/monetarias` |
| `get_evolucion_variable(idVariable, desde=None, hasta=None, offset=None, limit=None)` | `GET /estadisticas/v4.0/monetarias/{idVariable}` |

## `get_monetarias()`

Devuelve el listado de variables monetarias con su paginado.

Sin parámetros. Devuelve `ResultGetMonetariasV1`:

- `resultset: Resultset` (metadatos de paginación)
    - `Resultset.count: int`
    - `Resultset.offset: int`
    - `Resultset.limit: int`
- `variables: list[VariableMonetaria]`
    - `VariableMonetaria.idVariable: int`
    - `VariableMonetaria.descripcion: str`
    - `VariableMonetaria.categoria: str`
    - `VariableMonetaria.tipoSerie: str`
    - `VariableMonetaria.periodicidad: str` (`D`, `M`, `T`/`Q`)
    - `VariableMonetaria.unidadExpresion: str`
    - `VariableMonetaria.moneda: str` (`ML`, `ME`, `MEyML`, `ARS`, `USD`)
    - `VariableMonetaria.primerFechaInformada: str`
    - `VariableMonetaria.ultFechaInformada: str`
    - `VariableMonetaria.ultValorInformado: float`

```python
with BCRAClient() as bcra:
    monetarias = bcra.monetarias.get_monetarias()
    print(monetarias.resultset.count)
    for variable in monetarias.variables:
        print(variable.idVariable, variable.descripcion)
```

El endpoint acepta además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)), y tiene su par
asíncrono `await bcra.monetarias.aget_monetarias()`.

## `get_evolucion_variable()`

Devuelve la evolución (serie histórica) de una variable monetaria.

Parámetros:
- `idVariable` (requerido): ID de la variable, obtenible con `get_monetarias()`.
- `desde` / `hasta`: límites del rango, como `str` ISO (`YYYY-MM-DD`) o
  `datetime.date`. Opcionales.
- `offset`: registros a descartar para el paginado. Opcional (default del
  servidor: 0).
- `limit`: registros a retornar, máximo 3000. Opcional (default del servidor:
  1000).

Devuelve `ResultGetEvolucionVariableV1`:

- `resultset: Resultset` (metadatos de paginación)
- `series: list[SerieMonetaria]`
    - `SerieMonetaria.idVariable: int`
    - `SerieMonetaria.detalle: list[PuntoSerie]`
        - `PuntoSerie.fecha: str` (`YYYY-MM-DD`)
        - `PuntoSerie.valor: float`

```python
with BCRAClient() as bcra:
    evolucion = bcra.monetarias.get_evolucion_variable(
        idVariable=1,
        desde="2025-05-20",
        hasta="2025-05-26",
        limit=10,
    )
    print(evolucion.resultset.count)
    for punto in evolucion.series[0].detalle:
        print(punto.fecha, punto.valor)
```

La compresión de la respuesta (`accept-encoding: gzip` o `br`) la negocia
automáticamente `httpx` según los extras instalados; no requiere configuración.
El par asíncrono es
`await bcra.monetarias.aget_evolucion_variable(...)`.
