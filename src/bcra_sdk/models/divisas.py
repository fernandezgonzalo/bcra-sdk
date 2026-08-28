from dataclasses import dataclass


@dataclass
class Divisa:
    """Una divisa del maestro de monedas del BCRA."""

    codigo: str
    denominacion: str


@dataclass
class ResultGetDivisasV1:
    """Respuesta de ``get_divisas``: listado de `Divisa`."""

    divisas: list[Divisa]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetDivisasV1":
        return cls(divisas=[Divisa(**d) for d in data])
