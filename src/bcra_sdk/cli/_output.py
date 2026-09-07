from __future__ import annotations

import dataclasses
import json
from typing import Any

from rich.console import Console
from rich.table import Table


def to_json(result: Any) -> str:
    """Serializa un modelo result del SDK como JSON."""
    return json.dumps(
        dataclasses.asdict(result), indent=2, ensure_ascii=False, default=str
    )


def _cell(value: Any) -> str:
    if isinstance(value, bool):
        return "si" if value else "no"
    if value is None:
        return ""
    return str(value)


def emit_table(rows: list[dict[str, Any]], columns: list[str]) -> None:
    """Imprime las filas como una tabla en la salida estándar."""
    table = Table(show_header=True, header_style="bold")
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*(_cell(row.get(column)) for column in columns))
    Console().print(table)
