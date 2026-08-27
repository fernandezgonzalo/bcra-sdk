# Cheques (`bcra.cheques`)

Endpoints de cheques denunciados del BCRA.

| Método | Endpoint |
|--------|----------|
| `get_entidades()` | `GET /cheques/v1.0/entidades` |
| `get_cheque_denunciado(codigo_entidad, numero_cheque)` | `GET /cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}` |

## `get_entidades()`

Devuelve el listado de entidades bancarias.

Sin parámetros. Devuelve `ResultGetEntidadesV1`:

- `entidades: list[EntidadBancaria]`
    - `EntidadBancaria.codigoEntidad: int`
    - `EntidadBancaria.denominacion: str`

```python
with BCRAClient() as bcra:
    entidades = bcra.cheques.get_entidades()
    for entidad in entidades.entidades:
        print(entidad.codigoEntidad, entidad.denominacion)
```

## `get_cheque_denunciado(codigo_entidad, numero_cheque)`

Devuelve el detalle de un cheque denunciado.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `codigo_entidad` | `int` | Código de la entidad bancaria (obligatorio) |
| `numero_cheque` | `int` | Número del cheque (obligatorio) |

Devuelve `ResultGetChequeDenunciadoV1`:

- `numeroCheque: int`
- `denunciado: bool`
- `fechaProcesamiento: str`
- `denominacionEntidad: str`
- `detalles: list[DetalleDenuncia]`
    - `DetalleDenuncia.sucursal: int`
    - `DetalleDenuncia.numeroCuenta: int`
    - `DetalleDenuncia.causal: str`

```python
with BCRAClient() as bcra:
    cheque = bcra.cheques.get_cheque_denunciado(
        codigo_entidad=11, numero_cheque=12345678
    )
    print(cheque.denunciado, cheque.denominacionEntidad)
```

Todos los métodos aceptan además el escape hatch `version=` para forzar una versión
específica (ver [Versionado de endpoints](../versionado.md)).
