from dataclasses import dataclass

from .evolucion import Resultset


@dataclass
class Metodologia:
    """Metodología de una variable monetaria.

    ``detalle`` describe cómo está compuesta la variable.
    """

    id: int
    detalle: str


@dataclass
class ResultGetMetodologiasV1:
    """Respuesta de ``get_metodologias``: metodologías con su paginado.

    ``resultset`` describe el total disponible (`count`) y la ventana
    devuelta (`offset`/`limit`), y ``metodologias`` contiene las
    metodologías de las variables.
    """

    resultset: Resultset
    metodologias: list[Metodologia]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetMetodologiasV1":
        return cls(
            resultset=Resultset(**data["metadata"]["resultset"]),
            metodologias=[Metodologia(**m) for m in data["results"]],
        )


@dataclass
class ResultGetMetodologiaV1:
    """Respuesta de ``get_metodologia``: metodología de una variable.

    A diferencia del listado, este endpoint no devuelve `Resultset`.
    """

    metodologia: Metodologia

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetMetodologiaV1":
        return cls(metodologia=Metodologia(**data["results"][0]))


@dataclass
class VariableMonetaria:
    """Variable monetaria del listado principal de `get_monetarias`."""

    idVariable: int
    descripcion: str
    categoria: str
    tipoSerie: str
    periodicidad: str
    unidadExpresion: str
    moneda: str
    primerFechaInformada: str
    ultFechaInformada: str
    ultValorInformado: float


@dataclass
class PuntoSerie:
    """Punto de una serie monetaria: fecha y valor de la variable."""

    fecha: str
    valor: float


@dataclass
class SerieMonetaria:
    """Serie histórica de una variable monetaria.

    ``detalle`` contiene los puntos de la serie (fecha y valor) ordenados de
    más reciente a más antiguo.
    """

    idVariable: int
    detalle: list[PuntoSerie]


@dataclass
class ResultGetEvolucionVariableV1:
    """Respuesta de ``get_evolucion_variable``.

    `resultset` describe el total disponible (`count`) y la ventana devuelta
    (`offset`/`limit`), y ``series`` contiene la serie de la variable pedida.
    """

    resultset: Resultset
    series: list[SerieMonetaria]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetEvolucionVariableV1":
        return cls(
            resultset=Resultset(**data["metadata"]["resultset"]),
            series=[
                SerieMonetaria(
                    idVariable=s["idVariable"],
                    detalle=[PuntoSerie(**p) for p in s["detalle"]],
                )
                for s in data["results"]
            ],
        )


@dataclass
class ResultGetMonetariasV1:
    """Respuesta de ``get_monetarias``: variables monetarias con su paginado.

    ``resultset`` describe el total disponible (`count`) y la ventana
    devuelta (`offset`/`limit`), y ``variables`` contiene el detalle de cada
    variable del maestro.
    """

    resultset: Resultset
    variables: list[VariableMonetaria]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetMonetariasV1":
        return cls(
            resultset=Resultset(**data["metadata"]["resultset"]),
            variables=[VariableMonetaria(**v) for v in data["results"]],
        )
