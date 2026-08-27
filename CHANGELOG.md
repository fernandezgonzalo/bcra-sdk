# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Conventional Commits](https://www.conventionalcommits.org/).

## [0.0.4] - 2026-08-27

### Added

- EstadisticasCambiarias resource with `get_divisas` endpoint (`GET /estadisticascambiarias/v1.0/Maestros/Divisas`)
- `Divisa` and `ResultGetDivisasV1` dataclasses for currency list serialization
- `get_cotizaciones` endpoint (`GET /estadisticascambiarias/v1.0/Cotizaciones`) with optional `fecha` query param
- `Cotizacion` and `ResultGetCotizacionesV1` dataclasses for exchange rates serialization
- Unit tests for `get_divisas` (happy path, empty, 500)
- Unit tests for `get_cotizaciones` (with/without fecha, empty, 400, 500)

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
