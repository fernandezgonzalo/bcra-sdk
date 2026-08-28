# Errores

Todas las excepciones del SDK heredan de `BCRAError`, de modo que un solo
`except BCRAError` cubre errores de red, timeout y HTTP. Más detalle en
[Errores](../errores.md).

::: bcra_sdk.exceptions.BCRAError
::: bcra_sdk.exceptions.BCRAHTTPError
::: bcra_sdk.exceptions.BCRAConnectionError
::: bcra_sdk.exceptions.BCRATimeoutError
::: bcra_sdk.exceptions.BCRAEndpointVersionError
