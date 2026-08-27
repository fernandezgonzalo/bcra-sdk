from dataclasses import dataclass


@dataclass
class Cotizacion:
    codigoMoneda: str
    descripcion: str
    tipoPase: float
    tipoCotizacion: float


@dataclass
class ResultGetCotizacionesV1:
    fecha: str | None
    detalle: list[Cotizacion]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetCotizacionesV1":
        return cls(
            fecha=data["fecha"],
            detalle=[Cotizacion(**d) for d in data.get("detalle", [])],
        )
