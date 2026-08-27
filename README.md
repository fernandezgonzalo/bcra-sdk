# BCRA-SDK

SDK no oficial e inmutado por `httpx` para las APIs públicas del Banco Central de la República Argentina (BCRA).

`BCRAClient` es un único cliente que organiza los endpoints por dominio (`deudores`, `cheques`, `estadisticas_cambiarias`)
y estructura las respuestas en dataclasses fuertemente tipadas. Los endpoints están versionados, resuelven por defecto
la versión más reciente y permiten forzar una versión.

## Documentación

Documentación completa en [`docs/`](docs/index.md):

- [Guía rápida](docs/guia-rapida.md)
- [Endpoints](docs/index.md#contenido): deudores, cheques, estadísticas cambiarias
- [Versionado de endpoints](docs/versionado.md)
- [Errores](docs/errores.md)
- [Logging](docs/logging.md)
- [Contribución](docs/contribucion.md)

## Instalación

Aún no está publicado en PyPI. Se instala desde el repositorio de GitHub:

```bash
uv add "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.5"
# o con pip
pip install "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.5"
```

> Reemplaza `v0.0.5` con la versión que desees instalar. Consulta [releases](https://github.com/fernandezgonzalo/bcra-sdk/releases).

## Uso rápido

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    reporte = bcra.deudores.get_deudas(cuit="20111111112")
    print(reporte.denominacion)

    cotizaciones = bcra.estadisticas_cambiarias.get_cotizaciones("2024-06-12")
    for c in cotizaciones.detalle:
        print(c.codigoMoneda, c.tipoCotizacion)
```

## Tests

```bash
uv sync
uv run pytest
uv run pre-commit run --all-files
```

El SDK soporta Python 3.11 hasta 3.15. Para correr los tests en todas las versiones con tox:

```bash
uv run tox
```

Cada ejecución de test valida cobertura: debe ser **100%** (`fail_under = 100`).

## Licencia

MIT
