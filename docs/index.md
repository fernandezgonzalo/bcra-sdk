# BCRA-SDK

SDK no oficial para las APIs públicas del Banco Central de la República Argentina (BCRA).

`bcra-sdk` ofrece un único cliente (`BCRAClient`) que organiza los endpoints por dominio
(`deudores`, `cheques`, `estadisticas_cambiarias`, `monetarias`) y estructura cada
respuesta en dataclasses fuertemente tipadas.

## Características

- **Un solo cliente**: toda la API detrás de `BCRAClient`, con `base_url` y timeout configurables.
- **Respuestas tipadas**: cada endpoint devuelve una dataclass, sin manejar diccionarios crudos.
- **Endpoints versionados**: cada endpoint resuelve su versión más reciente por defecto,
  permite forzar una versión y emite `DeprecationWarning` en versiones deprecadas.
- **Errores explícitos**: jerarquía de excepciones propia (`BCRAError`, `BCRAHTTPError`,
  `BCRAEndpointVersionError`).
- **Una única dependencia en runtime**: `httpx`.

## Contenido

- [Instalación](instalacion.md)
- [Guía rápida](guia-rapida.md)
- Endpoints
    - [Deudores](endpoints/deudores.md)
    - [Cheques](endpoints/cheques.md)
    - [Estadísticas cambiarias](endpoints/estadisticas-cambiarias.md)
    - [Monetarias](endpoints/monetarias.md)
- API Reference
    - [Cliente y configuración](api/cliente.md)
    - [Recursos](api/recursos.md)
    - [Modelos](api/modelos.md)
    - [Errores](api/errores.md)
- [Versionado de endpoints](versionado.md)
- [Errores](errores.md)
- [Logging](logging.md)
- [Contribución](contribucion.md)
- [Changelog](changelog.md)

## Licencia

MIT
