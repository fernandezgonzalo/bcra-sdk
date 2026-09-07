# CLI

El CLI (`bcra`) es **opcional**: se instala con el extra `[cli]` y no agrega
dependencias al core del SDK.

```bash
pip install "bcra-sdk[cli] @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
```

Si ejecutás `bcra` sin instalar el extra, el comando muestra un error claro
indicando cómo instalarlo:

## Comandos

Expone los mismos endpoints que el SDK organizados por namespace:

```bash
bcra deudores deudas 20111111112
bcra deudores deudas-historicas 20234567891
bcra deudores cheques-rechazados 20111111112

bcra cheques entidades
bcra cheques cheque-denunciado 11 752395

bcra cambiarias divisas
bcra cambiarias cotizaciones --fecha 2024-06-12
bcra cambiarias evolucion-moneda USD --desde 2024-01-01 --hasta 2024-06-12

bcra monetarias monetarias
bcra monetarias evolucion-variable 16 --desde 2025-01-01 --hasta 2025-06-01
bcra monetarias metodologias
bcra monetarias metodologia 1

bcra transparencia cajas-ahorros --entidad 11
bcra transparencia paquetes-productos
bcra transparencia plazos-fijos
bcra transparencia prestamos-prendarios
bcra transparencia prestamos-hipotecarios
bcra transparencia prestamos-personales
bcra transparencia tarjetas-credito
```

`bcra --help` lista todos los comandos y cada subcomando tiene su propio
`--help`.

## Formato de salida

Por defecto la salida es JSON (listo para pipar con `jq` o procesar). Con
`--format table` (opción global, va **antes** del subcomando) se muestra una
vista tabular:

```bash
bcra --format table monetarias monetarias
bcra --format table transparencia tarjetas-credito
```

## Ayuda y autocompletado

- `bcra --version`: muestra la versión del SDK instalada.
- `bcra --install-completion`: instala el autocompletado de shell
  (bash/zsh/fish).
- `bcra --show-completion`: muestra el script de autocompletado para copiarlo.
