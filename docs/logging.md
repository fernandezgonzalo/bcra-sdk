# Logging

La librería **no configura handlers** (buena práctica en librerías: nunca tocar el root
logger). Usa loggers con el prefijo `bcra_sdk`:

- `bcra_sdk.client`
- `bcra_sdk.transport`
- `bcra_sdk.deudores`
- `bcra_sdk.cheques`
- `bcra_sdk.estadisticas_cambiarias`

Por defecto solo está presente un `NullHandler`, así que la librería no emite logs por
defecto. Para habilitar el diagnóstico:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("bcra_sdk").setLevel(logging.DEBUG)
```

Niveles usados:

- `INFO`: cada llamada a un endpoint (p. ej. "Consultando cotizaciones (fecha=...)").
- `DEBUG`: comandos HTTP, resúmenes de respuestas (totales, cantidades) y errores al
  abrir/cerrar el client.
- `ERROR`: respuestas HTTP con error (código y body).
