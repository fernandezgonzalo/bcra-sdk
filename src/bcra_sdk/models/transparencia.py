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


@dataclass
class PaqueteProducto:
    """Paquete de productos de una entidad del Régimen de Transparencia."""

    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    nombreCompleto: str
    nombreCorto: str
    comisionMaximaMantenimiento: float
    ingresoMinimoMensual: float
    antiguedadLaboralMinimaMeses: int
    edadMaximaSolicitada: int
    beneficiarios: str
    segmento: str
    productosIntegrantes: str
    territorioValidez: str
    masInformacion: str | None


@dataclass
class ResultGetPaquetesProductosV1:
    """Respuesta de ``get_paquetes_productos``: listado de `PaqueteProducto`."""

    paquetes_productos: list[PaqueteProducto]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetPaquetesProductosV1":
        return cls(paquetes_productos=[PaqueteProducto(**d) for d in data])
