from dataclasses import dataclass


@dataclass
class DetalleCheque:
    nroCheque: int
    fechaRechazo: str
    monto: float
    fechaPago: str | None
    fechaPagoMulta: str | None
    estadoMulta: str | None
    ctaPersonal: bool
    denomJuridica: str | None
    enRevision: bool
    procesoJud: bool


@dataclass
class EntidadCheque:
    entidad: int
    detalle: list[DetalleCheque]

    @classmethod
    def from_dict(cls, data: dict) -> "EntidadCheque":
        return cls(
            entidad=data["entidad"],
            detalle=[DetalleCheque(**d) for d in data.get("detalle", [])],
        )


@dataclass
class Causal:
    causal: str
    entidades: list[EntidadCheque]

    @classmethod
    def from_dict(cls, data: dict) -> "Causal":
        return cls(
            causal=data["causal"],
            entidades=[EntidadCheque.from_dict(e) for e in data.get("entidades", [])],
        )


@dataclass
class ResultGetChequesRechazadosV1:
    identificacion: int
    causales: list[Causal]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetChequesRechazadosV1":
        return cls(
            identificacion=data["identificacion"],
            causales=[Causal.from_dict(c) for c in data.get("causales", [])],
        )
