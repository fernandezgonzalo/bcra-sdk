from unittest.mock import MagicMock

import httpx


def test_get_deudas(client, monkeypatch):
    cuit = "1234567890"
    fake_data = {
        "status": 200,
        "results": {
            "identificacion": int(cuit),
            "denominacion": "PEPE",
            "periodos": [
                {
                    "periodo": "202606",
                    "entidades": [
                        {
                            "entidad": "INDUSTRIAL AND COMMERCIAL BANK OF CHINA (ARGENTINA) S.A.U.",
                            "situacion": 1,
                            "fechaSit1": "2017-05-30",
                            "monto": 1121.0,
                            "diasAtrasoPago": 0,
                            "refinanciaciones": False,
                            "recategorizacionOblig": False,
                            "situacionJuridica": False,
                            "irrecDisposicionTecnica": False,
                            "enRevision": False,
                            "procesoJud": False,
                        }
                    ],
                }
            ],
        },
    }
    mock_response = httpx.Response(200, json=fake_data)

    monkeypatch.setattr(
        client.deudores._t, "request", MagicMock(return_value=mock_response)
    )

    data = client.deudores.get_deudas(cuit=cuit)

    assert str(data.identificacion) == cuit
