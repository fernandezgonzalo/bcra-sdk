from dataclasses import dataclass


@dataclass
class DetalleDenuncia:
    """Detalle de una denuncia de cheque sin pagar."""

    sucursal: int
    numeroCuenta: int
    causal: str


@dataclass
class ResultGetChequeDenunciadoV1:
    """Respuesta de ``get_cheque_denunciado``.

    Incluye si el cheque figura como denunciado y el detalle de las
    denuncias asociadas (puede estar vacío).
    """

    numeroCheque: int
    denunciado: bool
    fechaProcesamiento: str
    denominacionEntidad: str
    detalles: list[DetalleDenuncia]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetChequeDenunciadoV1":
        return cls(
            numeroCheque=data["numeroCheque"],
            denunciado=data["denunciado"],
            fechaProcesamiento=data["fechaProcesamiento"],
            denominacionEntidad=data["denominacionEntidad"],
            detalles=[DetalleDenuncia(**d) for d in data.get("detalles", [])],
        )
