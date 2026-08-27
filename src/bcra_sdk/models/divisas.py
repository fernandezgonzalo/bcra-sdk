from dataclasses import dataclass


@dataclass
class Divisa:
    codigo: str
    denominacion: str


@dataclass
class ResultGetDivisasV1:
    divisas: list[Divisa]

    @classmethod
    def from_dict(cls, data: list) -> "ResultGetDivisasV1":
        return cls(divisas=[Divisa(**d) for d in data])
