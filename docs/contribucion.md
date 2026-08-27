# Contribución

Gracias por querer contribuir. El proyecto usa `uv` para gestión de dependencias,
`src-layout` y un conjunto de herramientas de calidad que se validan en CI y en pre-commit.

## Entorno

```bash
uv sync
```

## Calidad

Cada cambio debe pasar lint, format, type check y cobertura:

```bash
uv run pre-commit run --all-files
```

- **Lint y format**: `ruff` (check + format).
- **Type check**: `ty` (Astral). En CI corre con `uvx ty` / `uv check --ty-version`.
- **Cobertura**: se exige **100%** (`fail_under = 100`). Para ver líneas faltantes:

```bash
uv run pytest --cov-report=term-missing
```

## Documentación

La documentación vive en `docs/` y se compila con [MkDocs](https://www.mkdocs.org/) (theme
Material), que en CI/RTD se instala vía el grupo `docs` de `pyproject.toml`. Para levantarla
localmente:

```bash
uv run --group docs mkdocs serve
```

Y para validar un build de producción:

```bash
uv run --group docs mkdocs build --clean --strict
```

La publicación se hace desde ReadTheDocs: `.readthedocs.yaml` instala `uv`, sincroniza el
grupo `docs` y ejecuta `mkdocs build` hacia `$READTHEDOCS_OUTPUT`.

## Tests

```bash
uv run pytest                    # test suite + cobertura
uv run pytest tests/test_foo.py  # un archivo puntual
```

La suite default es determinista: usa respuestas reales del BCRA grabadas como cassettes en
`tests/cassettes/` (ver [`docs/testing.md`](testing.md)). Si la API cambia un contrato,
regrabalos con `uv run python scripts/record_cassettes.py`. Para los smoke tests en vivo:

```bash
uv run pytest -m integration --no-cov
```

El proyecto soporta Python 3.11 hasta 3.15. La fuente de verdad de las versiones es
`env_list` en la sección `[tool.tox]` de `pyproject.toml`. Para correr la suite en todas
las versiones (descarga los intérpretes con `uv` via el plugin `tox-uv`):

```bash
uv run tox
```

Y para una sola versión:

```bash
uv run tox -e py311
```

El CI (`.github/workflows/lint.yml`) repite la misma matrix: un job de `test` por version
(`tox -e py3XX`) en paralelo.

## Convenciones

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/), con scope,
  por ejemplo `feat(deudores): ...`, `fix(client): ...`.
- **PRs**: hacia `develop`, squash and merge.
- **Tests**: mockear `client.{namespace}._t.request` con `monkeypatch`. Para tests de
  error, el mock debe lanzar `BCRAHTTPError` directamente (no mockear una `httpx.Response`
  de error, porque `_raise_for_status` quedaría bypassed).
- **Modelos**: dataclasses planos (no Pydantic) con `from_dict` para deserializar.
  Naming: `Result{Metodo}V{Version}`.
- **No comentarios** en código salvo que se pidan explícitamente.

## Arquitectura (resumen)

- `BCRAClient` es el único punto de entrada; expone recursos por namespace
  (`client.deudores`, `client.cheques`, `client.estadisticas_cambiarias`).
- Cada resource (`Resource`) registra versiones por endpoint (`_register_version`) y las
  resuelve con `_resolve_version` (default: la más reciente; emite `DeprecationWarning`).
- `Transport` envuelve `httpx` y lanza `BCRAHTTPError` en cualquier 4xx/5xx.
- Única dependencia de runtime: `httpx`. La versión del paquete se deriva de git tags via
  `hatch-vcs`.
