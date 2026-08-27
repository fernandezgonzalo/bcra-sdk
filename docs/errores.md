# Errores

Todas las excepciones del SDK cuelgan de una base común.

| Excepción | Descripción |
|-----------|-------------|
| `BCRAError` | Base de la jerarquía. `except BCRAError` captura todos los errores del SDK |
| `BCRAHTTPError` | Responde a respuestas 4xx/5xx del BCRA. Expone `status_code` y `message` |
| `BCRAEndpointVersionError` | Se pidió una versión de endpoint inexistente |

## `BCRAHTTPError`

Se lanza desde el transporte cuando el BCRA responde con un código de error HTTP. Es una
subclase de `BCRAError` y expone dos atributos:

```python
from bcra_sdk import BCRAClient, BCRAHTTPError

try:
    with BCRAClient() as bcra:
        bcra.deudores.get_deudas(cuit="20111111112")
except BCRAHTTPError as err:
    print(err.status_code)  # por ejemplo 404
    print(err.message)      # body de la respuesta
```

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
