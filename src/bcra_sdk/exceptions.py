import httpx


class BCRAError(Exception):
    """Error base del SDK."""


class BCRAHTTPError(BCRAError):
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
    """Error de red o conexión al proveer de servicios."""


class BCRATimeoutError(BCRAConnectionError):
    """La petición excedió el tiempo de espera configurado."""


class BCRAEndpointVersionError(BCRAError):
    """Se pidio una version de un endpoint que no existe"""
