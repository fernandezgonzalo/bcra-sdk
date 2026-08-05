from dataclasses import dataclass


@dataclass
class Entidad:
    entidad: str
    situacion: str
    fechaSit1: str
    monto: float
    diasAtrasoPago: int
    refinanciaciones: bool
    recategorizacionOblig: bool
    situacionJuridica: bool
    irrecDisposicionTecnica: bool
    enRevision: bool
    procesoJud: bool


@dataclass
class Periodo:
    periodo: str
    entidades: list[Entidad]

    @classmethod
    def from_dict(cls, data: dict) -> "Periodo":
        return cls(
            periodo=data["periodo"],
            entidades=[Entidad(**e) for e in data.get("entidades", [])],
        )


@dataclass
class Results:
    identificacion: int
    denominacion: str
    periodos: list[Periodo]

    @classmethod
    def from_dict(cls, data: dict) -> "Results":
        return cls(
            identificacion=data["identificacion"],
            denominacion=data["denominacion"],
            periodos=[Periodo.from_dict(p) for p in data.get("periodos", [])],
        )
