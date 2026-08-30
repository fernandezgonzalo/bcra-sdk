from dataclasses import dataclass


@dataclass
class CajaAhorro:
    """Producto de cajas de ahorro de una entidad del Régimen de Transparencia."""

    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    procesoSimplificadoDebidaDiligencia: str


@dataclass
class ResultGetCajasAhorrosV1:
    """Respuesta de ``get_cajas_ahorros``: listado de `CajaAhorro`."""

    cajas_ahorros: list[CajaAhorro]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetCajasAhorrosV1":
        return cls(cajas_ahorros=[CajaAhorro(**d) for d in data])
