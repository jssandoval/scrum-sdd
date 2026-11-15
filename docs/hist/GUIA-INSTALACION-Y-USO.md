> En la versión 0.4.7, los comandos de agente llevan prefijo `ssdd-` y la CLI se ejecuta como `ssdd`.

# Instalación y uso de SSDD (Scrum-SDD) v0.4.5

## Instalar SSDD (Scrum-SDD) (una sola vez por equipo)

Descarga y descomprime `scrum-sdd-v0.4.5.zip` y abre una terminal en la carpeta `scrum-sdd`.

**macOS o Linux:**

```bash
sh install-cli.sh
```

**Windows con PowerShell:**

```powershell
powershell -ExecutionPolicy Bypass -File .\install-cli.ps1
```

**Requisito único del framework:** Python 3.9+ y un agente de programación. No necesitas npm, uv, Homebrew, Git para la instalación ni paquetes adicionales. Abre una terminal nueva después de instalar (el instalador configura el PATH del usuario).

## Inicializar proyectos

Entra a la carpeta de tu aplicación, nueva o existente:

```bash
ssdd init
ssdd doctor
```

Se instala la integración de todos los agentes por defecto. Opcionalmente `ssdd init --agent claude` instala solo esa integración. También se aceptan rutas, por ejemplo `ssdd init ./mi-proyecto`.

Actualiza recursos instalados de un proyecto con `ssdd update`. Para actualizar la **CLI global** descomprime la nueva versión y vuelve a ejecutar su instalador.

**Seguridad de datos:** `init` conserva los documentos fuente, `docs/estado.json`, `AGENTS.md`, `CLAUDE.md`, specs, código y tests del proyecto. `update` reemplaza archivos del framework administrados por él; si personalizaste directamente los skills, respáldalos antes. El mecanismo de aprobación no cambia.

## Uso de los skills

Abre tu agente desde el proyecto. Usa `/ssdd-descubrir <idea>` (Codex `$ssdd-descubrir`), revisa documentos, aprueba con `/ssdd-aprobar descubrimiento --por "Nombre"` y sigue el ciclo DERCAS → diseño → arquitectura → backlog → setup → implementación → auditoría → release → operación, tal como se explica a continuación.

---

## Instrucciones históricas de instalación (v0.3.0, reemplazadas en v0.4.5)

Las instrucciones de instalación que siguen se conservan como referencia histórica. **Para instalar v0.4.5, utiliza los pasos anteriores.**

# Guía de instalación y uso — SSDD (Scrum-SDD) v0.3.0

Esta guía explica cómo instalar el framework en un proyecto, iniciar un desarrollo nuevo, trabajar por historias y usarlo en un sistema existente. Los ejemplos usan **Claude Code** en macOS o Linux. En Windows, utiliza **Git Bash** para ejecutar `install.sh`.

## 1. Qué hace el framework

SSDD (Scrum-SDD) organiza el desarrollo en: **descubrimiento → requisitos DERCAS → diseño → arquitectura → backlog → configuración → implementación por historia → auditoría → release → operación**.

Los agentes generan artefactos, código y pruebas; el usuario revisa y aprueba las fases y acepta las historias. Las aprobaciones de fases caducan cuando cambia el archivo controlado por su hash. Esta restricción es de flujo de trabajo: **no autentica a una persona ni impide modificar el estado con acceso directo al sistema de archivos**.

## 2. Requisitos previos

- Python 3.9 o superior.
- Git y Bash.
- Al menos uno de los agentes: Claude Code, Codex, OpenCode, Antigravity o Pi, instalado y configurado.

Comprueba en la terminal:

```bash
python3 --version
git --version
bash --version
claude --version
```

Si utilizas otro agente, cambia la última línea por `codex --version`, `opencode --version` o el comando correspondiente.

## 3. Descargar y organizar carpetas

Descarga `scrum-sdd-v0.3.0.zip`, descomprímelo y coloca su carpeta `scrum-sdd` dentro de `~/proyectos/`:

```text
~/proyectos/
├── scrum-sdd/         # Framework (contiene install.sh)
└── mi-primera-app/    # Tu proyecto de software
```

Puedes crear los directorios desde una terminal:

```bash
mkdir -p ~/proyectos/mi-primera-app
```

> Si tienes `scrum-sdd` en otra ubicación, sustituye `~/proyectos/scrum-sdd` por su ruta real.

## 4. Instalar en tu proyecto

Desde una terminal:

```bash
bash "$HOME/proyectos/scrum-sdd/install.sh" "$HOME/proyectos/mi-primera-app"
```

El instalador crea `.claude/skills/`, `.agents/skills/`, envoltorios para OpenCode y Pi, `.framework/`, `docs/`, `specs/`, `src/`, `tests/` y `CLAUDE.md`. **No genera la aplicación todavía**; eso se hace en `/ssdd-setup`.

Abre el directorio del proyecto con tu agente:

```bash
cd ~/proyectos/mi-primera-app
claude
```

Si ya tenías abierta la sesión del agente, ciérrala y vuelve a abrirla para cargar los skills.

**Importante:** a partir de este punto, los comandos con `/` se introducen **dentro del chat del agente**, no en Bash. En Codex se invocan mediante `$nombre` o el selector de skills.

## 4.1. Opcional: incluir documentación existente

Antes de abrir el agente, copia documentos a estas carpetas dentro del proyecto instalado:

```text
docs/00-fuentes/
├── manuales/          # PDF, Word, Markdown
├── lineamientos/      # normas, políticas, procedimientos
├── formularios/       # formatos de captura
├── matrices/          # Excel, CSV
├── requerimientos/    # TDR, especificaciones previas
└── otros/             # diagramas, imágenes, anexos
```

El skill `/ssdd-descubrir` los inventaría e intenta leer su contenido; entrega evidencia exacta y contradicciones. Revisa `docs/01-descubrimiento/analisis-fuentes.md` antes de aprobar. `/ssdd-dercas` vuelve a consultar fuentes y prepara `docs/02-requisitos/matriz-trazabilidad-documental.md`, con referencias por documento, página/hoja/sección. Si una fuente es ilegible, no se inventa su contenido.

Consulta [Uso de documentos fuente](USAR-DOCUMENTOS-FUENTE.md) y el [ejemplo de registro de clientes](../examples/registro-clientes/README.md). Si no tienes archivos, puedes trabajar únicamente con la idea.

## 5. Proyecto nuevo: recorrer las primeras seis fases

Ejemplo: un SaaS para gestionar citas en clínicas pequeñas. Ejecuta un skill por vez. Después de cada fase revisa los archivos generados y solamente entonces aprueba.

### Fase 0: descubrimiento

Dentro de Claude Code:

```text
/ssdd-descubrir Quiero desarrollar un SaaS para que pequeñas clínicas gestionen citas, pacientes y recordatorios.
```

Revisa `docs/01-descubrimiento/` (visión, problema, Lean Canvas e hipótesis). Si estás de acuerdo:

```text
/ssdd-aprobar descubrimiento --por "Tu Nombre"
```

### Fase 1: requisitos

```text
/ssdd-dercas
```

Revisa `docs/02-requisitos/DERCAS.md`, incluidos RF, RNF, RN y CA:

```text
/ssdd-aprobar requisitos --por "Tu Nombre"
```

### Fase 2: diseño

```text
/ssdd-diseno
```

Revisa flujos, design system e inventario en `docs/03-diseno/`:

```text
/ssdd-aprobar diseno --por "Tu Nombre"
```

### Fase 3: arquitectura

```text
/ssdd-arquitectura
```

Revisa los diagramas, modelo de datos, API, seguridad y ADR en `docs/04-arquitectura/`. Aquí se decide y justifica el stack tecnológico.

```text
/ssdd-aprobar arquitectura --por "Tu Nombre"
```

### Fase 4: planificación Scrum

```text
/ssdd-backlog
```

Revisa `docs/05-scrum/`: épicas, historias, Definition of Ready, Definition of Done y Sprint 1.

```text
/ssdd-aprobar backlog --por "Tu Nombre"
```

### Fase 5: entorno de desarrollo

```text
/ssdd-setup
```

El agente genera `AGENTS.md` y configura estructura, herramientas, pruebas iniciales y CI según la arquitectura aprobada. Comprueba que el proyecto compile y pasen las verificaciones.

```text
/ssdd-aprobar setup --por "Tu Nombre"
```

## 6. Implementar y aceptar historias

Para cada historia del sprint sigue este ciclo dentro del agente:

**1. Implementar una historia:**

```text
/ssdd-implementar HU-001
```

El agente ejecuta Specify → Clarify → Plan → Tasks → Implement → Converge. Puede detenerse para resolver contradicciones o confirmar el plan. La implementación debe incluir pruebas que comprueben sus criterios de aceptación.

**2. Auditar de manera independiente:**

```text
/clear
/ssdd-auditar HU-001
```

`/clear` es un comando de Claude Code para limpiar el contexto; como alternativa abre una sesión nueva. Corrige hallazgos críticos o altos y vuelve a auditar cuando corresponda.

**3. Aceptar la historia:**

Tras revisar y probar personalmente el resultado (UAT):

```text
/ssdd-aceptar HU-001 --por "Tu Nombre"
```

Repite para `HU-002`, `HU-003`, etc. El agente **no debe registrar su propia aceptación**.

## 7. Release y operación

Cuando las historias del incremento estén aceptadas:

```text
/ssdd-release
```

Revisa el Dockerfile, la configuración de CI/CD, el runbook, las notas de versión, secretos y entorno de destino. **El despliegue real depende de configurar infraestructura y credenciales; el framework no sustituye esa configuración.** La autorización de producción se realiza en la plataforma CI/CD.

Después de comprobar un despliegue en producción:

```text
/ssdd-operar
```

Esto documenta SLO/SLA, registros, métricas, alertas y postmortems.

## 8. Consultar estado y trazabilidad

Dentro del agente:

```text
/ssdd-estado
/ssdd-trazabilidad
/ssdd-trazabilidad HU-001
```

- `/ssdd-estado`: muestra fases aprobadas, estados de historias y aprobaciones vencidas.
- `/ssdd-trazabilidad`: valida asociaciones RF → CA → HU → pruebas.
- `/ssdd-trazabilidad HU-001`: comprueba los criterios asociados a la historia indicada.

Si un control se bloquea, revisa el motivo que devuelve el agente y corrige la fase o evidencia correspondiente; no edites `docs/estado.json` manualmente.

## 9. Instalarlo en una aplicación existente

Desde Bash:

```bash
bash "$HOME/proyectos/scrum-sdd/install.sh" "$HOME/proyectos/mi-sistema-existente"
cd ~/proyectos/mi-sistema-existente
claude
```

Dentro del agente, usa el carril `feature` para comenzar a documentar el sistema y preparar su entorno:

```text
/ssdd-dercas
/ssdd-aprobar requisitos --por "Tu Nombre" --carril feature
/ssdd-setup
/ssdd-aprobar setup --por "Tu Nombre" --carril feature
```

Para una funcionalidad nueva, documenta el cambio, mantenlo en el backlog e impleméntalo por historia. Para una corrección urgente, usa el carril `hotfix`:

```text
/ssdd-implementar HU-042 --carril hotfix
```

Un hotfix exige una prueba de regresión y auditoría.

## 10. Otros agentes

| Agente | Inicio habitual | Invocación de ejemplo |
| --- | --- | --- |
| Claude Code | `claude` | `/ssdd-descubrir` |
| Codex | `codex` | `$ssdd-descubrir` o selector de skills |
| OpenCode | `opencode` | `/ssdd-descubrir` |
| Pi | `pi` | `/ssdd-descubrir` o `/skill:descubrir` |
| Antigravity | Interfaz o CLI disponible | `/ssdd-descubrir` (según integración) |

El instalador crea integraciones para estos agentes, pero la disponibilidad y las restricciones exactas dependen de sus versiones. Valida los comandos en tu instalación.

## 11. Ejecutar las pruebas del framework

Desde una **terminal**, no dentro del agente:

```bash
cd ~/proyectos/scrum-sdd
python3 -m unittest discover -s tests_framework -v
```

Estas son las pruebas del framework; además deben pasar las pruebas de cada aplicación creada con él.

## 12. Actualizar un proyecto

Descomprime la versión nueva del framework sobre su carpeta y ejecuta nuevamente:

```bash
bash "$HOME/proyectos/scrum-sdd/install.sh" "$HOME/proyectos/mi-primera-app"
```

Se vuelven a copiar scripts, skills y plantillas. El instalador conserva `docs/`, `specs/`, `AGENTS.md` y el código de tu aplicación. Antes de actualizar, guarda cambios en Git.

## 13. Problemas habituales

| Problema | Qué hacer |
| --- | --- |
| No aparece `/ssdd-descubrir` | Reinicia el agente desde la carpeta del proyecto y verifica la instalación |
| Aparece `BLOQUEADO` | Ejecuta `/ssdd-estado`; revisa aprobaciones y artefactos pendientes |
| Una aprobación caducó | Revisa los cambios del documento y vuelve a ejecutar `/ssdd-aprobar` |
| Falla `/ssdd-trazabilidad` | Corrige las referencias o pruebas y vuelve a ejecutar el comando |
| No se acepta `HU-001` | Completa implementación, auditoría y aceptación humana en orden |
| `/ssdd-release` no avanza | Verifica historias aceptadas y controles del carril |

## 14. Resumen del flujo

```text
IDEA
  ↓ /ssdd-descubrir      → /ssdd-aprobar descubrimiento
  ↓ /ssdd-dercas         → /ssdd-aprobar requisitos
  ↓ /ssdd-diseno         → /ssdd-aprobar diseno
  ↓ /ssdd-arquitectura   → /ssdd-aprobar arquitectura
  ↓ /ssdd-backlog        → /ssdd-aprobar backlog
  ↓ /ssdd-setup          → /ssdd-aprobar setup
  ↓ /ssdd-implementar HU-001
  ↓ /ssdd-auditar HU-001 (contexto independiente)
  ↓ /ssdd-aceptar HU-001 (persona, tras UAT)
  ↓ Repetir por historia
  ↓ /ssdd-release        → autorización de producción en CI/CD
  ↓ /ssdd-operar
```

**Nota de seguridad:** las restricciones de invocación humana de `/ssdd-aprobar` y `/ssdd-aceptar` funcionan como instrucciones/integraciones de los agentes, no como autenticación fuerte. No se debe presentar el archivo de estado local como prueba criptográfica de identidad.


## Actualizar la instalación y un proyecto existente (v0.4.7)

En macOS/Linux y Windows, ejecuta de nuevo el instalador global desde el paquete o GitHub (cuando la etiqueta v0.4.7 esté publicada). Abre otra terminal; desde el directorio de tu proyecto:

```bash
ssdd update
ssdd version
ssdd doctor
```

`ssdd update` actualiza scripts y skills administrados, **sin borrar** documentos, estados de aprobación, fuentes ni código. Cierra y vuelve a abrir el agente para cargar `ssdd-revertir`.

## La decisión del stack es del programador

En `/ssdd-arquitectura` el agente consulta qué quieres utilizar en frontend, backend, interoperabilidad, persistencia e infraestructura; muestra recomendaciones comparadas y se detiene para que elijas. Guarda las elecciones en ADR-001 antes de generar el diseño definitivo. No acepta el silencio como aprobación.

## Deshacer la aprobación de una fase

```text
/ssdd-revertir arquitectura --por "Nombre" --motivo "Deseo cambiar el stack"
```

Archiva documentos de la fase y el estado previo en `docs/historico-fases/`, revoca la aprobación de esa fase y las posteriores y deja el trabajo original intacto para revisión. No revierte commits ni borra historias o código. Vuelve a ejecutar `/ssdd-arquitectura` y luego `/ssdd-aprobar arquitectura --por "Nombre"`.


## Arquitectura integral y reversión en SSDD 0.4.7

Ejecuta `/ssdd-arquitectura`. El agente lee requisitos y necesidades y propone todas las decisiones técnicas que correspondan: UI y estilos, frontend, backend, interfaces de integración, bases de datos, almacenamiento, seguridad, colas y procesamiento asíncrono, caché, CI/CD, hosting, observabilidad, respaldo y otros. Explica cada propuesta, consulta tu decisión por componente y se detiene. Tú puedes aceptar todas sus recomendaciones o modificar las que necesites. Registra lo decidido en `propuesta-componentes.md` y ADR.

Para revertir una fase terminada tienes dos variantes:

```text
/ssdd-revertir arquitectura --modo aprobacion --por "Persona" --motivo "Modificar ADR"
/ssdd-revertir arquitectura --modo paso --por "Persona" --motivo "Rehacer desde cero"
```

`aprobacion` guarda histórico y retira aprobaciones sin borrar documentos. `paso` requiere una **confirmación explícita de eliminación**, archiva documentos y estado, comprueba el respaldo y retira únicamente entregables activos de esa fase. Ambas requieren revisar nuevamente las fases posteriores antes de aprobarlas. Ninguna opción borra código ni revierte Git.
