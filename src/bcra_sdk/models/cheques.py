from dataclasses import dataclass


@dataclass
class DetalleCheque:
    """Detalle de un rechazo de cheque para una entidad."""

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
    """Entidad en la que un cheque resultó rechazado junto a sus detalles."""

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
    """Un causal de rechazo con las entidades involucradas."""

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
    """Respuesta de ``get_cheques_rechazados`` de la Central de Deudores."""

    identificacion: int
    causales: list[Causal]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetChequesRechazadosV1":
        return cls(
            identificacion=data["identificacion"],
            causales=[Causal.from_dict(c) for c in data.get("causales", [])],
        )
