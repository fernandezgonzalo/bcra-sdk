"""Dev tool: graba respuestas reales de la API del BCRA como cassettes.

Uso:
    uv run python scripts/record_cassettes.py

Escribe en ``tests/cassettes/<endpoint>.json`` y falla si algún estado HTTP
no coincide con el esperado.
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass

import httpx

BASE_URL = "https://api.bcra.gob.ar"
OUTPUT_DIR = pathlib.Path("tests/cassettes")


@dataclass(frozen=True)
class RequestSpec:
    path: str
    out: str
    expected_status: int = 200
    params: dict[str, str | int] | None = None


REQUESTS: list[RequestSpec] = [
    RequestSpec(
        path="/estadisticas/v4.0/monetarias",
        out="monetarias.get_monetarias",
    ),
    RequestSpec(
        path="/estadisticas/v4.0/monetarias/1",
        out="monetarias.get_evolucion_variable",
        params={"desde": "2025-05-20", "hasta": "2025-05-26", "limit": 10},
    ),
    RequestSpec(
        path="/estadisticascambiarias/v1.0/Maestros/Divisas",
        out="estadisticascambiarias.get_divisas",
    ),
    RequestSpec(
        path="/estadisticascambiarias/v1.0/Cotizaciones",
        out="estadisticascambiarias.get_cotizaciones",
        params={"fecha": "2024-06-12"},
    ),
    RequestSpec(
        path="/estadisticascambiarias/v1.0/Cotizaciones/EUR",
        out="estadisticascambiarias.get_evolucion_moneda",
        params={"fechadesde": "2024-06-10", "fechahasta": "2024-06-12", "limit": 10},
    ),
    RequestSpec(
        path="/cheques/v1.0/entidades",
        out="cheques.get_entidades",
    ),
    RequestSpec(
        path="/centraldedeudores/v1.0/Deudas/20111111112",
        out="deudores.get_deudas",
        expected_status=404,
    ),
]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        for spec in REQUESTS:
            resp = client.get(spec.path, params=spec.params)
            if resp.status_code != spec.expected_status:
                raise SystemExit(
                    f"{spec.path}: status {resp.status_code} != {spec.expected_status}"
                )
            payload = {
                "path": spec.path,
                "params": spec.params,
                "status_code": resp.status_code,
                "json": resp.json(),
            }
            target = OUTPUT_DIR / f"{spec.out}.json"
            target.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"OK {resp.status_code}  {spec.path} -> {target.name}")


if __name__ == "__main__":
    main()
