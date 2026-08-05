from ._base import Resource, endpoint
from .models.deudores import Results


class Deudores(Resource):
    @endpoint(version="1.0", name="get_deudas")
    def get_deudas_v1(self, cuit: str) -> Results:
        r = self._t.request("GET", f"/centraldedeudores/v1.0/Deudas/{cuit}")
        result = Results.from_dict(r.json()["results"])
        return result
