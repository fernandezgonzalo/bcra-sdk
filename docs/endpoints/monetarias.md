# Estadísticas monetarias (`bcra.monetarias`)

Endpoints de estadísticas monetarias del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_monetarias()` | `GET /estadisticas/v4.0/monetarias` |

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
