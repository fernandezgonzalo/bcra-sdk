from dataclasses import dataclass


@dataclass
class Entidad:
    """Situación de un deudor en una entidad financiera para un período."""

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
    """Un período mensual de la situación de deudas con sus entidades."""

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
    """Respuesta de ``get_deudas``: situación de deudas por CUIT."""

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
    """Situación histórica de un deudor en una entidad para un período."""

    entidad: str
    situacion: int
    monto: float
    enRevision: bool
    procesoJud: bool


@dataclass
class PeriodoHistorica:
    """Un período del histórico de deudas con sus entidades."""

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
    """Respuesta de ``get_deudas_historicas``: histórico de deudas."""

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
