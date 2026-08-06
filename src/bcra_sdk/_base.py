from __future__ import annotations

import warnings

from .exceptions import BCRAEndpointVersionError


def endpoint(version: str, *, name: str | None, deprecated: bool = False):
    """Marca un metodo como la implementacion de un endpoint publico en una
    version puntual de la API del BCRA. Varias implementaciones pueden
    compartir "name" (mismo endpoint logico, distintas versiones) sin que
    eso afecte a otros endpoints de la misma clase.

    @endpoint(version="1.0", name="get_deudas", deprecated=True)
    def get_deudas_v1(self, cuit): ...

    @endpoint(version="1.0", name="get_deudas")
    def get_deudas_v2(self, identification): ...
    """

    def deco(func):
        func._endpoint_version = _parse_version(version)
        func._endpoint_name = name or func.__name__
        func._endpoint_deprecated = deprecated
        return func

    return deco


def _parse_version(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in version.split("."))


def _fmt_version(version: tuple[int, ...]) -> str:
    return ".".join(map(str, version))


class VersionedMethod:
    """Agrupa todas las implementaciones (versiones) de un mismo endpoint logico"""

    def __init__(self, name: str):
        self.name = name
        self.impls: dict[tuple[int, ...], object] = {}
        self.deprecated: set[tuple[int, ...]] = set()

    def add(self, func) -> None:
        version = func._endpoint_version
        self.impls[version] = func
        if func._endpoint_deprecated:
            self.deprecated.add(version)

    @property
    def latest(self) -> tuple[int, ...]:
        return max(self.impls)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        return BoundVersionedMethod(self, obj)


class BoundVersionedMethod:
    """Callable resultante de acceder a un VersionesMethod desde una instancia"""

    def __init__(self, vm: VersionedMethod, instance):
        self._vm = vm
        self._instance = instance

    def _resolve(self, version: str | None):
        v = _parse_version(version) if version else self._vm.latest
        if v not in self._vm.impls:
            disponibles = [_fmt_version(k) for k in self._vm.impls]
            raise BCRAEndpointVersionError(
                f"{self._vm.name} no tiene version '{version}'. "
                f"Disponibles: {disponibles}"
            )
        if v in self._vm.deprecated:
            warnings.warn(
                f"{self._vm.name} es version {_fmt_version(v)} esta deprecado",
                DeprecationWarning,
                stacklevel=3,
            )

        return self._vm.impls[v]

    def versions(self) -> list[str]:
        return [_fmt_version(v) for v in self._vm.impls]

    def __call__(self, *args, version: str | None = None, **kwargs):
        func = self._resolve(version)
        return func(self._instance, *args, **kwargs)


class ResourceMeta(type):
    """Agrupa, al crear la clase, todos los metodos @endpoint por nombre publico"""

    def __new__(mcls, clsname, bases, ns):
        grouped: dict[str, VersionedMethod] = {}
        for attr_name, val in list(ns.items()):
            if callable(val) and hasattr(val, "_endpoint_name"):
                pub_name = val._endpoint_name
                vm = grouped.setdefault(pub_name, VersionedMethod(pub_name))
                vm.add(val)
        ns.update(grouped)

        return super().__new__(mcls, clsname, bases, ns)


class Resource(metaclass=ResourceMeta):
    def __init__(self, transport):
        self._t = transport
