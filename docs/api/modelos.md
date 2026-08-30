# Modelos

Todos los modelos son dataclasses planas; deserializan la respuesta con su
classmethod `from_dict` y sus campos replican 1:1 los nombres del JSON de la API.

## Deudores

::: bcra_sdk.models.deudores.Entidad
::: bcra_sdk.models.deudores.Periodo
::: bcra_sdk.models.deudores.ResultGetDeudasV1
::: bcra_sdk.models.deudores.EntidadHistorica
::: bcra_sdk.models.deudores.PeriodoHistorica
::: bcra_sdk.models.deudores.ResultGetDeudasHistoricasV1

## Cheques rechazados

::: bcra_sdk.models.cheques.DetalleCheque
::: bcra_sdk.models.cheques.EntidadCheque
::: bcra_sdk.models.cheques.Causal
::: bcra_sdk.models.cheques.ResultGetChequesRechazadosV1

## Cheque denunciado

::: bcra_sdk.models.denunciados.DetalleDenuncia
::: bcra_sdk.models.denunciados.ResultGetChequeDenunciadoV1

## Entidades bancarias

::: bcra_sdk.models.entidades.EntidadBancaria
::: bcra_sdk.models.entidades.ResultGetEntidadesV1

## Divisas

::: bcra_sdk.models.divisas.Divisa
::: bcra_sdk.models.divisas.ResultGetDivisasV1

## Cotizaciones

::: bcra_sdk.models.cotizaciones.Cotizacion
::: bcra_sdk.models.cotizaciones.ResultGetCotizacionesV1

## Evolución de moneda

::: bcra_sdk.models.evolucion.Resultset
::: bcra_sdk.models.evolucion.ResultGetEvolucionMonedaV1

## Variables monetarias

::: bcra_sdk.models.monetarias.VariableMonetaria
::: bcra_sdk.models.monetarias.PuntoSerie
::: bcra_sdk.models.monetarias.SerieMonetaria
::: bcra_sdk.models.monetarias.Metodologia
::: bcra_sdk.models.monetarias.ResultGetMonetariasV1
::: bcra_sdk.models.monetarias.ResultGetEvolucionVariableV1
::: bcra_sdk.models.monetarias.ResultGetMetodologiasV1
::: bcra_sdk.models.monetarias.ResultGetMetodologiaV1

## Régimen de Transparencia

::: bcra_sdk.models.transparencia.CajaAhorro
::: bcra_sdk.models.transparencia.ResultGetCajasAhorrosV1
::: bcra_sdk.models.transparencia.PaqueteProducto
::: bcra_sdk.models.transparencia.ResultGetPaquetesProductosV1
