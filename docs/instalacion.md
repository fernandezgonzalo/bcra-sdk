# Instalación

## Requisitos

- Python >= 3.11 (se soporta hasta Python 3.15 inclusive)

## Desde el repositorio

El paquete aún no está publicado en PyPI. Se instala directamente desde GitHub.

Con `uv`:

```bash
uv add "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
```

Con `pip`:

```bash
pip install "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
```

> Reemplazá `v0.0.10` por la versión que quieras instalar. Consultá las
> [releases](https://github.com/fernandezgonzalo/bcra-sdk/releases) y el
> [changelog](changelog.md).

## Con CLI

El CLI (`bcra`) es opcional y se instala con el extra `[cli]`:

```bash
uv add "bcra-sdk[cli] @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
# o con pip
pip install "bcra-sdk[cli] @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.10"
```

Sin el extra, el comando `bcra` queda instalado pero muestra un error claro
al ejecutarlo pidiendo instalar `bcra-sdk[cli]`.

Véase [CLI](cli.md) para la lista de comandos.
