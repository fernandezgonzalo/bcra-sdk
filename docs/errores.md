# Errores

Todas las excepciones del SDK cuelgan de una base común.

| Excepción | Descripción |
|-----------|-------------|
| `BCRAError` | Base de la jerarquía. `except BCRAError` captura todos los errores del SDK |
| `BCRAHTTPError` | Responde a respuestas 4xx/5xx del BCRA. Expone `status_code`, `message`, `response` y `reason` |
| `BCRAConnectionError` | Error de red/conexión al intentar comunicarse con el BCRA |
| `BCRATimeoutError` | Subclase de `BCRAConnectionError`. La petición superó el tiempo de espera |
| `BCRAEndpointVersionError` | Se pidió una versión de endpoint inexistente |

## `BCRAHTTPError`

Se lanza desde el transporte cuando el BCRA responde con un código de error HTTP. Es una
subclase de `BCRAError` y expone los siguientes atributos:

- `status_code`: el código de estado HTTP.
- `message`: el body de la respuesta.
- `response`: la `httpx.Response` completa (útil para inspeccionar headers como
  `Retry-After`).
- `reason`: la frase de razón HTTP asociada al código (p. ej. "Not Found").

```python
from bcra_sdk import BCRAClient, BCRAHTTPError

try:
    with BCRAClient() as bcra:
        bcra.deudores.get_deudas(cuit="20111111112")
except BCRAHTTPError as err:
    print(err.status_code)  # por ejemplo 404
    print(err.message)  # body de la respuesta
    print(err.reason)  # "Not Found"
```

## `BCRAConnectionError` y `BCRATimeoutError`

Errores de red quedan envueltos por el SDK y también derivan de `BCRAError`, así que un
único `except BCRAError` sigue capturando todo:

```python
from bcra_sdk import BCRAError, BCRATimeoutError

try:
    with BCRAClient() as bcra:
        bcra.cheques.get_entidades()
except BCRATimeoutError:
    print("El BCRA tardó demasiado en responder")
except BCRAError as err:
    print(err)
```

Los timeouts se reintentan automáticamente según la política de retry (ver
[Reintentos](retry.md)).

## `BCRAEndpointVersionError`

Se lanza al pedir una versión de endpoint que no existe. El mensaje lista las versiones
disponibles y su estado (ver [Versionado de endpoints](versionado.md)).

## Manejo combinado

Como todas derivan de `BCRAError`, alcanza con capturar la base para cubrir todos los
casos:

```python
from bcra_sdk import BCRAError

try:
    with BCRAClient() as bcra:
        bcra.cheques.get_entidades()
except BCRAError as err:
    print(err)
```
