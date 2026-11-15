# scrum-sdd

Framework de desarrollo asistido por IA que lleva un proyecto desde la idea hasta producción combinando **Scrum**, **Spec-Driven Development** y el documento **DERCAS** (ISO/IEC/IEEE 29148).

El agente trabaja fase por fase. Cada fase termina en una puerta que solo una persona puede abrir, y la trazabilidad requisito → criterio → historia → prueba se valida de forma automática.

## Qué incluye

- **10 skills de fase**, del descubrimiento a la operación.
- **4 skills de control** para aprobar, aceptar y consultar el estado.
- **Puertas de control**: ninguna fase inicia si la anterior no fue aprobada. La aprobación caduca si el documento aprobado se edita.
- **Validación de trazabilidad**: falla si un requisito no tiene criterio, una historia no tiene requisito o un criterio no tiene prueba.
- **Tres carriles** según el tamaño del cambio: completo, feature y hotfix.

## Requisitos

- Python **3.9 o superior** (ya requerido por los validadores del framework).
- Un agente compatible: Claude Code, Codex, OpenCode, Antigravity o Pi.
- **No necesitas Node.js, npm, uv, pip, Homebrew ni instalar paquetes Python.**
- Git es recomendable para trabajar en el proyecto, pero no es obligatorio para instalar Scrum-SDD.

**Guía detallada:** [Instalación y uso paso a paso](docs/GUIA-INSTALACION-Y-USO.md).

## Instalación desde GitHub (recomendada)

Repositorio oficial: **https://github.com/jssandoval/scrum-sdd**.

En **macOS / Linux** (Python 3.9+):

```bash
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh
```

En **Windows / PowerShell** (Python 3.9+):

```powershell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

Después abre una terminal nueva y, dentro de tu proyecto:

```bash
scrum-sdd init
scrum-sdd doctor
```

**Importante:** estos instaladores funcionan cuando esté publicada la etiqueta `v0.4.0` en el repositorio. Descargan una versión etiquetada, no el código cambiante de `main`. Puedes revisar los scripts antes de ejecutarlos. No requieren Node.js, npm, uv, pip ni Homebrew.

Guía para el mantenedor: [Publicar en GitHub y crear Releases](docs/PUBLICAR-EN-GITHUB.md).

## Instalación fácil (v0.4.0)

1. Descarga y descomprime el ZIP. Abre la terminal **dentro de la carpeta `scrum-sdd`**.
2. Ejecuta el comando correspondiente a tu sistema operativo:

**macOS / Linux**

```bash
sh install-cli.sh
```

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy Bypass -File .\install-cli.ps1
```

3. Abre una **nueva terminal** y ejecuta en cualquier proyecto:

```bash
cd ruta/a/mi-proyecto
scrum-sdd init
scrum-sdd doctor
```

`init` configura todos los agentes compatibles por defecto. Para uno específico usa `scrum-sdd init --agent claude` (también `codex`, `opencode`, `antigravity`, `pi`). En un proyecto existente, **no sobrescribe** `docs/estado.json`, `CLAUDE.md`, tus documentos fuente, specs ni código.

### Comandos de distribución

| Comando | Función |
| --- | --- |
| `scrum-sdd init [ruta]` | Preparar un proyecto nuevo o existente |
| `scrum-sdd doctor` | Comprobar entorno y detectar agentes |
| `scrum-sdd version` | Mostrar versión instalada |
| `scrum-sdd update [ruta]` | Sincronizar recursos administrados en un proyecto |

**Para actualizar la CLI global** a una versión descargada más reciente, vuelve a ejecutar `install-cli.sh` / `install-cli.ps1` desde la carpeta de esa nueva versión. `update` no descarga archivos ni cambia la versión instalada globalmente.

**Instalación antigua:** `bash install.sh /ruta/a/mi-proyecto` sigue disponible en macOS/Linux por compatibilidad; en Windows utiliza la nueva CLI.

La inicialización crea esto en tu proyecto:

```
mi-proyecto/
├── CLAUDE.md             # apunta a AGENTS.md
├── .claude/skills/       # los 14 skills (Claude Code)
├── .agents/skills/       # los mismos skills (Codex, OpenCode, Antigravity, Pi)
├── .opencode/commands/   # comandos de barra para OpenCode
├── .pi/prompts/          # comandos de barra para Pi
├── .framework/           # plantillas, scripts y versión
├── docs/
│   ├── 00-fuentes/       # documentación aportada (manuales, formularios, etc.)
│   ├── estado.json       # estado de puertas e historias
│   ├── 01-descubrimiento/
│   ├── 02-requisitos/
│   ├── 03-diseno/
│   ├── 04-arquitectura/
│   ├── 05-scrum/
│   ├── 06-pruebas/
│   └── 07-operacion/
├── specs/                # una spec por historia
├── src/
└── tests/
```

Si el agente ya estaba abierto en el proyecto, reinícialo para que cargue los skills.

## Inicio rápido

Todo se hace con skills dentro del agente. Los ejemplos usan `/`; en Codex escribe `$` en su lugar (`$descubrir`, `$aprobar`). El ciclo es siempre el mismo: lanzas el skill, el agente genera los documentos, tú los revisas y apruebas.

```
/descubrir Una app para que talleres mecánicos agenden citas por WhatsApp
```

Revisa lo que dejó en `docs/01-descubrimiento/` y aprueba:

```
/aprobar descubrimiento --por "Tu Nombre"
```

Continúa con las fases siguientes:

```
/dercas                    luego  /aprobar requisitos --por "Tu Nombre"
/diseno                    luego  /aprobar diseno --por "Tu Nombre"
/arquitectura              luego  /aprobar arquitectura --por "Tu Nombre"
/backlog                   luego  /aprobar backlog --por "Tu Nombre"
/setup                     luego  /aprobar setup --por "Tu Nombre"
```

Por cada historia del sprint:

```
/implementar HU-001
/clear
/auditar HU-001
/aceptar HU-001 --por "Tu Nombre"
```

El `/clear` (o una sesión nueva) antes de auditar es obligatorio: quien escribió el código no lo audita.

Cuando todas las historias estén aceptadas:

```
/release
```

## Comandos

### Skills de fase

| Skill | Fase | Qué produce | Se aprueba con |
| --- | --- | --- | --- |
| `/descubrir <idea>` | 0. Descubrimiento | Visión, Lean Canvas, hipótesis | `/aprobar descubrimiento` |
| `/dercas` | 1. Requisitos | `DERCAS.md` con RF, RNF, RN y CA en Gherkin | `/aprobar requisitos` |
| `/diseno` | 2. Diseño | BPMN, navegación, design system, pantallas | `/aprobar diseno` |
| `/arquitectura` | 3. Arquitectura | C4, modelo de datos, OpenAPI, ADRs | `/aprobar arquitectura` |
| `/backlog` | 4. Planificación | Backlog, DoR, DoD, Sprint 1 | `/aprobar backlog` |
| `/setup` | 5. Entorno | `AGENTS.md`, linters, Docker, CI | `/aprobar setup` |
| `/implementar HU-XXX` | 6. Ejecución | Spec de la historia, pruebas y código | Revisión del Pull Request |
| `/auditar HU-XXX` | 7. QA y seguridad | Informe de auditoría, pruebas E2E | `/aceptar HU-XXX` |
| `/release` | 8. Despliegue | Dockerfile, pipeline, runbook | Aprobación en CI/CD |
| `/operar` | 9. Operación | SLOs, telemetría, alertas | Review y Retrospectiva |

### Skills de control

| Skill | Para qué |
| --- | --- |
| `/estado` | Ver qué fases están aprobadas, el estado de cada historia y el siguiente paso |
| `/aprobar <fase> --por "<nombre>"` | Registrar la aprobación humana de una fase |
| `/aceptar HU-XXX --por "<nombre>"` | Registrar la aceptación de una historia tras la UAT |
| `/trazabilidad [HU-XXX]` | Validar la cadena requisito → criterio → historia → prueba |

`/aprobar` y `/aceptar` solo se ejecutan cuando tú los escribes. En Claude Code y Pi el agente no puede invocarlos por su cuenta; en los demás depende de las instrucciones de `AGENTS.md`. **No es una garantía de identidad**: un usuario con acceso a la terminal o al repositorio puede modificar el estado.

## Carriles

No todo cambio necesita las diez fases.

| Carril | Cuándo usarlo | Flujo |
| --- | --- | --- |
| `completo` | Producto nuevo | Las diez fases en orden |
| `feature` | Funcionalidad nueva en un proyecto ya instalado | `/dercas` → `/backlog` → `/implementar` → `/auditar` |
| `hotfix` | Corrección urgente | `/implementar` con prueba de regresión → `/auditar` |

Ejemplo de hotfix:

```
/implementar HU-042 --carril hotfix
```

### Adoptarlo en un proyecto existente

1. Ejecuta `install.sh` sobre el proyecto.
2. Lanza `/dercas` para documentar lo que ya está construido.
3. Aprueba en carril feature:
   ```
   /aprobar requisitos --por "Tu Nombre" --carril feature
   /setup
   /aprobar setup --por "Tu Nombre" --carril feature
   ```
4. Trabaja cada cambio nuevo en carril `feature` o `hotfix`.

## Convenciones

Los scripts validan lo que tiene formato predecible. Respeta estos identificadores:

| Elemento | Formato | Dónde |
| --- | --- | --- |
| Requisito funcional | `### RF-001 Título` + `**Prioridad:** Must` | DERCAS |
| Requisito no funcional | `### RNF-001 Título` | DERCAS |
| Regla de negocio | `### RN-001 Título` | DERCAS |
| Criterio de aceptación | `### CA-001 (RF-001) Título` | DERCAS |
| Historia de usuario | `### HU-001 Título` + `**Requisitos:** RF-001` | Product backlog |
| Prueba | El nombre o comentario de una prueba con aserciones contiene `CA-001`; además debe ejecutarse la suite | `tests/` o `src/` |

- IDs de tres dígitos, nunca reutilizados. Un requisito descartado se marca `Won't`, no se borra.
- Prioridad MoSCoW: `Must`, `Should`, `Could`, `Won't`.
- Sin subencabezados dentro de la sección de un ID.

## Problemas frecuentes

| Síntoma | Causa | Solución |
| --- | --- | --- |
| Un skill responde BLOQUEADO | Falta aprobar una fase anterior | `/estado` para ver cuál, luego `/aprobar` |
| Una fase aprobada aparece como modificada | El documento se editó después de aprobarlo | Revisar el cambio y volver a `/aprobar` |
| `/trazabilidad` falla | Un RF sin criterio, una historia sin RF o un criterio sin prueba | Corregir con el skill que indique el reporte |
| `/aceptar` rechaza la historia | No pasó por `/auditar` | Auditar primero, en sesión nueva |
| Los skills no aparecen al escribir `/` | El agente se abrió antes de instalar | Reiniciar el agente |
| `/release` responde BLOQUEADO | Hay historias sin aceptar | `/estado` y aceptar las pendientes |

## Integración continua

`/setup` copia un workflow de GitHub Actions a `.github/workflows/ci-cd.yml`. En cada Pull Request valida trazabilidad, lint, pruebas y dependencias. El despliegue a producción exige historias aceptadas y una aprobación manual en el environment `production`. Debes configurar scripts reales de despliegue y smoke tests; si faltan, CI falla y no simula un despliegue.

## Actualizar

```bash
cd scrum-sdd && git pull
./install.sh /ruta/a/mi-proyecto
```

Reinstalar actualiza skills, plantillas y scripts. No toca `docs/`, `specs/`, `AGENTS.md` ni tu código.

## Agentes soportados

El instalador deja el proyecto listo para los cinco. Los skills son los mismos; cambia dónde los busca cada agente y cómo se invocan.

| Agente | Lee los skills de | Reglas del proyecto | Invocación |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `CLAUDE.md` → `AGENTS.md` | `/aprobar ...` |
| Codex | `.agents/skills/` | `AGENTS.md` | `$aprobar ...` |
| OpenCode | `.agents/skills/` | `AGENTS.md` | `/aprobar ...` |
| Antigravity y `agy` | `.agents/skills/` | `AGENTS.md` | `/aprobar ...` |
| Pi | `.agents/skills/` | `AGENTS.md` | `/aprobar ...` o `/skill:aprobar ...` |

Notas:

- En OpenCode y Pi los comandos `/nombre` funcionan gracias a los envoltorios que el instalador genera en `.opencode/commands/` y `.pi/prompts/`.
- En Pi los skills y plantillas del proyecto solo cargan después de marcar el proyecto como confiable.
- Puedes cambiar de agente a mitad del proyecto: el estado vive en `docs/estado.json`, no en el agente.
- Para auditar, usa siempre una sesión nueva si tu agente no tiene subagentes con contexto limpio.

## Estructura del repo

```
scrum-sdd/
├── LICENSE
├── VERSION
├── install.sh
├── constitution/     # plantilla de AGENTS.md
├── skills/           # 10 de fase + 4 de control
├── templates/        # DERCAS, backlog, spec de historia, ADR, auditoría
├── scripts/          # gate.py (puertas), trace.py (trazabilidad)
├── ci/               # workflow de GitHub Actions
└── examples/         # proyecto de muestra de punta a punta
```

## Estado del proyecto

Versión 0.4.0. Incluye validación de evidencias y pruebas automáticas del framework. Los cinco agentes siguen pendientes de pruebas integrales en proyectos reales.

## Licencia

[MIT](LICENSE). Puedes usarlo, modificarlo y distribuirlo, también en proyectos comerciales, conservando el aviso de copyright.

El instalador copia la licencia a `.framework/LICENSE` en cada proyecto para cumplir ese requisito.

## Verificación del framework
Ejecuta `python3 -m unittest discover -s tests_framework -v` desde el repositorio. El validador de trazabilidad usa una comprobación estructural básica: **no demuestra por sí solo** que una prueba verifica el requisito. Ejecuta siempre el test suite real, revisa su significado en `/auditar` y bloquea los PR si fallan.

## Restricción de aprobación
`/aprobar` y `/aceptar` requieren invocación explícita por una persona en el chat, con `--por`. No se añade una autenticación extra. Es un control del flujo del agente, no una barrera frente a quien tenga acceso directo a los archivos o comandos de Python.

## Documentos fuente: manuales, formularios y matrices

**Ya puedes iniciar desde varios documentos**, no solo desde una idea. Copia PDF, Word, Excel, Markdown o imágenes a `docs/00-fuentes/` (subcarpetas `manuales/`, `lineamientos/`, `formularios/`, `matrices/`, `requerimientos/`, `otros/`). Ejecuta `/descubrir`, revisa el inventario y análisis de fuentes, resuelve contradicciones y aprueba. `/dercas` genera la matriz de trazabilidad documental con IDs de fuente y ubicación verificable.

El inventario es automático (ruta, tamaño, SHA-256); **la interpretación de contenido depende del agente**. Un archivo no legible se declara como pendiente; no se inventan datos. Cambiar fuentes después de aprobar invalida las aprobaciones de descubrimiento o requisitos que correspondan.

**Guía:** [Cómo usar documentos fuente](docs/USAR-DOCUMENTOS-FUENTE.md). **Ejemplo completo:** [Registro de clientes con manual y formulario contradictorios](examples/registro-clientes/README.md).
