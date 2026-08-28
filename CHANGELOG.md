# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Conventional Commits](https://www.conventionalcommits.org/).

## [Unreleased]

### Added

- Reintentos automáticos ante errores transitorios: `RetryPolicy` configurable vía `BCRAClient(retries=...)`, backoff exponencial, respeto del header `Retry-After` y retry de timeouts (sync y async)
- Inputs tipados: fechas (`fecha`, `fechadesde`, `fechahasta`) aceptan `datetime.date` además de `str` ISO, con validación y normalización a `YYYY-MM-DD`
- Validación de CUIT en `get_deudas`/`aget_deudas` (11 dígitos, guiones opcionales)
- Golden tests deterministas con cassettes: respuestas reales del BCRA grabadas en `tests/cassettes/`, regrabables con `uv run python scripts/record_cassettes.py`, que verifican que los modelos parseados espejen 1:1 la API
- Suite de integración en vivo (`tests/test_integration.py`, marker `integration`): deseleccionada por defecto, se corre con `uv run pytest -m integration --no-cov` y en un workflow manual de CI (`workflow_dispatch`); docs en `docs/testing.md`
- Docstrings públicos (style Google, en español) en cliente, recursos, `RetryPolicy`, excepciones y todos los modelos
- Sección **API Reference** en la documentación generada con `mkdocstrings`/`mkdocstrings-python` (cliente, recursos, modelos y errores)
- Gate de CHANGELOG: `scripts/check_changelog.py` valida el formato (Keep a Changelog + secciones) y que todo PR que toque `src/**` actualice `CHANGELOG.md` bajo `## [Unreleased]`; corre en pre-commit (hook `changelog`) y en un job de CI en PRs (`--pr-base`)
- Job de CI `docs` que compila el sitio con `mkdocs build --clean --strict` en cada PR/push, para detectar índices rotos y refs de mkdocstrings antes de publicar
- Job de CI `package` que construye wheel + sdist y corre `twine check` en cada PR/push, adelantando errores de empaquetado que antes solo se veían en el release
- **Release Drafter**: `.github/release-drafter.yml` + workflow que mantiene un draft de release categorizado por tipo de cambio (Conventional Commits) y autolabela los PRs desde el título

### Changed

- La versión del paquete (`__version__`) ahora se deriva de `importlib.metadata` en vez de estar hardcodeada
- `BCRAHTTPError` expone `response` y `reason`; se agregaron `BCRAConnectionError` y `BCRATimeoutError` (subclase de la anterior) para errores de red, todos bajo `BCRAError`
- Metadata de PyPI completa: `authors`, `license`, `keywords`, `classifiers` y `project.urls`
- CI: nuevo job `pre-commit`, `concurrency` para cancelar runs viejos, verificación estricta de que el tag coincida con la versión del paquete y `twine check` en el release
- Corregida la rama objetivo de los PRs en `AGENTS.md` y `docs/contribucion.md` (`develop` -> `main`), que era el único branch de trabajo real

## [0.0.7] - 2026-08-27

### Added

- Async endpoint methods (`aget_*`) across all resources, mirroring every sync method with the same signature and return model
- `Resource._fetch` shared dispatch so sync and async methods share endpoint resolution, HTTP call and model parsing
- Async unit tests for every endpoint (happy path and error propagation)

## [0.0.6] - 2026-08-27

### Added

- Markdown documentation under `docs/` (installation, quickstart, endpoints, versioning, errors, logging, contribution, changelog)
- MkDocs site with the Material theme, prepared to be published on ReadTheDocs
- `docs` dependency group in `pyproject.toml` (`mkdocs`, `mkdocs-material`)
- `.readthedocs.yaml` build configuration using `uv`

### Fixed

- ReadTheDocs build now publishes the MkDocs output to `$READTHEDOCS_OUTPUT/html`

## [0.0.5] - 2026-08-27

### Changed

- Replaced the metaclass/descriptor versioning system with explicit typed public methods, restoring correct IDE autocompletion and type checking on endpoint signatures
- `Resource` now exposes `versions(endpoint)` to inspect available versions and their deprecation status
- Version resolution (`version=` escape hatch) now validates against registered versions, emits `DeprecationWarning` for deprecated ones, and raises `BCRAEndpointVersionError` listing available versions
- Each resource registers its endpoint version specs (`_register_version`) with path and response model
- Rewrote `README.md` to reflect the actual architecture, usage, endpoints, versioning, and logging

### Added

- Unit tests for `Resource` versioning (`versions`, explicit/default resolution, unknown version, deprecation warning)

## [0.0.4] - 2026-08-27

### Added

- EstadisticasCambiarias resource with `get_divisas` endpoint (`GET /estadisticascambiarias/v1.0/Maestros/Divisas`)
- `Divisa` and `ResultGetDivisasV1` dataclasses for currency list serialization
- `get_cotizaciones` endpoint (`GET /estadisticascambiarias/v1.0/Cotizaciones`) with optional `fecha` query param
- `Cotizacion` and `ResultGetCotizacionesV1` dataclasses for exchange rates serialization
- `get_evolucion_moneda` endpoint (`GET /estadisticascambiarias/v1.0/Cotizaciones/{moneda}`) with optional `fechadesde`, `fechahasta`, `limit`, and `offset` query params
- `Resultset` and `ResultGetEvolucionMonedaV1` dataclasses for exchange rate evolution serialization
- Unit tests for `get_divisas` (happy path, empty, 500)
- Unit tests for `get_cotizaciones` (with/without fecha, empty, 400, 500)
- Unit tests for `get_evolucion_moneda` (basic, with params, empty, 400, 500)

## [0.0.3] - 2026-08-26

### Added

- Cheques resource with `get_entidades` endpoint (`GET /cheques/v1.0/entidades`)
- `EntidadBancaria` and `ResultGetEntidadesV1` dataclasses for entity list serialization
- `get_cheque_denunciado` endpoint (`GET /cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}`)
- `DetalleDenuncia` and `ResultGetChequeDenunciadoV1` dataclasses for reported check serialization
- Unit tests for `get_entidades` (happy path, empty, 500)
- Unit tests for `get_cheque_denunciado` (single detail, multiple details, not reported, 400, 404, 500)

## [0.0.2] - 2026-08-26

### Added

- Cheques rechazados endpoint (`get_cheques_rechazados`) under Deudores resource
- Dataclasses for cheques rechazados: `DetalleCheque`, `EntidadCheque`, `Causal`, `ResultGetChequesRechazadosV1`
- Logging configuration module (`_log.py`) with NullHandler for library best practices
- Integrated loggers across `client`, `transport`, and `deudores` modules
- Unit tests for cheques rechazados (happy path, empty, 400, 404, 500)

### Changed

- Renamed `Results` to `ResultGetDeudasV1` for endpoint-specific naming consistency

### Fixed

- Removed `logging.basicConfig()` call from deudores module (libraries should never configure root logger)
- Removed duplicate `Deudores` class that overwrote the Resource-based implementation
- Fixed trailing whitespace in `.gitignore`

## [0.0.1] - 2026-08-12

### Added

- Core `BCRAClient` with sync and async Transport support using httpx
- Versioned endpoint decorator system (`@endpoint`) and `Resource` base class with metaclass
- `Deudores` resource with `get_deudas_v1` implementation
- `Results`, `Periodo`, and `Entidad` dataclasses for response serialization
- `ResultGetDeudasHistoricasV1` with `get_deudas_historicas_v1` endpoint
- Exception hierarchy: `BCRAError`, `BCRAHTTPError`, `BCRAEndpointVersionError`
- Unit tests for `get_deudas` and `get_deudas_historicas` endpoints using httpx mocking
