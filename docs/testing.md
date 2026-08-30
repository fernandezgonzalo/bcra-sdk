# Testing: cassettes y suite de integración

La suite de tests tiene dos niveles:

- **Tests deterministas** (default): mockean la red con respuestas reales del BCRA
  grabadas como *cassettes*. No requieren conexión y corren en cada `uv run pytest`,
  tox y pre-commit.
- **Suite de integración** (marcada `@pytest.mark.integration`): pega contra la API en
  vivo. Requiere red y se **excluye del default** (`-m "not integration"` en `addopts`).

## Cassettes

Las respuestas reales se guardan en `tests/cassettes/<endpoint>.json` con el formato:

```json
{
  "path": "/estadisticascambiarias/v1.0/Cotizaciones",
  "params": { "fecha": "2024-06-12" },
  "status_code": 200,
  "json": { ... }
}
```

Solo se graban endpoints deterministas (históricos a fecha fija o maestros estables).
No entran aquellos cuya respuesta cambia día a día — p. ej. `get_cheque_denunciado`
incluye `fechaProcesamiento` —, que se cubren solo en la suite de integración.

Los tests golden (`tests/test_golden.py`) deserializan el cassette con el SDK y
comprueban que el modelo parseado espeje 1:1 la respuesta real
(`dataclasses.asdict(result)`), incluido el camino de error (404 de deudores con el
mensaje real del BCRA).

### Regrabar los cassettes

Si el BCRA cambia un contrato (agrega/quita campos) los tests golden fallarán. Para
actualizar con la respuesta actual:

```bash
uv run python scripts/record_cassettes.py
```

El script hace la petición en vivo, escribe los JSON y falla si algún estado HTTP cambió
respecto del esperado. Revisá el diff de los cassettes antes de commitear.

## Suite de integración

Smoke tests en vivo contra `https://api.bcra.gob.ar` (`tests/test_integration.py`):
divisas, cotizaciones a fecha fija, evolución de moneda, entidades, cajas de ahorro,
el 404 de deudores con un CUIT sin datos y un cheque no denunciado.

```bash
uv run pytest -m integration --no-cov
```

`--no-cov` desactiva la medición de cobertura, cuyo mínimo del 100% solo aplica a la
suite determinista (al correr `-m integration` las pruebas unitarias quedan deseleccionadas).

En CI se corre manualmente desde GitHub (`.github/workflows/integration.yml`, trigger
`workflow_dispatch`); nunca se ejecuta en el flujo normal de PRs ni en pre-commit.
