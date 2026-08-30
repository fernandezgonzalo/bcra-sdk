# BCRA-SDK

[![CI](https://github.com/fernandezgonzalo/bcra-sdk/actions/workflows/lint.yml/badge.svg)](https://github.com/fernandezgonzalo/bcra-sdk/actions/workflows/lint.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11–3.15](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](pyproject.toml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](#cobertura)
[![Documentation](https://readthedocs.org/projects/bcra-sdk/badge/?version=latest)](https://bcra-sdk.readthedocs.io/)

SDK no oficial e impulsado por `httpx` para las APIs públicas del Banco Central de la República Argentina (BCRA).

`BCRAClient` es un único cliente que organiza los endpoints por dominio (`deudores`, `cheques`, `estadisticas_cambiarias`, `monetarias`, `regimen_de_transparencia`)
y estructura las respuestas en dataclasses fuertemente tipadas. Los endpoints están versionados, resuelven por defecto
la versión más reciente y permiten forzar una versión.

Características:

- Sync y async en la misma instancia (`with` / `async with`), con un par `aget_*` por endpoint.
- Reintentos automáticos ante errores transitorios con backoff exponencial (configurables vía `RetryPolicy`).
- Errores de red, timeout y HTTP unificados bajo `BCRAError`.
- Inputs tipados: fechas como `str` ISO o `datetime.date`; validación de CUIT.

## Cobertura

El SDK cubre las **5 APIs públicas** que el BCRA ofrece en
[`api.bcra.gob.ar`](https://www.bcra.gob.ar/apis-banco-central/): Central de
Deudores, Cheques denunciados, Estadísticas Cambiarias, Estadísticas
Monetarias y Régimen de Transparencia. Son **19 endpoints, todos con su
variante asíncrona** `aget_*` (mismo transporte, reintentos y errores).

| API oficial (BCRA) | Resource | Endpoints |
|---|---|---|
| Central de Deudores | `bcra.deudores` | `get_deudas`, `get_deudas_historicas`, `get_cheques_rechazados` |
| Cheques denunciados | `bcra.cheques` | `get_entidades`, `get_cheque_denunciado` |
| Estadísticas Cambiarias | `bcra.estadisticas_cambiarias` | `get_divisas`, `get_cotizaciones`, `get_evolucion_moneda` |
| Estadísticas Monetarias | `bcra.monetarias` | `get_monetarias`, `get_evolucion_variable`, `get_metodologias`, `get_metodologia` |
| Régimen de Transparencia | `bcra.regimen_de_transparencia` | `get_cajas_ahorros`, `get_paquetes_productos`, `get_plazos_fijos`, `get_prestamos_prendarios`, `get_prestamos_hipotecarios`, `get_prestamos_personales`, `get_tarjetas_credito` |

Estadísticas Monetarias usa la versión actual `v4.0` (que incluye Principales
Variables; `v1.0`–`v3.0` quedaron deprecadas por el BCRA). Cada endpoint
registra sus versiones disponibles y se resuelve por defecto a la más reciente;
consultalas con `bcra.<namespace>.versions("<endpoint>")`. La referencia
completa por namespace está en [`docs/endpoints/`](docs/endpoints/).

## Documentación

Documentación completa en [`docs/`](docs/index.md):

- [Guía rápida](docs/guia-rapida.md)
- [Endpoints](docs/index.md#contenido): deudores, cheques, estadísticas cambiarias, monetarias, régimen de transparencia
- [API Reference](docs/api/cliente.md): cliente, recursos, modelos y errores
- [Versionado de endpoints](docs/versionado.md)
- [Reintentos](docs/retry.md)
- [Errores](docs/errores.md)
- [Logging](docs/logging.md)
- [Contribución](docs/contribucion.md)

## Instalación

Aún no está publicado en PyPI. Se instala desde el repositorio de GitHub:

```bash
uv add "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
# o con pip
pip install "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
```

> Reemplaza `v0.0.10` con la versión que desees instalar. Consulta [releases](https://github.com/fernandezgonzalo/bcra-sdk/releases).

## Uso rápido

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    reporte = bcra.deudores.get_deudas(cuit="20111111112")
    print(reporte.denominacion)

    cotizaciones = bcra.estadisticas_cambiarias.get_cotizaciones("2024-06-12")
    for c in cotizaciones.detalle:
        print(c.codigoMoneda, c.tipoCotizacion)

    monetarias = bcra.monetarias.get_monetarias()
    for v in monetarias.variables:
        print(v.idVariable, v.descripcion)

    cajas = bcra.regimen_de_transparencia.get_cajas_ahorros(codigoEntidad=11)
    for caja in cajas.cajas_ahorros:
        print(caja.descripcionEntidad)

    paquetes = bcra.regimen_de_transparencia.get_paquetes_productos(codigoEntidad=11)
    for p in paquetes.paquetes_productos:
        print(p.nombreCorto, p.segmento)

    plazos = bcra.regimen_de_transparencia.get_plazos_fijos(codigoEntidad=11)
    for p in plazos.plazos_fijos:
        print(p.nombreCorto, p.tasaEfectivaAnualMinima)

    hipotecarios = bcra.regimen_de_transparencia.get_prestamos_hipotecarios(
        codigoEntidad=11
    )
    for h in hipotecarios.prestamos_hipotecarios:
        print(h.nombreCorto, h.tasaEfectivaAnualMaxima)

    personales = bcra.regimen_de_transparencia.get_prestamos_personales(
        codigoEntidad=11
    )
    for p in personales.prestamos_personales:
        print(p.nombreCorto, p.tasaEfectivaAnualMaxima)

    tarjetas = bcra.regimen_de_transparencia.get_tarjetas_credito(codigoEntidad=11)
    for t in tarjetas.tarjetas_credito:
        print(t.nombreCorto, t.segmento, t.tasaEfectivaAnualMaximaFinanciacion)
```

Uso asíncrono: todos los endpoints tienen su par `aget_*`. La misma instancia
sirve para sync (`with`) y async (`async with`).

```python
import asyncio

from bcra_sdk import BCRAClient


async def main():
    async with BCRAClient() as bcra:
        reporte = await bcra.deudores.aget_deudas(cuit="20111111112")
        for periodo in reporte.periodos:
            print(periodo.periodo)

        cotizaciones = await bcra.estadisticas_cambiarias.aget_cotizaciones(
            "2024-06-12"
        )
        for c in cotizaciones.detalle:
            print(c.codigoMoneda, c.tipoCotizacion)

        monetarias = await bcra.monetarias.aget_monetarias()
        for v in monetarias.variables:
            print(v.idVariable, v.descripcion)


asyncio.run(main())
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

Los tests usan respuestas reales del BCRA grabadas como cassettes (`tests/cassettes/`), por
lo que no requieren red. Para smoke tests en vivo contra la API (la suite `integration`,
deseleccionada por defecto):

```bash
uv run pytest -m integration --no-cov
```

Detalles en [`docs/testing.md`](docs/testing.md).

## Licencia

MIT
