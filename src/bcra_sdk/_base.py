from __future__ import annotations

import inspect
import warnings
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Protocol

import httpx

from .exceptions import BCRAEndpointVersionError


class Model(Protocol):
    """Protocolo para los modelos de respuesta: una clase con ``from_dict``."""

    @classmethod
    def from_dict(cls, data): ...


@dataclass
class VersionSpec:
    """Especificacion de una version de un endpoint."""

    path: str
    model: type[Model]
    deprecated: bool = False


def _parse_version(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in version.split("."))


def _extract(
    model: type[Model], resp: httpx.Response, results_key: str | None
) -> Model:
    data = resp.json()[results_key] if results_key else resp.json()
    return model.from_dict(data)


async def _extract_async(
    call: Awaitable[httpx.Response], model: type[Model], results_key: str | None
) -> Model:
    resp = await call
    return _extract(model, resp, results_key)


class Resource:
    """Base class para resources con soporte de endpoints versionados.

    Cada endpoint publico se declara como un metodo de la clase con su firma
    tipada real (autocompletado/validacion en el IDE), y su versionado se
    registra via ``_register_version``. ``_resolve_version`` se encarga de
    seleccionar la version (por defecto la mas reciente), validar la version
    pedida y emitir deprecation warnings.

    Ejemplo de uso dentro de un recurso::

        class EstadisticasCambiarias(Resource):
            def __init__(self, transport):
                super().__init__(transport)
                self._register_version(
                    "get_cotizaciones", "1.0",
                    path="/Cotizaciones",
                    model=ResultGetCotizacionesV1,
                )

            def get_cotizaciones(self, *, version=None):
                spec = self._resolve_version("get_cotizaciones", version)
                r = self._t.request("GET", spec.path)
                return spec.model.from_dict(r.json()["results"])
    """

    def __init__(self, transport):
        self._t = transport
        self._version_specs: dict[str, dict[str, VersionSpec]] = {}
        # {"get_cotizaciones": {"1.0": VersionSpec("/Cotizaciones", Model)}}

    def _fetch(
        self,
        call: Callable[..., Any],
        *,
        endpoint: str,
        version: str | None = None,
        params: dict[str, Any] | None = None,
        path_vars: dict[str, Any] | None = None,
        model: type[Model],
        results_key: str | None = "results",
    ) -> Any:
        """Ejecuta un endpoint contra el transporte sync o async segun ``call``."""
        spec = self._resolve_version(endpoint, version)
        path = spec.path.format(**(path_vars or {}))
        response = call("GET", path, params=params or None)
        if inspect.isawaitable(response):
            return _extract_async(response, model, results_key)
        return _extract(model, response, results_key)

    def _register_version(
        self,
        endpoint: str,
        version: str,
        *,
        path: str,
        model: type[Model],
        deprecated: bool = False,
    ) -> None:
        specs = self._version_specs.setdefault(endpoint, {})
        specs[version] = VersionSpec(path=path, model=model, deprecated=deprecated)

    def _sorted_versions(self, endpoint: str) -> list[str]:
        return sorted(
            self._version_specs.get(endpoint, {}),
            key=_parse_version,
        )

    def _resolve_version(self, endpoint: str, version: str | None) -> VersionSpec:
        specs = self._version_specs.get(endpoint, {})

        if not specs:
            raise BCRAEndpointVersionError(
                f"No hay versiones registradas para '{endpoint}'."
            )

        if version is None:
            resolved = self._sorted_versions(endpoint)[-1]
        else:
            if version not in specs:
                disponibles = [
                    f"{v} (deprecada)" if specs[v].deprecated else v
                    for v in self._sorted_versions(endpoint)
                ]
                raise BCRAEndpointVersionError(
                    f"{endpoint} no tiene version '{version}'. "
                    f"Disponibles: {disponibles}"
                )
            resolved = version

        spec = specs[resolved]
        if spec.deprecated:
            warnings.warn(
                f"{endpoint} version {resolved} esta deprecada",
                DeprecationWarning,
                stacklevel=3,
            )

        return spec

    def versions(self, endpoint: str) -> dict[str, dict[str, bool]]:
        """Devuelve las versiones disponibles de un endpoint y su deprecacion.

        Ejemplo: {"1.0": {"deprecated": True}, "2.0": {"deprecated": False}}
        """
        return {
            v: {"deprecated": spec.deprecated}
            for v, spec in sorted(
                self._version_specs.get(endpoint, {}).items(),
                key=lambda item: _parse_version(item[0]),
            )
        }
