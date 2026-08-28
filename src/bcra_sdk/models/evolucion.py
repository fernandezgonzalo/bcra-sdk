from dataclasses import dataclass

from .cotizaciones import ResultGetCotizacionesV1


@dataclass
class Resultset:
    """Metadatos de paginado de la evolución de una moneda."""

    count: int
    offset: int
    limit: int


@dataclass
class ResultGetEvolucionMonedaV1:
    """Respuesta de ``get_evolucion_moneda``.

    Agrupa el `Resultset` con la serie de cotizaciones diarias.
    """

    resultset: Resultset
    cotizaciones: list[ResultGetCotizacionesV1]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetEvolucionMonedaV1":
        return cls(
            resultset=Resultset(**data["metadata"]["resultset"]),
            cotizaciones=[
                ResultGetCotizacionesV1.from_dict(c) for c in data["results"]
            ],
        )
