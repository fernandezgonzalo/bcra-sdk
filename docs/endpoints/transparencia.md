# Régimen de Transparencia (`bcra.regimen_de_transparencia`)

Endpoints de la API pública (sin autenticación) del Régimen de Transparencia del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_cajas_ahorros(codigoEntidad=None)` | `GET /transparencia/v1.0/CajasAhorros` |
| `get_paquetes_productos(codigoEntidad=None)` | `GET /transparencia/v1.0/PaquetesProductos` |

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
