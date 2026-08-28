import httpx


class BCRAError(Exception):
    """Error base del SDK. Todas las excepciones heredan de esta clase."""


class BCRAHTTPError(BCRAError):
    """La API respondió con un estado HTTP de error (4xx o 5xx).

    Args:
        status_code: Código de estado HTTP de la respuesta.
        message: Mensaje de error (el cuerpo de la respuesta).
        response: La respuesta HTTP original, si está disponible.
    """

    def __init__(
        self,
        status_code: int,
        message: str,
        response: httpx.Response | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.response = response
        self.reason = response.reason_phrase if response is not None else None
        super().__init__(f"[{self.status_code} {self.message}]")


class BCRAConnectionError(BCRAError):
    """Error de red o de conexión al contactar el servicio."""


class BCRATimeoutError(BCRAConnectionError):
    """La petición excedió el tiempo de espera configurado."""


class BCRAEndpointVersionError(BCRAError):
    """Se solicitó una versión de endpoint que no existe."""
