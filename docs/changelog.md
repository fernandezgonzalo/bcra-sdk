# Changelog

Todas las novedades del proyecto se registran en
[`CHANGELOG.md`](https://github.com/fernandezgonzalo/bcra-sdk/blob/main/CHANGELOG.md)
(el formato sigue [Keep a Changelog](https://keepachangelog.com/) y los cambios
[Conventional Commits](https://www.conventionalcommits.org/)).

Última versión publicada: **0.0.9** (2026-08-29).

## [0.0.9] - 2026-08-29

### Added

- Recurso `RegimenDeTransparencia` (`client.regimen_de_transparencia`) con `get_cajas_ahorros`,
  `get_paquetes_productos`, `get_plazos_fijos`, `get_prestamos_prendarios`,
  `get_prestamos_hipotecarios`, `get_prestamos_personales` y `get_tarjetas_credito` (con sus
  pares `aget_*`) y filtro opcional `codigoEntidad`, incluyendo sus modelos.

### Fixed

- Orden de imports y `__all__` en `monetarias` y sus modelos para cumplir con ruff 0.16
  (isort case-insensitive y `__all__` sorteado), con el pre-commit alineado a la versión
  de ruff que corre en CI.
- Workflow de Release Drafter: permisos `contents: write` para crear/actualizar el draft,
  job `autolabel` limitado a eventos `pull_request` y migración del deprecado
  `categories[*].labels` al esquema `when: labels`.

## [0.0.8] - 2026-08-29

### Added

- Reintentos automáticos ante errores transitorios (`RetryPolicy`, backoff exponencial,
  respeto de `Retry-After`), configurables vía `BCRAClient(retries=...)`, sync y async.
- Inputs tipados: fechas (`fecha`, `fechadesde`, `fechahasta`, `desde`, `hasta`) aceptan
  `datetime.date` además de `str` ISO, con validación y normalización a `YYYY-MM-DD`.
- Validación de CUIT en `get_deudas`/`aget_deudas`.
- Golden tests deterministas con cassettes (respuestas reales del BCRA, regrabables con
  `scripts/record_cassettes.py`) y suite de integración en vivo (marker `integration`).
- Docstrings públicos (estilo Google, en español) y sección **API Reference** con mkdocstrings.
- Gates de CI: CHANGELOG (`scripts/check_changelog.py`), job `docs` con `mkdocs --strict`,
  job `package` (wheel + sdist + `twine check`) y Release Drafter.
- Recurso `Monetarias` (`client.monetarias`) con `get_monetarias`, `get_evolucion_variable`
  y `get_metodologias`/`get_metodologia` (con sus pares `aget_*`), incluyendo sus modelos.

### Changed

- `__version__` se deriva de `importlib.metadata` en vez de estar hardcodeada.
- `BCRAHTTPError` expone `response` y `reason`; se agregaron `BCRAConnectionError` y
  `BCRATimeoutError`, todas bajo `BCRAError`.
- Metadata de PyPI completa y CI con job `pre-commit`, `concurrency` y verificación de que
  el tag coincida con la versión del paquete.

## [0.0.7] - 2026-08-27

### Added

- Métodos asíncronos de endpoints (`aget_*`) en todos los resources, espejando cada
  método síncrono con la misma firma y modelo de retorno.
- Dispatch compartido en `Resource._fetch` para que las versiones sync y async
  compartan resolución de versión, llamada HTTP y parseo del modelo.
- Tests asíncronos para cada endpoint (caso feliz y propagación de errores).

## [0.0.6] - 2026-08-27

### Added

- Documentación en Markdown bajo `docs/` (instalación, guía rápida, endpoints, versionado, errores, logging, contribución, changelog).
- Sitio compilado con MkDocs y tema Material, publicado en ReadTheDocs.
- Grupo `docs` en `pyproject.toml` (`mkdocs`, `mkdocs-material`).
- Configuración de build de RTD (`.readthedocs.yaml`) usando `uv`.

### Fixed

- El build de ReadTheDocs ahora publica la salida de MkDocs en `$READTHEDOCS_OUTPUT/html`.

## [0.0.5] - 2026-08-27

### Changed

- Se reemplazó el sistema de versionado por metaclass/descriptors con métodos públicos
  tipados explícitos, restaurando el autocompletado y el type checking correctos en los
  endpoints.
- `Resource` ahora expone `versions(endpoint)` para inspeccionar versiones disponibles y
  su estado de deprecación.
- La resolución de versión (`version=` escape hatch) valida contra las versiones
  registradas, emite `DeprecationWarning` para las deprecadas y lanza
  `BCRAEndpointVersionError` listando las disponibles.
- Cada resource registra sus specs de versión (`_register_version`) con path y modelo de
  respuesta.

### Added

- Tests unitarios para el versioning de `Resource` (`versions`, resolución default/explicita,
  versión desconocida, warning de deprecación).

## [0.0.4] - 2026-08-27

### Added

- Resource `EstadisticasCambiarias` con endpoint `get_divisas`
  (`GET /estadisticascambiarias/v1.0/Maestros/Divisas`).
- Dataclasses `Divisa` y `ResultGetDivisasV1` para la serialización de divisas.
- Endpoint `get_cotizaciones` (`GET /estadisticascambiarias/v1.0/Cotizaciones`) con
  `fecha` opcional.
- Dataclasses `Cotizacion` y `ResultGetCotizacionesV1`.
- Endpoint `get_evolucion_moneda` (`GET /estadisticascambiarias/v1.0/Cotizaciones/{moneda}`)
  con `fechadesde`, `fechahasta`, `limit` y `offset` opcionales.
- Dataclasses `Resultset` y `ResultGetEvolucionMonedaV1`.
- Tests para `get_divisas`, `get_cotizaciones` y `get_evolucion_moneda`.

## [0.0.3] - 2026-08-26

### Added

- Resource `Cheques` con endpoint `get_entidades` (`GET /cheques/v1.0/entidades`).
- Dataclasses `EntidadBancaria` y `ResultGetEntidadesV1`.
- Endpoint `get_cheque_denunciado`
  (`GET /cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}`).
- Dataclasses `DetalleDenuncia` y `ResultGetChequeDenunciadoV1`.
- Tests para `get_entidades` y `get_cheque_denunciado`.

## [0.0.2] - 2026-08-26

### Added

- Endpoint `get_cheques_rechazados` en el resource Deudores.
- Dataclasses para cheques rechazados: `DetalleCheque`, `EntidadCheque`, `Causal`,
  `ResultGetChequesRechazadosV1`.
- Módulo de logging (`_log.py`) con `NullHandler`.
- Loggers integrados en `client`, `transport` y `deudores`.

### Changed

- Se renombró `Results` a `ResultGetDeudasV1`.

### Fixed

- Se eliminó `logging.basicConfig()` de deudores (las librerías no configuran el root logger).
- Se eliminó una clase `Deudores` duplicada que pisaba la implementación basada en `Resource`.
- Espacios al final de línea en `.gitignore`.

## [0.0.1] - 2026-08-12

### Added

- `BCRAClient` con Transport sync y async basado en `httpx`.
- Sistema de endpoints versionados (`@endpoint`) y `Resource` con metaclass.
- Resource `Deudores` con `get_deudas_v1`.
- Dataclasses `Results`, `Periodo` y `Entidad`.
- `ResultGetDeudasHistoricasV1` con `get_deudas_historicas_v1`.
- Jerarquía de excepciones: `BCRAError`, `BCRAHTTPError`, `BCRAEndpointVersionError`.
- Tests para `get_deudas` y `get_deudas_historicas`.
