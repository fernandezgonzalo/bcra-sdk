# BCRA-SDK

SDK no oficial e inmutado por `httpx` para las APIs públicas del Banco Central de la República Argentina (BCRA).
Soporta flujos síncronos y asíncronos sobre la misma instancia, y estructura las respuestas en dataclasses fuertemente tipadas.

## Instalación

Aún no está publicado en PyPI. Se instala desde el repositorio de GitHub:

```bash
uv add "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.4"
# o con pip
pip install "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.4"
```

> Reemplaza `v0.0.4` con la versión que desees instalar. Consulta [releases](https://github.com/fernandezgonzalo/bcra-sdk/releases).

## Uso rápido

`BCRAClient` es un único cliente que organiza los endpoints por dominio (`deudores`, `cheques`, `estadisticas_cambiarias`).
Con el context manager se gestionan los recursos y el pool de conexiones.

### Síncrono

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    reporte = bcra.deudores.get_deudas(cuit="20111111112")
    print(reporte.denominacion)
```

### Asíncrono

```python
import asyncio
from bcra_sdk import BCRAClient

async def main():
    async with BCRAClient() as bcra:
        cotizaciones = await bcra.estadisticas_cambiarias.aget_cotizaciones("2024-06-12")
        for c in cotizaciones.detalle:
            print(c.codigoMoneda, c.tipoCotizacion)

if __name__ == "__main__":
    asyncio.run(main())
```

## Recursos y endpoints

Cada dominio expone un resource con sus métodos tipados.

### Deudores (`bcra.deudores`)

| Método | Endpoint |
|--------|----------|
| `get_deudas(cuit)` | `GET /centraldedeudores/v1.0/Deudas/{cuit}` |
| `get_deudas_historicas(identification)` | `GET /CentralDeDeudores/v1.0/Deudas/Historicas/{identification}` |
| `get_cheques_rechazados(identification)` | `GET /centraldedeudores/v1.0/Deudas/ChequesRechazados/{identification}` |

### Cheques (`bcra.cheques`)

| Método | Endpoint |
|--------|----------|
| `get_entidades()` | `GET /cheques/v1.0/entidades` |
| `get_cheque_denunciado(codigo_entidad, numero_cheque)` | `GET /cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}` |

### Estadísticas cambiarias (`bcra.estadisticas_cambiarias`)

| Método | Endpoint |
|--------|----------|
| `get_divisas()` | `GET /estadisticascambiarias/v1.0/Maestros/Divisas` |
| `get_cotizaciones(fecha=None)` | `GET /estadisticascambiarias/v1.0/Cotizaciones` |
| `get_evolucion_moneda(moneda, fechadesde=None, fechahasta=None, limit=None, offset=None)` | `GET /estadisticascambiarias/v1.0/Cotizaciones/{moneda}` |

## Versionado de endpoints

Cada endpoint resuelve por defecto la versión más reciente. El SDK expone las versiones disponibles y su deprecación:

```python
bcra.estadisticas_cambiarias.versions("get_cotizaciones")
# {"1.0": {"deprecated": False}}
```

Es posible forzar una versión específica como escape hatch avanzado:

```python
bcra.deudores.get_deudas(cuit="123", version="1.0")
```

Si se pide una versión inexistente se lanza `BCRAEndpointVersionError` listando las disponibles y su estado. Las versiones deprecadas emiten un `DeprecationWarning`.

## Errores

- `BCRAError` — base de la jerarquía.
- `BCRAHTTPError` — respuestas 4xx/5xx del BCRA (expone `status_code` y `message`).
- `BCRAEndpointVersionError` — se pidió una versión de endpoint inexistente.

## Logging

La librería no configura handlers (best practice). Usa el logger `bcra_sdk` con un `NullHandler` por defecto. Para habilitar logs:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("bcra_sdk").setLevel(logging.DEBUG)
```

## Tests

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
```

El SDK soporta Python 3.11 hasta 3.15. Para correr los tests en todas las versiones con tox (usando `uv` como instalador via el plugin `tox-uv`):

```bash
uv run tox
```

tox define los envs `py311`...`py315` en `pyproject.toml` (sección `[tool.tox]`) como única fuente de verdad de las versiones soportadas. También se puede correr una sola version:

```bash
uv run tox -e py311
```

`uv` descarga la versión de Python indicada si no está instalada. En CI, el job `test` del workflow `lint.yml` repite la misma matrix llamando a `tox -e py3XX` por job (en paralelo).

## Licencia

MIT
