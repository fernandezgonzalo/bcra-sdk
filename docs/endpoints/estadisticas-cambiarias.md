# Estadísticas cambiarias (`bcra.estadisticas_cambiarias`)

Endpoints de estadísticas cambiarias del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_divisas()` | `GET /estadisticascambiarias/v1.0/Maestros/Divisas` |
| `get_cotizaciones(fecha=None)` | `GET /estadisticascambiarias/v1.0/Cotizaciones` |
| `get_evolucion_moneda(moneda, fechadesde=None, fechahasta=None, limit=None, offset=None)` | `GET /estadisticascambiarias/v1.0/Cotizaciones/{moneda}` |

## `get_divisas()`

Devuelve el listado de divisas.

Sin parámetros. Devuelve `ResultGetDivisasV1`:

- `divisas: list[Divisa]`
    - `Divisa.codigo: str`
    - `Divisa.denominacion: str`

```python
with BCRAClient() as bcra:
    divisas = bcra.estadisticas_cambiarias.get_divisas()
    for divisa in divisas.divisas:
        print(divisa.codigo, divisa.denominacion)
```

## `get_cotizaciones(fecha=None)`

Devuelve las cotizaciones de monedas para una fecha (o las más recientes si no se indica).

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `fecha` | `str \| None` | Fecha en formato `AAAA-MM-DD`. Sin fecha, devuelve la última disponible |

Devuelve `ResultGetCotizacionesV1`:

- `fecha: str | None`
- `detalle: list[Cotizacion]`
    - `Cotizacion.codigoMoneda: str`
    - `Cotizacion.descripcion: str`
    - `Cotizacion.tipoPase: float`
    - `Cotizacion.tipoCotizacion: float`

```python
with BCRAClient() as bcra:
    cotizaciones = bcra.estadisticas_cambiarias.get_cotizaciones("2024-06-12")
    for c in cotizaciones.detalle:
        print(c.codigoMoneda, c.tipoCotizacion)
```

## `get_evolucion_moneda(moneda, fechadesde=None, fechahasta=None, limit=None, offset=None)`

Devuelve la evolución de cotizaciones de una moneda, con paginado opcional.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `moneda` | `str` | Código de la moneda (por ejemplo `USD`) (obligatorio) |
| `fechadesde` | `str \| None` | Fecha de inicio (`AAAA-MM-DD`) |
| `fechahasta` | `str \| None` | Fecha de fin (`AAAA-MM-DD`) |
| `limit` | `int \| None` | Cantidad máxima de resultados |
| `offset` | `int \| None` | Desplazamiento para paginar |

Devuelve `ResultGetEvolucionMonedaV1`:

- `resultset: Resultset` (metadatos de paginación)
    - `Resultset.count: int`
    - `Resultset.offset: int`
    - `Resultset.limit: int`
- `cotizaciones: list[ResultGetCotizacionesV1]`
    - cada elemento con `fecha` y `detalle` (ver `get_cotizaciones`)

```python
with BCRAClient() as bcra:
    evolucion = bcra.estadisticas_cambiarias.get_evolucion_moneda(
        moneda="USD",
        fechadesde="2024-01-01",
        fechahasta="2024-06-30",
        limit=10,
    )
    print(evolucion.resultset.count)
```

Todos los métodos aceptan además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)).
