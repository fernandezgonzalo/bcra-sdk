# Reintentos

La API del BCRA es pública y no ofrece SLA, por lo que el SDK reintenta errores
transitorios de forma automática.

## Política por defecto

Por defecto cada petición se reintenta **hasta 2 veces** (3 intentos en total) ante:

- Códigos de estado `429`, `500`, `502`, `503` y `504`.
- Timeouts de red (`httpx.TimeoutException`).

La espera entre intentos crece de forma exponencial (`backoff * 2^n`, con `backoff = 0.5s`
por defecto), salvo que el servidor envíe el header `Retry-After`, en cuyo caso se respeta
ese tiempo. No se reintentan otros errores 4xx (p. ej. `404`) ni errores de conexión.

Los reintentos se loguean en nivel `WARNING` con el logger `bcra_sdk.transport`.

## Configurar la política

Se pasa una `RetryPolicy` al client:

```python
from bcra_sdk import BCRAClient, RetryPolicy

# Sin reintentos
client = BCRAClient(retries=RetryPolicy(max_retries=0))

# Más reintentos, espera base de 1 segundo, sin reintentar timeouts
client = BCRAClient(
    retries=RetryPolicy(
        max_retries=5,
        backoff=1.0,
        retry_on_timeout=False,
    )
)
```

`RetryPolicy` es un `dataclass` congelado con los campos:

| Campo | Default | Descripción |
|-------|---------|-------------|
| `max_retries` | `2` | Cantidad de reintentos (`0` desactiva el retry) |
| `backoff` | `0.5` | Espera base en segundos |
| `retry_on_timeout` | `True` | Si se reintentan timeouts |
| `statuses` | `(429, 500, 502, 503, 504)` | Códigos de estado a reintentar |

Si la política de retry se agota, se propaga el último error (`BCRAHTTPError` o
`BCRATimeoutError`) a la aplicación.
