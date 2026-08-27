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

`BCRAClient` se puede abrir con `async with` (se cierra el pool asíncrono), pero los
métodos de los endpoints (por ejemplo `get_cotizaciones`) son actualmente **síncronos**:
la capa asíncrona (`arequest`, `aclose`) ya existe en el transporte, pero aún no hay
métodos `aget_*` expuestos por los resources.

```python
from bcra_sdk import BCRAClient

async def main():
    async with BCRAClient() as bcra:
        # El pool async se gestiona con aclose() al salir del contexto.
        await bcra.aclose()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

## Próximos pasos

- [Endpoints de deudores](endpoints/deudores.md)
- [Endpoints de cheques](endpoints/cheques.md)
- [Endpoints de estadísticas cambiarias](endpoints/estadisticas-cambiarias.md)
- [Versionado de endpoints](versionado.md)
