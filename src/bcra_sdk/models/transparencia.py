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


@dataclass
class PlazoFijo:
    """Plazo fijo comercializado por una entidad del Régimen de Transparencia."""

    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    nombreCompleto: str
    nombreCorto: str
    denominacion: str | None
    montoMinimoInvertir: float
    plazoMinimoInvertirDias: int
    canalConstitucion: str
    tasaEfectivaAnualMinima: float
    territorioValidez: str
    masInformacion: str | None


@dataclass
class ResultGetPlazosFijosV1:
    """Respuesta de ``get_plazos_fijos``: listado de `PlazoFijo`."""

    plazos_fijos: list[PlazoFijo]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetPlazosFijosV1":
        return cls(plazos_fijos=[PlazoFijo(**d) for d in data])


@dataclass
class PrestamoPrendario:
    """Préstamo prendario de una entidad del Régimen de Transparencia."""

    relacionMontoTasacion: int
    destinoFondos: str
    montoMinimoOtorgable: float
    denominacion: str
    montoMaximoOtorgable: float
    plazoMaximoOtorgable: int
    ingresoMinimoMensual: float
    antiguedadLaboralMinimaMeses: int
    edadMaximaSolicitada: int
    relacionCuotaIngreso: int
    beneficiario: str
    cargoMaximoCancelacionAnticipada: int
    tasaEfectivaAnualMaxima: float
    tipoTasa: str
    costoFinancieroEfectivoTotalMaximo: float
    cuotaInicial: float
    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    nombreCompleto: str
    nombreCorto: str
    territorioValidez: str
    masInformacion: str | None


@dataclass
class ResultGetPrestamosPrendariosV1:
    """Respuesta de ``get_prestamos_prendarios``: listado de `PrestamoPrendario`."""

    prestamos_prendarios: list[PrestamoPrendario]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetPrestamosPrendariosV1":
        return cls(prestamos_prendarios=[PrestamoPrendario(**d) for d in data])


@dataclass
class PrestamoHipotecario:
    """Préstamo hipotecario de una entidad del Régimen de Transparencia."""

    relacionMontoTasacion: int
    destinoFondos: str
    denominacion: str
    montoMaximoOtorgable: float
    plazoMaximoOtorgable: int
    ingresoMinimoMensual: float
    antiguedadLaboralMinimaMeses: int
    edadMaximaSolicitada: int
    relacionCuotaIngreso: int
    beneficiario: str
    cargoMaximoCancelacionAnticipada: int
    tasaEfectivaAnualMaxima: float
    tipoTasa: str
    costoFinancieroEfectivoTotalMaximo: float
    cuotaInicial: float
    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    nombreCompleto: str
    nombreCorto: str
    territorioValidez: str
    masInformacion: str | None


@dataclass
class ResultGetPrestamosHipotecariosV1:
    """Respuesta de ``get_prestamos_hipotecarios``: listado de `PrestamoHipotecario`."""

    prestamos_hipotecarios: list[PrestamoHipotecario]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetPrestamosHipotecariosV1":
        return cls(prestamos_hipotecarios=[PrestamoHipotecario(**d) for d in data])


@dataclass
class PrestamoPersonal:
    """Préstamo personal de una entidad del Régimen de Transparencia."""

    montoMinimoOtorgable: float
    denominacion: str
    montoMaximoOtorgable: float
    plazoMaximoOtorgable: int
    ingresoMinimoMensual: float
    antiguedadLaboralMinimaMeses: int
    edadMaximaSolicitada: int
    relacionCuotaIngreso: int
    beneficiario: str
    cargoMaximoCancelacionAnticipada: int
    tasaEfectivaAnualMaxima: float
    tipoTasa: str
    costoFinancieroEfectivoTotalMaximo: float
    cuotaInicial: float
    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    nombreCompleto: str
    nombreCorto: str
    territorioValidez: str
    masInformacion: str | None


@dataclass
class ResultGetPrestamosPersonalesV1:
    """Respuesta de ``get_prestamos_personales``: listado de `PrestamoPersonal`."""

    prestamos_personales: list[PrestamoPersonal]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetPrestamosPersonalesV1":
        return cls(prestamos_personales=[PrestamoPersonal(**d) for d in data])


@dataclass
class TarjetaCredito:
    """Tarjeta de crédito ofrecida por una entidad del Régimen de Transparencia."""

    comisionMaximaAdministracionMantenimiento: float
    comisionMaximaRenovacion: float
    tasaEfectivaAnualMaximaFinanciacion: float
    tasaEfectivaAnualMaximaAdelantoEfectivo: float
    ingresoMinimoMensual: float
    antiguedadLaboralMinimaMeses: int
    edadMaximaSolicitada: int
    segmento: str
    codigoEntidad: int
    descripcionEntidad: str
    fechaInformacion: str
    nombreCompleto: str
    nombreCorto: str
    territorioValidez: str
    masInformacion: str | None


@dataclass
class ResultGetTarjetasCreditoV1:
    """Respuesta de ``get_tarjetas_credito``: listado de `TarjetaCredito`."""

    tarjetas_credito: list[TarjetaCredito]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetTarjetasCreditoV1":
        return cls(tarjetas_credito=[TarjetaCredito(**d) for d in data])
