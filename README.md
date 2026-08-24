# BCRA-SDK

[Python 3.10+] • [Network: HTTPX] • [CLI: Typer & Rich] • [License: MIT]

SDK moderno, eficiente y fuertemente tipado para interactuar con la API pública del Banco Central de la República Argentina (BCRA). Proporciona acceso nativo síncrono y asíncrono a los datos económicos, estructurando las respuestas en dataclasses inmutables y ofreciendo una interfaz de línea de comandos (CLI) lista para usar.


## Características principales

* Doble cliente nativo: Soporte para flujos síncronos (BcraClient) y asíncronos (AsyncBcraClient) con pool de conexiones optimizado mediante httpx.

* Arquitectura por namespaces: Métodos organizados por dominios de negocio (.deudores, .cheques, .cambiarias) para evitar la saturación del autocompletado en el IDE.

* Acceso público libre: Diseñado específicamente para consumir endpoints públicos sin necesidad de tokens de autenticación ni registros previos.

* Estructuras fuertemente tipadas: Conversión automática de respuestas JSON a objetos nativos de Python con validación de tipos (montos a float, banderas a bool).

* CLI profesional integrada: Herramienta de terminal generada automáticamente con formateo estético de datos mediante tablas visuales (Typer y Rich).


## Instalación

El paquete se puede instalar directamente desde el repositorio de GitHub, ya que aún no está disponible en PyPI. Puedes instalarlo apuntando a la URL del release o al repositorio directamente:

```bash
# Usando uv (recomendado) apuntando al release
uv add "bcra-sdk @ https://github.com/fernandezgonzalo/bcra-sdk/releases/download/v0.0.1/bcra_sdk-0.0.1-py3-none-any.whl"

# Con pip apuntando al release
pip install "bcra-sdk @ https://github.com/fernandezgonzalo/bcra-sdk/releases/download/v0.0.1/bcra_sdk-0.0.1-py3-none-any.whl"

# O también puedes instalarlo directamente desde el repositorio (requiere git)
uv add "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.1"
pip install "bcra-sdk @ git+https://github.com/fernandezgonzalo/bcra-sdk.git@v0.0.1"
```

> [!NOTE]
> Reemplaza v0.0.1 con la versión específica que desees instalar. Consulta la página de [releases](https://github.com/fernandezgonzalo/bcra-sdk/releases) para ver las versiones disponibles.

## Guia de Uso Rapida

### Cliente Sincrono

Ideal para scripts de automatización, tareas programadas (cron) o aplicaciones tradicionales.

```python
from bcra_sdk import BcraClient

with BcraClient() as bcra:
    reporte = bcra.deudores.get_actual("20111111112")

    print(f"Denominación: {reporte.denominacion}")
    for deuda in reporte.deudas:
        print(f"Banco: {deuda.entidad} | Monto: ${deuda.monto:,.2f} | Situación: {deuda.situacion}")
```

### Cliente Asincrono

Diseñado para aplicaciones de alta concurrencia, microservicios o integraciones nativas con FastAPI.

```python
import asyncio
from bcra_sdk import AsyncBcraClient

async def main():
    async with AsyncBcraClient() as bcra:

        cotizaciones = await bcra.cambiarias.get_cotizaciones()
        for cotizacion in cotizaciones:
            print(f"Moneda: {cotizacion.codigo_moneda} | Venta: {cotizacion.venta}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Interfaz de linea de comandos (CLI) [No Implementado Aun]

La librería registra automáticamente el comando ejecutable bcra en tu entorno tras la instalación.

Comandos disponibles:

* bcra deudores actual [CUIT]: Obtiene la situación crediticia actual y tablas de deuda para el CUIT provisto.
* bcra cambiarias cotizaciones: Muestra por consola las cotizaciones cambiarias vigentes del BCRA.
* bcra --help: Despliega la ayuda del sistema y el árbol de subcomandos.

Ejemplo de uso directo en la terminal:

```bash
bcra deudores actual 20111111112
```

## Estructura del proyecto

El repositorio sigue el estándar moderno de empaquetado de la comunidad de Python, aislando los entornos de desarrollo de los artefactos de distribución:

```bash
bcra-sdk/
├── pyproject.toml
├── README.md
├── src/
│   └── bcra_sdk/
│       ├── __init__.py
│       ├── _base.py
│       ├── _parsers.py
│       ├── client.py
│       ├── async_client.py
│       ├── deudores.py
│       ├── cheques.py
│       ├── cambiarias.py
│       └── schemas.py
└── tests/
    ├── conftest.py
    ├── test_client.py
    └── test_async_client.py
```

## Control de calidad local (Pre-commit hooks)

Antes de confirmar cualquier cambio (`git commit`), utilizamos pre-commit para ejecutar automáticamente análisis estáticos, formateo de código y chequeos de sintaxis. Esto garantiza que ningún código "sucio" llegue al repositorio remoto.

### Configuración inicial:

1. Sincroniza tu entorno de desarrollo

```bash
uv sync
```

2. Instala los hooks de git en tu repositorio local:

```bash
uv run pre-commit install
```

A partir de este momento, cada commit correrá de forma automática:

* **Ruff Linter**: Evalúa errores comunes de Python y malas prácticas.
* **Ruff Formatter**: Formatea tu código bajo el estilo estandarizado.
* **Chequeos básicos**: Verifica sintaxis de archivos YAML, elimina espacios al final de las líneas y asegura saltos de línea correctos.

Para correr los chequeos manualmente en todos los archivos:

```bash
uv run pre-commit run --all-files
```

## Proceso de Pull Requests (PRs)

Toda contribución debe integrarse mediante un Pull Request hacia la rama develop. Requisitos para que un PR sea aprobado y fusionado:

1. **Formulario descriptivo**: Explica qué hace el cambio, por qué y cómo se probó.
2. **Pruebas unitarias**: Si agregas una funcionalidad o corriges un bug, debes acompañarlo con su respectivo test en tests/. La suite debe pasar al 100%:

```bash
uv run pytest
```

3. **Aprobacion**: Requiere la revisión y el visto bueno de al menos un mantenedor.
4. **Historial limpio**: Se prefiere el uso de "Squash and Merge" al fusionar.

## Convención de Commits (Conventional Commits)

Para mantener un historial de Git ordenado, legible y permitir la generación automática de Changelogs,
adoptamos la especificación de [Conventional Commits](https://www.conventionalcommits.org/).

Cada mensaje de commit debe seguir la siguiente estructura:

```text
<tipo>(<alcance opcional>): <descripción corta en minúscula>

[cuerpo opcional con más detalles]

[pie de página opcional para cerrar issues o indicar cambios importantes]
```

### Tipos de Commits Permitidos:

* `feat`: Una nueva funcionalidad para el usuario (se traduce en un incremento de versión Minor).
* `fix`: La resolución de un error o bug (se traduce en un incremento de versión Patch).
* `docs`: Cambios únicamente en la documentación (como el README o archivos .md).
* `style`: Cambios cosméticos que no afectan el comportamiento del código (espacios, formateo con Ruff, punto y coma perdidos).
* `refactor`: Reestructuración de código que no corrige un error ni añade una funcionalidad (ej. renombrar variables, optimizar funciones).
* `test`: Añadir pruebas unitarias faltantes o corregir pruebas existentes.
* `chore`: Tareas de mantenimiento general, actualización de dependencias (uv.lock), o configuraciones de build/CI.

Ejemplos:

```bash
# Ejemplo simple de una nueva característica
git commit -m "feat(deudores): agregar consulta de deudores históricos"

# Ejemplo de una corrección de bug
git commit -m "fix(client): resolver timeout en conexiones lentas con httpx"

# Ejemplo con un cambio disruptivo (Breaking Change) que requiere subir la versión "Major"
# Se añade un signo de exclamación (!) antes de los dos puntos
git commit -m "feat(api)!: renombrar el método get_actual por fetch_status"
```

## Licencia

Este proyecto está bajo la Licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente en entornos comerciales o privados.
