# Changelog

Todas las novedades del proyecto se registran en
[`CHANGELOG.md`](https://github.com/fernandezgonzalo/bcra-sdk/blob/main/CHANGELOG.md)
(el formato sigue [Keep a Changelog](https://keepachangelog.com/) y los cambios
[Conventional Commits](https://www.conventionalcommits.org/)).

Última versión publicada: **0.0.5** (2026-08-27).

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
