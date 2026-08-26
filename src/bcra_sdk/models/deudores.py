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
class ResultGetDeudasV1:
    identificacion: int
    denominacion: str
    periodos: list[Periodo]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetDeudasV1":
        return cls(
            identificacion=data["identificacion"],
            denominacion=data["denominacion"],
            periodos=[Periodo.from_dict(p) for p in data.get("periodos", [])],
        )


@dataclass
class EntidadHistorica:
    entidad: str
    situacion: int
    monto: float
    enRevision: bool
    procesoJud: bool


@dataclass
class PeriodoHistorica:
    periodo: str
    entidades: list[EntidadHistorica]

    @classmethod
    def from_dict(cls, data: dict) -> "PeriodoHistorica":
        return cls(
            periodo=data["periodo"],
            entidades=[EntidadHistorica(**e) for e in data.get("entidades", [])],
        )


@dataclass
class ResultGetDeudasHistoricasV1:
    identificacion: str
    denominacion: str
    periodos: list[PeriodoHistorica]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetDeudasHistoricasV1":
        return cls(
            identificacion=data["identificacion"],
            denominacion=data["denominacion"],
            periodos=[PeriodoHistorica.from_dict(p) for p in data.get("periodos", [])],
        )
