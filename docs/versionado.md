# Versionado de endpoints

Los endpoints del BCRA están versionados. Cada resource registra las versiones de cada
endpoint (`_register_version`) y las resuelve con `_resolve_version`.

## Comportamiento por defecto

Si no se indica nada, cada endpoint resuelve **la versión más reciente registrada**, de
forma independiente a los demás endpoints del mismo resource.

## Consultar versiones disponibles

`Resource.versions(endpoint)` devuelve las versiones de un endpoint y su estado de deprecación:

```python
bcra.estadisticas_cambiarias.versions("get_cotizaciones")
# {"1.0": {"deprecated": False}}
```

Con una versión deprecada o varias versiones:

```python
bcra.estadisticas_cambiarias.versions("get_cotizaciones")
# {"1.0": {"deprecated": True}, "2.0": {"deprecated": False}}
```

## Forzar una versión (escape hatch)

Todos los métodos de endpoint aceptan el parámetro keyword-only `version=`:

```python
bcra.deudores.get_deudas(cuit="20111111112", version="1.0")
```

### Versión inexistente

Si se pide una versión que el endpoint no tiene, se lanza `BCRAEndpointVersionError`
listando las versiones disponibles y su estado:

```python
bcra.deudores.get_deudas(cuit="20111111112", version="9.0")
# BCRAEndpointVersionError: get_deudas no tiene version '9.0'. Disponibles: ['1.0']
```

### Versión deprecada

Si la versión resuelta está deprecada, se emite un `DeprecationWarning`:

```python
import warnings

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    bcra.deudores.get_deudas(cuit="20111111112", version="1.0")
    # w[0].category == DeprecationWarning
```

Naming: los modelos de respuesta de los endpoints se nombran
`Result{Metodo}V{Version}` (por ejemplo `ResultGetCotizacionesV1`).
