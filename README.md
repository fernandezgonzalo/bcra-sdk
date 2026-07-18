===============================================================================
                                   bcra-sdk
===============================================================================

[Python 3.10+] [Network: HTTPX] [CLI: Typer & Rich] [Licencia: MIT]

SDK moderno, eficiente y fuertemente tipado para interactuar con la API publica
del Banco Central de la Republica Argentina (BCRA). Esta biblioteca proporciona
acceso nativo tanto sincronico como asincronico a los datos economicos del banco,
estructurando las respuestas en dataclasses inmutables y ofreciendo una interfaz
de linea de comandos (CLI) lista para usar.

-------------------------------------------------------------------------------
1. CARACTERISTICAS CORE
-------------------------------------------------------------------------------

* Doble Cliente Nativo: Soporte completo para flujos sincronos (BcraClient) y
  asincronos (AsyncBcraClient) utilizando un pool de conexiones optimizado
  via httpx.
* Arquitectura de Namespaces: Metodos organizados por dominios de negocio claros
  (.deudores, .cheques, .cambiarias) evitando la saturacion del autocompletado
  en el IDE.
* Acceso Publico Libre: Disenado especificamente para consumir los endpoints
  publicos sin requerir gestiones complejas de tokens de autenticacion o
  registros previos.
* Estructuras Fuertemente Tipadas: Conversion automatizada de respuestas JSON
  crudas a objetos nativos de Python con validaciones internas de tipos de datos
  (montos a float, banderas a bool).
* CLI Profesional Integrada: Herramienta de terminal autogenerada que incluye
  formateo estetico de datos mediante tablas visuales gracias a Typer y Rich.

-------------------------------------------------------------------------------
2. INSTALACION
-------------------------------------------------------------------------------

Instala el paquete directamente utilizando tu gestor de dependencias preferido:
TODO: Arreglar esto
# Con uv (Recomendado)
uv add bcra-sdk

# Con pip tradicional
pip install bcra-sdk

-------------------------------------------------------------------------------
3. GUIA DE USO RAPIDO
-------------------------------------------------------------------------------

--- 3.1. Cliente Sincronico ---
Ideal para scripts de automatizacion, tareas programadas (cron) o aplicaciones
basadas en frameworks tradicionales.

from bcra_sdk import BcraClient

# Uso recomendado mediante Context Manager para gestionar el pool de conexiones
with BcraClient() as bcra:
    # Consulta la situacion crediticia en la Central de Deudores
    reporte = bcra.deudores.get_actual("20111111112")

    print(f"Denominacion: {reporte.denominacion}")
    for deuda in reporte.deudas:
        print(f"Banco: {deuda.entidad} | Monto: ${deuda.monto:,.2f} | Situacion: {deuda.situacion}")


--- 3.2. Cliente Asincronico ---
Disenado para aplicaciones de alta concurrencia, microservicios o integraciones
nativas con FastAPI.

import asyncio
from bcra_sdk import AsyncBcraClient

async def main():
    async with AsyncBcraClient() as bcra:
        # Consulta de cotizaciones del mercado cambiario de forma asincrona
        cotizaciones = await bcra.cambiarias.get_cotizaciones()
        for cotizacion in cotizaciones:
            print(f"Moneda: {cotizacion.codigo_moneda} | Venta: {cotizacion.venta}")

if __name__ == "__main__":
    asyncio.run(main())

-------------------------------------------------------------------------------
4. INTERFAZ DE LINEA DE COMANDOS (CLI)
-------------------------------------------------------------------------------

La libreria registra automaticamente el comando ejecutable "bcra" en tu entorno
tras la instalacion.

Comandos Disponibles:
* bcra deudores actual [CUIT]    Obtiene la situacion crediticia actual y
                                 tablas de deuda para el CUIT provisto.
* bcra cambiarias cotizaciones   Muestra por consola las cotizaciones cambiarias
                                 vigentes del BCRA.
* bcra --help                    Despliega la ayuda del sistema y el arbol de
                                 subcomandos.

Ejemplo de uso directo en la terminal:
$ bcra deudores actual 20111111112

-------------------------------------------------------------------------------
5. ESTRUCTURA DEL PROYECTO
-------------------------------------------------------------------------------

El repositorio sigue el estandar moderno de empaquetado de la comunidad de Python,
aislando los entornos de desarrollo de los artefactos de distribucion:

bcra-sdk/
├── pyproject.toml         # Configuracion unificada de uv, ruff y dependencias
├── README.txt             # El documento que estas leyendo
├── src/
│   └── bcra_sdk/          # Unico codigo empaquetado e instalado al usuario
│       ├── __init__.py    # Exposicion de la fachada publica y logging base
│       ├── _base.py       # Orquestador interno de URLs y configuraciones globales
│       ├── _parsers.py    # Transformacion segura de JSON a Dataclasses
│       ├── client.py      # Cliente de fachada Sincronico
│       ├── async_client.py# Cliente de fachada Asincronico
│       ├── deudores.py    # Submodulo / Namespace de Central de Deudores
│       ├── cheques.py     # Submodulo / Namespace de Cheques Denunciados
│       ├── cambiarias.py  # Submodulo / Namespace de Estadisticas Cambiarias
│       └── schemas.py     # Modelos de datos y Dataclasses inmutables
└── tests/                 # Suite de testing externa (No se distribuye en PyPI)
    ├── conftest.py        # Fixtures globales y respuestas de mock
    ├── test_client.py     # Tests unitarios sincronicos utilizando respx
    └── test_async_client.py # Tests unitarios asincronos (@pytest.mark.asyncio)

-------------------------------------------------------------------------------
6. GUIA DE DESARROLLO Y FLUJO DE TRABAJO
-------------------------------------------------------------------------------

Para mantener el codigo limpio, consistente y evitar dolores de cabeza al
integrar nuevas funcionalidades, seguimos un flujo de trabajo estricto apoyado
por herramientas de automatizacion.

--- 6.1. Gitflow (Estrategia de Ramas) ---
Utilizamos una version simplificada de Gitflow para organizar el repositorio:

* main: Contiene unicamente codigo estable y productivo. Cada commit en esta
  rama corresponde a una version publicada (tag) en PyPI.
* develop: Es la rama de integracion. Aqui se acumulan las ultimas
  caracteristicas listas para la proxima version estable.
* Ramas de soporte (feature/*, bugfix/*, hotfix/*):
  - Para crear una nueva funcionalidad: git checkout -b feature/nombre (desde develop).
  - Para corregir un error: git checkout -b bugfix/nombre (desde develop).
  - Para arreglos criticos en produccion: git checkout -b hotfix/nombre (desde main).

--- 6.2. Control de Calidad Local (Pre-commit Hooks) ---
Antes de confirmar cualquier cambio (git commit), utilizamos pre-commit para
ejecutar automaticamente analisis estaticos, formateo de codigo y chequeos de
sintaxis. Esto garantiza que ningun codigo "sucio" llegue al repositorio remoto.

Configuracion inicial:
1. Sincroniza tu entorno de desarrollo:
   uv sync
2. Instala los hooks de git en tu repositorio local:
   uv run pre-commit install

A partir de este momento, cada commit correra de forma automatica:
* Ruff Linter: Evalua errores comunes de Python y malas practicas.
* Ruff Formatter: Formatea tu codigo bajo el estilo estandarizado.
* Chequeos basicos: Verifica sintaxis de archivos YAML, elimina espacios al
  final de las lineas y asegura saltos de linea correctos.

Para correr los chequeos manualmente en todos los archivos:
uv run pre-commit run --all-files

--- 6.3. Proceso de Pull Requests (PRs) ---
Toda contribucion debe integrarse mediante un Pull Request hacia la rama "develop".
Requisitos para que un PR sea aprobado y fusionado:

1. Formulario descriptivo: Explica que hace el cambio, por que y como se probo.
2. Pruebas unitarias: Si agregas una funcionalidad o corregis un bug, debes
   acompanarlo con su respectivo test en "tests/". La suite debe pasar al 100%:
   uv run pytest
3. Aprobacion: Requiere la revision y el visto bueno de al menos un mantenedor.
4. Historial limpio: Se prefiere el uso de "Squash and Merge" al fusionar.

### Convención de Commits (Conventional Commits)

Para mantener un historial de Git ordenado, legible y permitir la **generación automática de Changelogs** (historiales de cambios), adoptamos la especificación de [Conventional Commits](https://www.conventionalcommits.org/).

Cada mensaje de commit debe seguir la siguiente estructura:

```text
<tipo>(<alcance opcional>): <descripción corta en minúscula>

[cuerpo opcional con más detalles]

[pie de página opcional para cerrar issues o indicar cambios importantes]
```

#### Tipos de Commits Permitidos:

*   **`feat`**: Una nueva funcionalidad para el usuario (se traduce en un incremento de versión **Minor**).
*   **`fix`**: La resolución de un error o bug (se traduce en un incremento de versión **Patch**).
*   **`docs`**: Cambios únicamente en la documentación (como el README o archivos `.md`).
*   **`style`**: Cambios cosméticos que no afectan el comportamiento del código (espacios, formateo con Ruff, punto y coma perdidos).
*   **`refactor`**: Reestructuración de código que no corrige un error ni añade una funcionalidad (ej. renombrar variables, optimizar funciones).
*   **`test`**: Añadir pruebas unitarias faltantes o corregir pruebas existentes.
*   **`chore`**: Tareas de mantenimiento general, actualización de dependencias (`uv.lock`), o configuraciones de build/CI.

#### Ejemplos Prácticos:

```bash
# Ejemplo simple de una nueva característica
git commit -m "feat(deudores): agregar consulta de deudores históricos"

# Ejemplo de una corrección de bug
git commit -m "fix(client): resolver timeout en conexiones lentas con httpx"

# Ejemplo con un cambio disruptivo (Breaking Change) que requiere subir la versión "Major"
# Se añade un signo de exclamación (!) antes de los dos puntos
git commit -m "feat(api)!: renombrar el método get_actual por fetch_status"
```

-------------------------------------------------------------------------------
7. LICENCIA
-------------------------------------------------------------------------------

Este proyecto esta bajo la Licencia MIT. Podes usarlo, modificarlo y distribuirlo
libremente en entornos comerciales o privados.
