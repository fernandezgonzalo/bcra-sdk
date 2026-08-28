from dataclasses import dataclass


@dataclass
class EntidadBancaria:
    """Una entidad bancaria del sistema de cheques."""

    codigoEntidad: int
    denominacion: str


@dataclass
class ResultGetEntidadesV1:
    """Respuesta de ``get_entidades``: listado de `EntidadBancaria`."""

    entidades: list[EntidadBancaria]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetEntidadesV1":
        return cls(entidades=[EntidadBancaria(**e) for e in data])
