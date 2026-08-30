# Régimen de Transparencia (`bcra.regimen_de_transparencia`)

Endpoints de la API pública (sin autenticación) del Régimen de Transparencia del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_cajas_ahorros(codigoEntidad=None)` | `GET /transparencia/v1.0/CajasAhorros` |
| `get_paquetes_productos(codigoEntidad=None)` | `GET /transparencia/v1.0/PaquetesProductos` |
| `get_plazos_fijos(codigoEntidad=None)` | `GET /transparencia/v1.0/PlazosFijos` |
| `get_prestamos_prendarios(codigoEntidad=None)` | `GET /transparencia/v1.0/Prestamos/Prendarios` |

## `get_cajas_ahorros()`

Devuelve los productos de cajas de ahorro informados por las entidades en el
Régimen de Transparencia. La respuesta no incluye metadatos de paginación.

Parámetros:
- `codigoEntidad` (opcional): código numérico de la entidad financiera para
  filtrar el listado (los códigos se pueden consultar con `get_entidades` de
  `bcra.cheques`). Si no se informa, devuelve todas las entidades.

Devuelve `ResultGetCajasAhorrosV1`:

- `cajas_ahorros: list[CajaAhorro]`
    - `CajaAhorro.codigoEntidad: int`
    - `CajaAhorro.descripcionEntidad: str` (nombre oficial o razón social)
    - `CajaAhorro.fechaInformacion: str` (`YYYY-MM-DD`, fecha de actualización)
    - `CajaAhorro.procesoSimplificadoDebidaDiligencia: str` (`SI`/`NO`)

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    todas = bcra.regimen_de_transparencia.get_cajas_ahorros()
    for caja in todas.cajas_ahorros:
        print(caja.codigoEntidad, caja.descripcionEntidad)

    filtradas = bcra.regimen_de_transparencia.get_cajas_ahorros(codigoEntidad=11)
```

El endpoint acepta además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)), y tiene su par
asíncrono `await bcra.regimen_de_transparencia.aget_cajas_ahorros(...)`.

Un `codigoEntidad` sin datos levanta `BCRAHTTPError` (404), igual que los
errores internos del servidor (500).

## `get_paquetes_productos()`

Devuelve los paquetes de productos informados por las entidades en el Régimen
de Transparencia. La respuesta no incluye metadatos de paginación.

Parámetros:
- `codigoEntidad` (opcional): código numérico de la entidad financiera para
  filtrar el listado (los códigos se pueden consultar con `get_entidades` de
  `bcra.cheques`). Si no se informa, devuelve todas las entidades.

Devuelve `ResultGetPaquetesProductosV1`:

- `paquetes_productos: list[PaqueteProducto]`
    - `PaqueteProducto.codigoEntidad: int` (código de la entidad informante)
    - `PaqueteProducto.descripcionEntidad: str` (nombre oficial o razón social)
    - `PaqueteProducto.fechaInformacion: str` (`YYYY-MM-DD`, fecha de actualización)
    - `PaqueteProducto.nombreCompleto: str` (nombre completo del paquete)
    - `PaqueteProducto.nombreCorto: str` (nombre corto del paquete)
    - `PaqueteProducto.comisionMaximaMantenimiento: float` (comisión máxima de mantenimiento)
    - `PaqueteProducto.ingresoMinimoMensual: float` (ingreso mínimo mensual solicitado)
    - `PaqueteProducto.antiguedadLaboralMinimaMeses: int` (antigüedad laboral mínima en meses)
    - `PaqueteProducto.edadMaximaSolicitada: int` (edad máxima solicitada)
    - `PaqueteProducto.beneficiarios: str` (beneficiarios del paquete)
    - `PaqueteProducto.segmento: str` (segmento: Básico, Premium gold, etc.)
    - `PaqueteProducto.productosIntegrantes: str` (productos que integran el paquete)
    - `PaqueteProducto.territorioValidez: str` (territorio de validez de la oferta)
    - `PaqueteProducto.masInformacion: str | None` (información adicional, puede ser `None`)

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    todos = bcra.regimen_de_transparencia.get_paquetes_productos()
    for p in todos.paquetes_productos:
        print(p.codigoEntidad, p.nombreCorto, p.segmento)

    filtrados = bcra.regimen_de_transparencia.get_paquetes_productos(codigoEntidad=14)
```

El endpoint acepta además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)), y tiene su par
asíncrono
`await bcra.regimen_de_transparencia.aget_paquetes_productos(...)`.

Un `codigoEntidad` sin datos levanta `BCRAHTTPError` (404), igual que los
errores internos del servidor (500).

## `get_plazos_fijos()`

Devuelve los plazos fijos que comercializa cada entidad en el Régimen de
Transparencia. La respuesta no incluye metadatos de paginación.

Parámetros:
- `codigoEntidad` (opcional): código numérico de la entidad financiera para
  filtrar el listado (los códigos se pueden consultar con `get_entidades` de
  `bcra.cheques`). Si no se informa, devuelve todas las entidades.

Devuelve `ResultGetPlazosFijosV1`:

- `plazos_fijos: list[PlazoFijo]`
    - `PlazoFijo.codigoEntidad: int` (código de la entidad informante)
    - `PlazoFijo.descripcionEntidad: str` (nombre oficial o razón social)
    - `PlazoFijo.fechaInformacion: str` (`YYYY-MM-DD`, fecha de actualización)
    - `PlazoFijo.nombreCompleto: str` (nombre completo del tipo de plazo fijo)
    - `PlazoFijo.nombreCorto: str` (nombre corto del tipo de plazo fijo)
    - `PlazoFijo.denominacion: str | None` (Pesos, Dólares estadounidenses, Euros, UVAs, UVIs; puede ser `None`)
    - `PlazoFijo.montoMinimoInvertir: float` (monto mínimo a invertir)
    - `PlazoFijo.plazoMinimoInvertirDias: int` (plazo mínimo en días: 30, 60, 90, 180, 360)
    - `PlazoFijo.canalConstitucion: str` (canal de constitución: Home banking, Cajero automático, etc.)
    - `PlazoFijo.tasaEfectivaAnualMinima: float` (tasa efectiva anual mínima)
    - `PlazoFijo.territorioValidez: str` (territorio de validez de la oferta)
    - `PlazoFijo.masInformacion: str | None` (información adicional, puede ser `None`)

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    todos = bcra.regimen_de_transparencia.get_plazos_fijos()
    for pf in todos.plazos_fijos:
        print(pf.codigoEntidad, pf.nombreCorto, pf.tasaEfectivaAnualMinima)

    filtrados = bcra.regimen_de_transparencia.get_plazos_fijos(codigoEntidad=7)
```

El endpoint acepta además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)), y tiene su par
asíncrono
`await bcra.regimen_de_transparencia.aget_plazos_fijos(...)`.

Un `codigoEntidad` sin datos levanta `BCRAHTTPError` (404), igual que los
errores internos del servidor (500).

## `get_prestamos_prendarios()`

Devuelve los préstamos prendarios que ofrece cada entidad en el Régimen de
Transparencia. La respuesta no incluye metadatos de paginación.

Parámetros:
- `codigoEntidad` (opcional): código numérico de la entidad financiera para
  filtrar el listado (los códigos se pueden consultar con `get_entidades` de
  `bcra.cheques`). Si no se informa, devuelve todas las entidades.

Devuelve `ResultGetPrestamosPrendariosV1`:

- `prestamos_prendarios: list[PrestamoPrendario]`
    - `PrestamoPrendario.codigoEntidad: int` (código de la entidad informante)
    - `PrestamoPrendario.descripcionEntidad: str` (nombre oficial o razón social)
    - `PrestamoPrendario.fechaInformacion: str` (`YYYY-MM-DD`, fecha de actualización)
    - `PrestamoPrendario.nombreCompleto: str` (nombre completo del préstamo)
    - `PrestamoPrendario.nombreCorto: str` (nombre corto del préstamo)
    - `PrestamoPrendario.denominacion: str` (Pesos, Dólares estadounidenses, UVA)
    - `PrestamoPrendario.montoMinimoOtorgable: float` (monto mínimo otorgable)
    - `PrestamoPrendario.montoMaximoOtorgable: float` (monto máximo otorgable)
    - `PrestamoPrendario.plazoMaximoOtorgable: int` (plazo máximo en meses)
    - `PrestamoPrendario.ingresoMinimoMensual: float` (ingreso mínimo mensual solicitado)
    - `PrestamoPrendario.antiguedadLaboralMinimaMeses: int` (antigüedad laboral mínima en meses)
    - `PrestamoPrendario.edadMaximaSolicitada: int` (edad máxima solicitada)
    - `PrestamoPrendario.relacionCuotaIngreso: int` (relación cuota/ingreso en %)
    - `PrestamoPrendario.relacionMontoTasacion: int` (relación monto/tasación en %)
    - `PrestamoPrendario.destinoFondos: str` (destino de los fondos)
    - `PrestamoPrendario.beneficiario: str` (beneficiario del préstamo)
    - `PrestamoPrendario.cargoMaximoCancelacionAnticipada: int` (cargo máximo por cancelación anticipada, 0-99 %)
    - `PrestamoPrendario.tasaEfectivaAnualMaxima: float` (tasa efectiva anual máxima)
    - `PrestamoPrendario.tipoTasa: str` (Fija, Variable, Mixta)
    - `PrestamoPrendario.costoFinancieroEfectivoTotalMaximo: float` (costo financiero efectivo total máximo)
    - `PrestamoPrendario.cuotaInicial: float` (cuota inicial a plazo máximo cada $10.000)
    - `PrestamoPrendario.territorioValidez: str` (territorio de validez de la oferta)
    - `PrestamoPrendario.masInformacion: str | None` (información adicional, puede ser `None`)

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    todos = bcra.regimen_de_transparencia.get_prestamos_prendarios()
    for pp in todos.prestamos_prendarios:
        print(pp.codigoEntidad, pp.nombreCorto, pp.tasaEfectivaAnualMaxima)

    filtrados = bcra.regimen_de_transparencia.get_prestamos_prendarios(codigoEntidad=7)
```

El endpoint acepta además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)), y tiene su par
asíncrono
`await bcra.regimen_de_transparencia.aget_prestamos_prendarios(...)`.

Un `codigoEntidad` sin datos levanta `BCRAHTTPError` (404), igual que los
errores internos del servidor (500).
