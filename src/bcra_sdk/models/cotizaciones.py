from dataclasses import dataclass


@dataclass
class Cotizacion:
    """Cotización de una moneda para una fecha determinada."""

    codigoMoneda: str
    descripcion: str
    tipoPase: float
    tipoCotizacion: float


@dataclass
class ResultGetCotizacionesV1:
    """Respuesta de ``get_cotizaciones``: cotizaciones del día por moneda.

    ``fecha`` puede ser ``None`` cuando la API devuelve la cotización más
    reciente sin fecha asociada en el nivel raíz.
    """

    fecha: str | None
    detalle: list[Cotizacion]

    @classmethod
    def from_dict(cls, data: dict) -> "ResultGetCotizacionesV1":
        return cls(
            fecha=data["fecha"],
            detalle=[Cotizacion(**d) for d in data.get("detalle", [])],
        )
