# SSDD — Scrum Spec-Driven Development

[![Licencia: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](#requisitos)
[![Agentes](https://img.shields.io/badge/agentes-Claude%20Code%20%7C%20Codex%20%7C%20OpenCode%20%7C%20Antigravity%20%7C%20Pi-6e5494.svg)](#agentes-soportados)

[English](README.md) | **Español**

> Los agentes de IA inventan requisitos, pierden la trazabilidad entre specs y código, y avanzan de fase sin que nadie la aprobó. SSDD lo frena: cada fase termina en una puerta que solo una persona puede abrir, y la cadena **requisito → criterio de aceptación → historia de usuario → prueba** se valida de forma automática, no confiando en la palabra del agente.

SSDD lleva un proyecto de la idea a producción combinando **Scrum**, **Spec-Driven Development** y el documento **DERCAS** (ISO/IEC/IEEE 29148). Trabaja fase por fase, dentro del agente que ya usás — sin IDE nuevo, sin ventana de chat nueva.

## Por qué SSDD

Si ya probaste un flujo spec-driven con un agente de IA, seguro te topaste con alguno de estos:

- El agente "se auto-aprueba" y pasa a la siguiente fase.
- Requisitos, criterios de aceptación y pruebas se desalinean en silencio — nadie lo nota hasta QA o producción.
- Revertir una mala decisión de arquitectura significa o vivir con ella o volar todo el historial.

La respuesta de SSDD a cada uno:

| Problema | Mecanismo de SSDD |
| --- | --- |
| El agente se auto-aprueba | `/ssdd-aprobar` y `/ssdd-aceptar` solo corren cuando una persona los escribe en el chat, con `--por "Nombre"` |
| Spec y código se desalinean | `/ssdd-trazabilidad` falla ruidosamente si un requisito no tiene criterio, una historia no tiene requisito, o un criterio no tiene prueba |
| No se puede revertir una fase con seguridad | `/ssdd-revertir` archiva la fase con copia verificable en `docs/historico-fases/` y revoca las aprobaciones posteriores — sin tocar `src/`, `tests/` ni los documentos de otras fases |
| Editar un documento aprobado pasa inadvertido | La aprobación se invalida automáticamente en el momento en que el documento aprobado cambia |

## Cómo funciona

```
idea ──▶ descubrimiento ──▶ requisitos ──▶ diseño ──▶ arquitectura ──▶ backlog ──▶ setup
                 (cada fase termina en una puerta que solo abre una persona)
                                │
                                ▼
       por historia:  implementar ──▶ auditar (sesión nueva) ──▶ aceptar ──▶ release ──▶ operar
```

Ninguna fase inicia hasta que la anterior esté aprobada. Ninguna historia se acepta hasta que fue auditada en una sesión limpia — quien escribió el código no la audita.

## Inicio rápido

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh

# Windows / PowerShell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

Luego, dentro de tu proyecto, en una terminal nueva:

```bash
ssdd init
ssdd doctor
```

Reinicia tu agente para que cargue los skills nuevos, y después:

```
/ssdd-descubrir Una app para que talleres mecánicos agenden citas por WhatsApp
```

Revisa lo que quedó en `docs/01-descubrimiento/` y apruébalo:

```
/ssdd-aprobar descubrimiento --por "Tu Nombre"
```

Ese es todo el ciclo: corres un skill, revisas lo que generó, apruebas o lo devuelves. Repite por las fases siguientes (referencia completa de comandos más abajo).

> Los instaladores descargan una versión etiquetada (`v0.4.7`), no el código cambiante de `main`. Puedes leer el script antes de ejecutarlo. No requiere Node.js, npm, uv, pip ni Homebrew.

## Qué incluye

- **10 skills de fase** — del descubrimiento a la operación.
- **5 skills de control** — aprobar, aceptar, consultar estado, validar trazabilidad, revertir.
- **Puertas de aprobación** — ninguna fase inicia si la anterior no está aprobada; la aprobación se invalida sola si el documento aprobado se edita después.
- **Validación de trazabilidad** — falla si un requisito no tiene criterio, una historia no tiene requisito o un criterio no tiene prueba.
- **Tres carriles** según el tamaño del cambio: `completo` (producto nuevo), `feature` (adición a un proyecto existente), `hotfix` (corrección urgente).
- **Ingesta de documentos fuente** — arranca desde manuales, formularios o planillas (PDF/Word/Excel/Markdown/imágenes) en vez de una idea en blanco; SSDD construye una matriz de trazabilidad documental con IDs de fuente y ubicaciones verificadas por SHA-256.

## Requisitos

- Python **3.9+** (lo usan los propios validadores del framework).
- Un agente compatible: Claude Code, Codex, OpenCode, Antigravity o Pi.
- **No necesitas Node.js, npm, uv, pip ni Homebrew.**
- Git es recomendable para trabajar en el proyecto, no obligatorio para instalar SSDD.

Guía detallada: [Instalación y uso paso a paso](docs/GUIA-INSTALACION-Y-USO.md).

## Instalación

Repositorio oficial: **https://github.com/jssandoval/scrum-sdd**

### Desde GitHub (recomendada)

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh

# Windows / PowerShell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

```bash
ssdd init
ssdd doctor
```

### Desde un ZIP descargado

1. Descomprime y abre una terminal **dentro de la carpeta `scrum-sdd`**.
2. Ejecuta el instalador para tu sistema operativo:

   ```bash
   sh install-cli.sh            # macOS / Linux
   ```
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install-cli.ps1   # Windows
   ```
3. Abre una **terminal nueva** y, en cualquier proyecto:

   ```bash
   cd ruta/a/mi-proyecto
   ssdd init
   ssdd doctor
   ```

`ssdd init` configura todos los agentes compatibles por defecto. Para uno específico: `ssdd init --agent claude` (también `codex`, `opencode`, `antigravity`, `pi`). En un proyecto existente nunca sobrescribe `docs/estado.json`, `CLAUDE.md`, tus documentos fuente, specs ni código.

### Comandos de la CLI

| Comando | Hace |
| --- | --- |
| `ssdd init [ruta]` | Preparar un proyecto nuevo o existente |
| `ssdd doctor` | Comprobar entorno y detectar agentes |
| `ssdd version` | Mostrar versión instalada |
| `ssdd update [ruta]` | Sincronizar recursos administrados en un proyecto |

Para actualizar la CLI global, vuelve a ejecutar `install-cli.sh` / `install-cli.ps1` desde una versión descargada más reciente — `ssdd update` no hace esto.

### Qué se crea en tu proyecto

```
mi-proyecto/
├── CLAUDE.md             # apunta a AGENTS.md
├── .claude/skills/       # los 15 skills (Claude Code)
├── .agents/skills/       # los mismos skills (Codex, OpenCode, Antigravity, Pi)
├── .opencode/commands/   # comandos de barra para OpenCode
├── .pi/prompts/          # comandos de barra para Pi
├── .framework/           # plantillas, scripts y versión
├── docs/
│   ├── 00-fuentes/       # documentación que aportas (manuales, formularios...)
│   ├── estado.json       # estado de puertas e historias
│   ├── 01-descubrimiento/ … 07-operacion/
├── specs/                # una spec por historia
├── src/
└── tests/
```

## Referencia de comandos

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
| `/ssdd-operar` | 9. Operación | SLOs, telemetría, alertas | Review y retrospectiva |

### Skills de control

| Skill | Para qué |
| --- | --- |
| `/ssdd-estado` | Ver qué fases están aprobadas, el estado de cada historia y el siguiente paso |
| `/ssdd-aprobar <fase> --por "<nombre>"` | Registrar la aprobación humana de una fase |
| `/ssdd-aceptar HU-XXX --por "<nombre>"` | Registrar la aceptación de una historia tras la UAT |
| `/ssdd-trazabilidad [HU-XXX]` | Validar la cadena requisito → criterio → historia → prueba |
| `/ssdd-revertir <fase> --por "Nombre" --motivo "Razón"` | Archivar una fase aprobada y revocar su aprobación y las posteriores |

`/ssdd-aprobar` y `/ssdd-aceptar` solo corren cuando una persona los escribe en el chat. En Claude Code y Pi el agente no puede invocarlos por su cuenta; en los demás depende de las instrucciones de `AGENTS.md`. **No es una garantía de identidad** — cualquiera con acceso a la terminal o al repositorio puede modificar el estado directamente.

### `$` vs `/`

Los ejemplos arriba usan `/`; en Codex escribe `$` en su lugar (`$ssdd-descubrir`, `$ssdd-aprobar`).

## Carriles

No todo cambio necesita las diez fases.

| Carril | Cuándo usarlo | Flujo |
| --- | --- | --- |
| `completo` | Producto nuevo | Las diez fases en orden |
| `feature` | Funcionalidad nueva en un proyecto ya instalado | `/ssdd-dercas` → `/ssdd-backlog` → `/ssdd-implementar` → `/ssdd-auditar` |
| `hotfix` | Corrección urgente | `/ssdd-implementar` (con prueba de regresión) → `/ssdd-auditar` |

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

Los scripts validan todo lo que tiene formato predecible — respeta estos identificadores:

| Elemento | Formato | Dónde |
| --- | --- | --- |
| Requisito funcional | `### RF-001 Título` + `**Prioridad:** Must` | DERCAS |
| Requisito no funcional | `### RNF-001 Título` | DERCAS |
| Regla de negocio | `### RN-001 Título` | DERCAS |
| Criterio de aceptación | `### CA-001 (RF-001) Título` | DERCAS |
| Historia de usuario | `### HU-001 Título` + `**Requisitos:** RF-001` | Product backlog |
| Prueba | El nombre o comentario de la prueba contiene `CA-001`, con aserciones reales, y la suite realmente se ejecuta | `tests/` o `src/` |

- IDs de tres dígitos, nunca reutilizados. Un requisito descartado se marca `Won't`, nunca se borra.
- Prioridad MoSCoW: `Must`, `Should`, `Could`, `Won't`.
- Sin subencabezados dentro de la sección de un ID.

## Problemas frecuentes

| Síntoma | Causa | Solución |
| --- | --- | --- |
| Un skill responde BLOQUEADO | Falta aprobar una fase anterior | `/ssdd-estado` para ver cuál, luego `/ssdd-aprobar` |
| Una fase aprobada aparece como modificada | El documento se editó después de aprobarlo | Revisar el cambio y volver a `/ssdd-aprobar` |
| `/ssdd-trazabilidad` falla | Un RF sin criterio, una historia sin RF o un criterio sin prueba | Corregir según el reporte |
| `/ssdd-aceptar` rechaza la historia | No pasó por `/ssdd-auditar` | Auditar primero, en sesión nueva |
| Los skills no aparecen al escribir `/` | El agente se abrió antes de instalar | Reiniciar el agente |
| `/ssdd-release` responde BLOQUEADO | Hay historias sin aceptar | `/ssdd-estado` y aceptar las pendientes |

## Integración continua

`/ssdd-setup` copia un workflow de GitHub Actions a `.github/workflows/ci-cd.yml`. En cada Pull Request valida trazabilidad, lint, pruebas y dependencias. El despliegue a producción exige historias aceptadas y una aprobación manual en el environment `production`. Debes configurar scripts reales de despliegue y smoke tests — si faltan, CI falla en vez de simular un despliegue.

## Actualizar

```bash
cd scrum-sdd && git pull
./install.sh /ruta/a/mi-proyecto
```

Reinstalar actualiza skills, plantillas y scripts. No toca `docs/`, `specs/`, `AGENTS.md` ni tu código.

Desde instalaciones anteriores (v0.4.7 y previas), vuelve a ejecutar el instalador remoto de arriba y luego, dentro del proyecto:

```bash
ssdd update --agent all
ssdd version
ssdd doctor
```

`ssdd update` conserva `docs/estado.json`, DERCAS, documentación fuente y código.

## Agentes soportados

El instalador deja el proyecto listo para los cinco. Los skills son los mismos; cambia dónde los busca cada agente y cómo se invocan.

| Agente | Lee los skills de | Reglas del proyecto | Invocación |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `CLAUDE.md` → `AGENTS.md` | `/ssdd-aprobar ...` |
| Codex | `.agents/skills/` | `AGENTS.md` | `$ssdd-aprobar ...` |
| OpenCode | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` |
| Antigravity y `agy` | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` |
| Pi | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` o `/skill:aprobar ...` |

- Puedes cambiar de agente a mitad del proyecto — el estado vive en `docs/estado.json`, no en el agente.
- Para auditar, usa siempre una sesión nueva si tu agente no tiene subagentes con contexto limpio.
- En Pi, los skills y plantillas del proyecto solo cargan después de marcar el proyecto como confiable.

## Documentos fuente: manuales, formularios y matrices

Puedes arrancar desde documentos existentes en vez de una idea en blanco. Copia PDF, Word, Excel, Markdown o imágenes a `docs/00-fuentes/` (`manuales/`, `lineamientos/`, `formularios/`, `matrices/`, `requerimientos/`, `otros/`), ejecuta `/ssdd-descubrir`, revisa el inventario y el análisis de contradicciones, resuelve los conflictos y aprueba. `/ssdd-dercas` construye la matriz de trazabilidad documental con IDs de fuente y ubicaciones verificables (ruta, tamaño, SHA-256).

El inventario es automático; **interpretar el contenido es trabajo del agente**. Un archivo no legible se marca como pendiente — no se inventan datos. Cambiar las fuentes después de aprobar invalida las aprobaciones de descubrimiento o requisitos correspondientes.

Guía: [Cómo usar documentos fuente](docs/USAR-DOCUMENTOS-FUENTE.md). Ejemplo completo: [Registro de clientes con manual y formulario contradictorios](examples/registro-clientes/README.md).

## La elección del stack queda en manos del programador

Durante `/ssdd-arquitectura`, el agente recomienda opciones y pide al programador elegir **frontend, backend, interoperabilidad, persistencia e infraestructura** antes de generar el ADR definitivo. La decisión queda registrada en `ADR-001-stack-tecnologico.md` y se aprueba junto con la fase.

## Revertir una fase aprobada

```text
/ssdd-revertir arquitectura --por "Nombre" --motivo "Modificar la tecnología elegida"
```

Esto guarda una copia del estado y los documentos de la fase en `docs/historico-fases/` y revoca la aprobación de esa fase y de las posteriores. Los documentos originales, el código y las historias nunca se borran — es una reversión del workflow, no un `git reset`.

## Estructura del repo

```
scrum-sdd/
├── LICENSE
├── VERSION
├── install.sh
├── constitution/     # plantilla de AGENTS.md
├── skills/           # 10 skills de fase + 4 de control
├── templates/        # DERCAS, backlog, spec de historia, ADR, auditoría
├── scripts/          # gate.py (puertas), trace.py (trazabilidad)
├── ci/               # plantilla de workflow de GitHub Actions
└── examples/         # proyecto de muestra de punta a punta
```

## Estado del proyecto

Versión 0.4.7. Incluye validación de evidencias y pruebas automáticas del propio framework. Los cinco agentes siguen pendientes de pruebas integrales en proyectos reales — issues y PRs son bienvenidos.

## Verificar el framework

```bash
python3 -m unittest discover -s tests_framework -v
```

El validador de trazabilidad hace una comprobación estructural básica — **no demuestra por sí solo** que una prueba verifica un requisito. Ejecuta siempre el test suite real, revisa su significado en `/ssdd-auditar` y bloquea el PR si falla.

## Una nota sobre la puerta de aprobación

`/ssdd-aprobar` y `/ssdd-aceptar` requieren invocación explícita por una persona en el chat, con `--por`. No hay una capa de autenticación adicional — es un control del flujo del agente, no una barrera frente a quien tenga acceso directo a los archivos o la terminal.

## Licencia

[MIT](LICENSE). Úsalo, modifícalo y distribúyelo libremente, incluso en proyectos comerciales, conservando el aviso de copyright. El instalador copia la licencia a `.framework/LICENSE` en cada proyecto para cumplir con esto.
