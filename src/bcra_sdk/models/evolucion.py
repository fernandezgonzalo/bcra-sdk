from dataclasses import dataclass

from .cotizaciones import ResultGetCotizacionesV1


@dataclass
class Resultset:
    count: int
    offset: int
    limit: int


@dataclass
class ResultGetEvolucionMonedaV1:
    resultset: Resultset
    cotizaciones: list[ResultGetCotizacionesV1]
