# BCRA-SDK

SDK no oficial e impulsado por `httpx` para las APIs públicas del Banco Central de la República Argentina (BCRA).

`BCRAClient` es un único cliente que organiza los endpoints por dominio (`deudores`, `cheques`, `estadisticas_cambiarias`, `monetarias`, `regimen_de_transparencia`)
y estructura las respuestas en dataclasses fuertemente tipadas. Los endpoints están versionados, resuelven por defecto
la versión más reciente y permiten forzar una versión.

Características:

- Sync y async en la misma instancia (`with` / `async with`), con un par `aget_*` por endpoint.
- Reintentos automáticos ante errores transitorios con backoff exponencial (configurables vía `RetryPolicy`).
- Errores de red, timeout y HTTP unificados bajo `BCRAError`.
- Inputs tipados: fechas como `str` ISO o `datetime.date`; validación de CUIT.

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
uv add "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.8"
# o con pip
pip install "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.8"
```

> Reemplaza `v0.0.8` con la versión que desees instalar. Consulta [releases](https://github.com/fernandezgonzalo/bcra-sdk/releases).

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

Uso asíncrono: cada endpoint tiene su par `aget_*`.

```python
import asyncio

from bcra_sdk import BCRAClient


async def main():
    async with BCRAClient() as bcra:
        reporte = await bcra.deudores.aget_deudas(cuit="20111111112")
        for periodo in reporte.periodos:
            print(periodo.periodo)


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
