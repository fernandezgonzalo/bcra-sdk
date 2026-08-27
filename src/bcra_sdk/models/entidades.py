from dataclasses import dataclass


@dataclass
class EntidadBancaria:
    codigoEntidad: int
    denominacion: str


@dataclass
class ResultGetEntidadesV1:
    entidades: list[EntidadBancaria]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetEntidadesV1":
        return cls(entidades=[EntidadBancaria(**e) for e in data])
