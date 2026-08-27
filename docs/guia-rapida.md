# Guía rápida

`BCRAClient` organiza los endpoints por dominio: `deudores`, `cheques` y
`estadisticas_cambiarias`. Usá los context managers para gestionar los recursos y el
pool de conexiones de HTTP.

## Síncrono

```python
from bcra_sdk import BCRAClient

with BCRAClient() as bcra:
    reporte = bcra.deudores.get_deudas(cuit="20111111112")
    print(reporte.denominacion)
    for periodo in reporte.periodos:
        print(periodo.periodo)
```

## Asíncrono

`BCRAClient` se abre y cierra con `async with`, y cada endpoint tiene su par asíncrono
con prefijo `a` (por ejemplo `aget_cotizaciones`), con la misma firma y devolviendo el
mismo modelo que su versión síncrona.

```python
from bcra_sdk import BCRAClient

async def main():
    async with BCRAClient() as bcra:
        cotizaciones = await bcra.estadisticas_cambiarias.aget_cotizaciones("2024-06-12")
        for c in cotizaciones.detalle:
            print(c.codigoMoneda, c.tipoCotizacion)
        reporte = await bcra.deudores.aget_deudas(cuit="20111111112")
        print(reporte.denominacion)

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

## Próximos pasos

- [Endpoints de deudores](endpoints/deudores.md)
- [Endpoints de cheques](endpoints/cheques.md)
- [Endpoints de estadísticas cambiarias](endpoints/estadisticas-cambiarias.md)
- [Versionado de endpoints](versionado.md)
