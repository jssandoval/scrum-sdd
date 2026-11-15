> **SSDD v0.4.6**: Nombre corto de Scrum SDD. Todos los skills usan prefijo `ssdd-` (por ejemplo `/ssdd-descubrir`, `/ssdd-aprobar`). La CLI se llama `ssdd`. El repositorio GitHub sigue siendo `jssandoval/scrum-sdd`.

# SSDD — Scrum Spec-Driven Development

Framework de desarrollo asistido por IA que lleva un proyecto desde la idea hasta producción combinando **Scrum**, **Spec-Driven Development** y el documento **DERCAS** (ISO/IEC/IEEE 29148).

El agente trabaja fase por fase. Cada fase termina en una puerta que solo una persona puede abrir, y la trazabilidad requisito → criterio → historia → prueba se valida de forma automática.

## Qué incluye

- **10 skills de fase**, del descubrimiento a la operación.
- **5 skills de control** para aprobar, aceptar y consultar el estado.
- **Puertas de control**: ninguna fase inicia si la anterior no fue aprobada. La aprobación caduca si el documento aprobado se edita.
- **Validación de trazabilidad**: falla si un requisito no tiene criterio, una historia no tiene requisito o un criterio no tiene prueba.
- **Tres carriles** según el tamaño del cambio: completo, feature y hotfix.

## Requisitos

- Python **3.9 o superior** (ya requerido por los validadores del framework).
- Un agente compatible: Claude Code, Codex, OpenCode, Antigravity o Pi.
- **No necesitas Node.js, npm, uv, pip, Homebrew ni instalar paquetes Python.**
- Git es recomendable para trabajar en el proyecto, pero no es obligatorio para instalar SSDD (Scrum-SDD).

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
ssdd init
ssdd doctor
```

**Importante:** estos instaladores funcionan cuando esté publicada la etiqueta `v0.4.6` en el repositorio. Descargan una versión etiquetada, no el código cambiante de `main`. Puedes revisar los scripts antes de ejecutarlos. No requieren Node.js, npm, uv, pip ni Homebrew.

Guía para el mantenedor: [Publicar en GitHub y crear Releases](docs/PUBLICAR-EN-GITHUB.md).

## Instalación fácil (v0.4.6)

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
ssdd init
ssdd doctor
```

`init` configura todos los agentes compatibles por defecto. Para uno específico usa `ssdd init --agent claude` (también `codex`, `opencode`, `antigravity`, `pi`). En un proyecto existente, **no sobrescribe** `docs/estado.json`, `CLAUDE.md`, tus documentos fuente, specs ni código.

### Comandos de distribución

| Comando | Función |
| --- | --- |
| `ssdd init [ruta]` | Preparar un proyecto nuevo o existente |
| `ssdd doctor` | Comprobar entorno y detectar agentes |
| `ssdd version` | Mostrar versión instalada |
| `ssdd update [ruta]` | Sincronizar recursos administrados en un proyecto |

**Para actualizar la CLI global** a una versión descargada más reciente, vuelve a ejecutar `install-cli.sh` / `install-cli.ps1` desde la carpeta de esa nueva versión. `update` no descarga archivos ni cambia la versión instalada globalmente.

**Instalación antigua:** `bash install.sh /ruta/a/mi-proyecto` sigue disponible en macOS/Linux por compatibilidad; en Windows utiliza la nueva CLI.

La inicialización crea esto en tu proyecto:

```
mi-proyecto/
├── CLAUDE.md             # apunta a AGENTS.md
├── .claude/skills/       # los 15 skills (Claude Code)
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

Todo se hace con skills dentro del agente. Los ejemplos usan `/`; en Codex escribe `$` en su lugar (`$ssdd-descubrir`, `$ssdd-aprobar`). El ciclo es siempre el mismo: lanzas el skill, el agente genera los documentos, tú los revisas y apruebas.

```
/ssdd-descubrir Una app para que talleres mecánicos agenden citas por WhatsApp
```

Revisa lo que dejó en `docs/01-descubrimiento/` y aprueba:

```
/ssdd-aprobar descubrimiento --por "Tu Nombre"
```

Continúa con las fases siguientes:

```
/ssdd-dercas                    luego  /ssdd-aprobar requisitos --por "Tu Nombre"
/ssdd-diseno                    luego  /ssdd-aprobar diseno --por "Tu Nombre"
/ssdd-arquitectura              luego  /ssdd-aprobar arquitectura --por "Tu Nombre"
/ssdd-backlog                   luego  /ssdd-aprobar backlog --por "Tu Nombre"
/ssdd-setup                     luego  /ssdd-aprobar setup --por "Tu Nombre"
```

Por cada historia del sprint:

```
/ssdd-implementar HU-001
/clear
/ssdd-auditar HU-001
/ssdd-aceptar HU-001 --por "Tu Nombre"
```

El `/clear` (o una sesión nueva) antes de auditar es obligatorio: quien escribió el código no lo audita.

Cuando todas las historias estén aceptadas:

```
/ssdd-release
```

## Comandos

### Skills de fase

| Skill | Fase | Qué produce | Se aprueba con |
| --- | --- | --- | --- |
| `/ssdd-descubrir <idea>` | 0. Descubrimiento | Visión, Lean Canvas, hipótesis | `/ssdd-aprobar descubrimiento` |
| `/ssdd-dercas` | 1. Requisitos | `DERCAS.md` con RF, RNF, RN y CA en Gherkin | `/ssdd-aprobar requisitos` |
| `/ssdd-diseno` | 2. Diseño | BPMN, navegación, design system, pantallas | `/ssdd-aprobar diseno` |
| `/ssdd-arquitectura` | 3. Arquitectura | C4, modelo de datos, OpenAPI, ADRs | `/ssdd-aprobar arquitectura` |
| `/ssdd-backlog` | 4. Planificación | Backlog, DoR, DoD, Sprint 1 | `/ssdd-aprobar backlog` |
| `/ssdd-setup` | 5. Entorno | `AGENTS.md`, linters, Docker, CI | `/ssdd-aprobar setup` |
| `/ssdd-implementar HU-XXX` | 6. Ejecución | Spec de la historia, pruebas y código | Revisión del Pull Request |
| `/ssdd-auditar HU-XXX` | 7. QA y seguridad | Informe de auditoría, pruebas E2E | `/ssdd-aceptar HU-XXX` |
| `/ssdd-release` | 8. Despliegue | Dockerfile, pipeline, runbook | Aprobación en CI/CD |
| `/ssdd-operar` | 9. Operación | SLOs, telemetría, alertas | Review y Retrospectiva |

### Skills de control

| Skill | Para qué |
| --- | --- |
| `/ssdd-estado` | Ver qué fases están aprobadas, el estado de cada historia y el siguiente paso |
| `/ssdd-aprobar <fase> --por "<nombre>"` | Registrar la aprobación humana de una fase |
| `/ssdd-aceptar HU-XXX --por "<nombre>"` | Registrar la aceptación de una historia tras la UAT |
| `/ssdd-trazabilidad [HU-XXX]` | Validar la cadena requisito → criterio → historia → prueba |
| `/ssdd-revertir <fase> --por "Nombre" --motivo "Razón"` | Archivar fase aprobada y revocar su aprobación y las posteriores |

`/ssdd-aprobar` y `/ssdd-aceptar` solo se ejecutan cuando tú los escribes. En Claude Code y Pi el agente no puede invocarlos por su cuenta; en los demás depende de las instrucciones de `AGENTS.md`. **No es una garantía de identidad**: un usuario con acceso a la terminal o al repositorio puede modificar el estado.

## Carriles

No todo cambio necesita las diez fases.

| Carril | Cuándo usarlo | Flujo |
| --- | --- | --- |
| `completo` | Producto nuevo | Las diez fases en orden |
| `feature` | Funcionalidad nueva en un proyecto ya instalado | `/ssdd-dercas` → `/ssdd-backlog` → `/ssdd-implementar` → `/ssdd-auditar` |
| `hotfix` | Corrección urgente | `/ssdd-implementar` con prueba de regresión → `/ssdd-auditar` |

Ejemplo de hotfix:

```
/ssdd-implementar HU-042 --carril hotfix
```

### Adoptarlo en un proyecto existente

1. Ejecuta `install.sh` sobre el proyecto.
2. Lanza `/ssdd-dercas` para documentar lo que ya está construido.
3. Aprueba en carril feature:
   ```
   /ssdd-aprobar requisitos --por "Tu Nombre" --carril feature
   /ssdd-setup
   /ssdd-aprobar setup --por "Tu Nombre" --carril feature
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
| Un skill responde BLOQUEADO | Falta aprobar una fase anterior | `/ssdd-estado` para ver cuál, luego `/ssdd-aprobar` |
| Una fase aprobada aparece como modificada | El documento se editó después de aprobarlo | Revisar el cambio y volver a `/ssdd-aprobar` |
| `/ssdd-trazabilidad` falla | Un RF sin criterio, una historia sin RF o un criterio sin prueba | Corregir con el skill que indique el reporte |
| `/ssdd-aceptar` rechaza la historia | No pasó por `/ssdd-auditar` | Auditar primero, en sesión nueva |
| Los skills no aparecen al escribir `/` | El agente se abrió antes de instalar | Reiniciar el agente |
| `/ssdd-release` responde BLOQUEADO | Hay historias sin aceptar | `/ssdd-estado` y aceptar las pendientes |

## Integración continua

`/ssdd-setup` copia un workflow de GitHub Actions a `.github/workflows/ci-cd.yml`. En cada Pull Request valida trazabilidad, lint, pruebas y dependencias. El despliegue a producción exige historias aceptadas y una aprobación manual en el environment `production`. Debes configurar scripts reales de despliegue y smoke tests; si faltan, CI falla y no simula un despliegue.

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
| Claude Code | `.claude/skills/` | `CLAUDE.md` → `AGENTS.md` | `/ssdd-aprobar ...` |
| Codex | `.agents/skills/` | `AGENTS.md` | `$ssdd-aprobar ...` |
| OpenCode | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` |
| Antigravity y `agy` | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` |
| Pi | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` o `/skill:aprobar ...` |

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

Versión 0.4.6. Incluye validación de evidencias y pruebas automáticas del framework. Los cinco agentes siguen pendientes de pruebas integrales en proyectos reales.

## Licencia

[MIT](LICENSE). Puedes usarlo, modificarlo y distribuirlo, también en proyectos comerciales, conservando el aviso de copyright.

El instalador copia la licencia a `.framework/LICENSE` en cada proyecto para cumplir ese requisito.

## Verificación del framework
Ejecuta `python3 -m unittest discover -s tests_framework -v` desde el repositorio. El validador de trazabilidad usa una comprobación estructural básica: **no demuestra por sí solo** que una prueba verifica el requisito. Ejecuta siempre el test suite real, revisa su significado en `/ssdd-auditar` y bloquea los PR si fallan.

## Restricción de aprobación
`/ssdd-aprobar` y `/ssdd-aceptar` requieren invocación explícita por una persona en el chat, con `--por`. No se añade una autenticación extra. Es un control del flujo del agente, no una barrera frente a quien tenga acceso directo a los archivos o comandos de Python.

## Documentos fuente: manuales, formularios y matrices

**Ya puedes iniciar desde varios documentos**, no solo desde una idea. Copia PDF, Word, Excel, Markdown o imágenes a `docs/00-fuentes/` (subcarpetas `manuales/`, `lineamientos/`, `formularios/`, `matrices/`, `requerimientos/`, `otros/`). Ejecuta `/ssdd-descubrir`, revisa el inventario y análisis de fuentes, resuelve contradicciones y aprueba. `/ssdd-dercas` genera la matriz de trazabilidad documental con IDs de fuente y ubicación verificable.

El inventario es automático (ruta, tamaño, SHA-256); **la interpretación de contenido depende del agente**. Un archivo no legible se declara como pendiente; no se inventan datos. Cambiar fuentes después de aprobar invalida las aprobaciones de descubrimiento o requisitos que correspondan.

**Guía:** [Cómo usar documentos fuente](docs/USAR-DOCUMENTOS-FUENTE.md). **Ejemplo completo:** [Registro de clientes con manual y formulario contradictorios](examples/registro-clientes/README.md).


## Actualización desde instalaciones anteriores (v0.4.6 y previas)

En macOS/Linux, vuelve a ejecutar el instalador remoto documentado arriba para actualizar la CLI global y sus recursos. En Windows, ejecuta de nuevo el instalador remoto PowerShell. Después entra al proyecto y ejecuta:

```bash
ssdd update --agent all
ssdd version
ssdd doctor
```

`ssdd update` conserva `docs/estado.json`, DERCAS, documentación fuente y código. La versión anterior de los skills genéricos puede seguir instalada: sus archivos no se eliminan automáticamente para evitar borrar personalizaciones. Usa únicamente los comandos `ssdd-*`. El historial de cada reversión queda en `docs/historico-fases/`.

## Elección del stack por el programador

En `/ssdd-arquitectura`, el agente recomienda y pide que el programador elija **frontend, backend, interoperabilidad, persistencia e infraestructura** antes de generar el ADR definitivo. La decisión se conserva en `ADR-001-stack-tecnologico.md` y se aprueba junto con la fase.

## Revertir una fase aprobada

```text
/ssdd-revertir arquitectura --por "Nombre" --motivo "Modificar tecnología elegida"
```

Se guarda copia del estado y documentos de la fase en `docs/historico-fases/`; las aprobaciones de esa fase y las posteriores se revocan. Los documentos originales, el código y las historias no se borran. Es una reversión del workflow, no un `git reset`.
