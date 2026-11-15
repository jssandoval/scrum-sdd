# Manual de instalación, comandos y flujo de trabajo de SSDD

**Versión de referencia:** SSDD 0.4.7  
**Nombre completo:** Scrum Spec-Driven Development (SSDD)  
**Repositorio:** https://github.com/jssandoval/scrum-sdd

Este manual se puede incorporar tal cual en `docs/MANUAL-SSDD.md` del repositorio. Explica los comandos vigentes, los nombres de versiones anteriores y cómo utilizar cada fase.

## 1. Distinguir dos tipos de comandos

- **Comandos de terminal:** `ssdd init`, `ssdd update`, `ssdd doctor` y `ssdd version` se ejecutan en Terminal, PowerShell o la consola de tu sistema.
- **Skills del agente:** `/ssdd-descubrir`, `/ssdd-dercas`, etc. se ejecutan **dentro del agente de programación** (Claude Code, OpenCode, Antigravity o Pi). En Codex normalmente se invocan con `$`, por ejemplo `$ssdd-descubrir`.

> **Compatibilidad de nombres:** `scrum-sdd init` y los skills sin prefijo (por ejemplo `/descubrir`) pertenecen a versiones anteriores. En SSDD 0.4.7 la CLI se llama `ssdd` y **los skills instalados llevan prefijo `ssdd-`**. No asumas que los comandos antiguos continúan disponibles tras instalar o actualizar; podrían existir solo como restos de una instalación antigua.

## 2. Instalación

**Requisitos:** Python 3.9 o superior y un agente de programación compatible. No se exige instalar Node.js, npm, uv, pip ni paquetes adicionales para SSDD. Git es recomendable para versionar el proyecto.

### 2.1. Desde el repositorio publicado

En macOS o Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh
```

En Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

Estos comandos requieren que el repositorio y el Release de la versión indicada por el instalador remoto estén publicados y accesibles. Para revisar el código antes de ejecutarlo, descarga los scripts y examínalos.

### 2.2. Desde un ZIP descargado

Descomprime el paquete de SSDD y abre una terminal dentro de su carpeta:

macOS / Linux:

```bash
sh install-cli.sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\install-cli.ps1
```

Abre una terminal nueva para que encuentre el ejecutable `ssdd`.

### 2.3. Inicializar un proyecto

```bash
cd /ruta/a/mi-proyecto
ssdd init
ssdd doctor
```

Para instalar solo la integración de Claude Code:

```bash
ssdd init --agent claude
```

Agentes admitidos por el inicializador: `claude`, `codex`, `opencode`, `antigravity`, `pi`, `all` (predeterminado). El comando `init` funciona tanto en proyectos nuevos como existentes y busca conservar el código y los documentos del proyecto.

## 3. Comandos de terminal: nombres antiguos y actuales

| Comando | Disponibilidad | Qué hace | Ejemplo |
| --- | --- | --- | --- |
| `scrum-sdd init` | **Antiguo** (CLI anterior al cambio de nombre) | Inicializaba un proyecto con el framework | Sustituir por `ssdd init` |
| `ssdd init` | **Vigente** | Instala skills, plantillas, validadores y estructura SSDD en un proyecto | `ssdd init` o `ssdd init ./mi-proyecto --agent claude` |
| `ssdd doctor` | **Vigente** | Verifica el entorno y detecta agentes disponibles | `ssdd doctor` |
| `ssdd version` | **Vigente** | Muestra la versión de la CLI instalada | `ssdd version` |
| `ssdd update` | **Vigente** | Actualiza los archivos administrados por SSDD dentro de un proyecto | `ssdd update` o `ssdd update ./mi-proyecto` |

**Atención a las actualizaciones:** `ssdd update` **no descarga** una nueva versión de Internet ni actualiza la CLI global. Primero instala la versión nueva de la CLI (instalador remoto publicado o `install-cli.sh` / `install-cli.ps1` de un paquete descargado); luego ejecuta `ssdd update` en cada proyecto.

## 4. Tabla de equivalencias de skills

Los nombres de la columna izquierda son **históricos**, no alias garantizados de la versión actual.

| Skill antiguo | Skill vigente | Para qué sirve |
| --- | --- | --- |
| `/descubrir` | `/ssdd-descubrir` | Descubrimiento e investigación de fuentes |
| `/dercas` | `/ssdd-dercas` | Redacción del DERCAS y requisitos trazables |
| `/diseno` | `/ssdd-diseno` | Procesos, navegación, UX/UI y pantallas |
| `/arquitectura` | `/ssdd-arquitectura` | Propuestas técnicas, decisiones del desarrollador y ADR |
| `/backlog` | `/ssdd-backlog` | Épicas, historias, prioridades y sprints |
| `/setup` | `/ssdd-setup` | Preparación del proyecto y CI |
| `/implementar` | `/ssdd-implementar` | Implementación de una historia con SDD/TDD |
| `/auditar` | `/ssdd-auditar` | Revisión independiente de código y seguridad |
| `/aprobar` | `/ssdd-aprobar` | Aprobación humana de una fase |
| `/aceptar` | `/ssdd-aceptar` | Aceptación humana de una historia |
| `/estado` | `/ssdd-estado` | Consulta de estado del proceso |
| `/trazabilidad` | `/ssdd-trazabilidad` | Verificación RF → CA → HU → prueba |
| `/release` | `/ssdd-release` | Preparación de despliegue y entrega |
| `/operar` | `/ssdd-operar` | Monitoreo, SLO y operación |
| *(no existía)* | `/ssdd-revertir` | Revocar aprobación o retirar una fase con respaldo |

## 5. Explicación de cada skill (antiguo y vigente)

### 5.1. `/descubrir` → `/ssdd-descubrir`

**Cuándo:** al iniciar una idea o investigar un sistema existente. **Entradas:** la idea y, si existen, manuales, formularios, matrices, normas o requerimientos en `docs/00-fuentes/`. **Acciones:** inventaría las fuentes, diferencia hechos de hipótesis, descubre procesos y actores, formula preguntas y detecta contradicciones. **Salidas:** `docs/01-descubrimiento/`, incluyendo visión del producto, análisis de fuentes y Lean Canvas.

```text
/ssdd-descubrir Quiero desarrollar un sistema para administrar inventario de ferreterías.
```

Si no tienes archivos fuente, **no falla solo por estar vacía la carpeta**: continúa con la idea, documentando la ausencia de fuentes. El siguiente paso es revisar la propuesta y aprobar descubrimiento.

### 5.2. `/dercas` → `/ssdd-dercas`

**Cuándo:** después de aprobar descubrimiento. **Entradas:** resultados anteriores y documentos fuente originales. **Acciones:** formula requisitos funcionales (RF), no funcionales (RNF), reglas de negocio (RN) y criterios de aceptación (CA); relaciona requisitos con la evidencia y registra vacíos o contradicciones. **Salidas:** `docs/02-requisitos/DERCAS.md` y matriz de trazabilidad documental.

```text
/ssdd-dercas
```

Revisa ambigüedades y aprueba requisitos antes de avanzar.

### 5.3. `/diseno` → `/ssdd-diseno`

**Cuándo:** tras aprobar requisitos. **Acciones:** diseña procesos BPMN, flujos, navegación, sistema visual accesible e inventario de pantallas, sin escribir aún la aplicación. **Salidas:** `docs/03-diseno/`.

```text
/ssdd-diseno
```

### 5.4. `/arquitectura` → `/ssdd-arquitectura`

**Cuándo:** tras aprobar diseño. **Acciones:** revisa los RF/RNF y propone **todos los componentes técnicos pertinentes**, no solo frontend y backend: estilos (por ejemplo Tailwind CSS cuando convenga), persistencia, autenticación, autorizaciones, APIs, interoperabilidad, caché, colas/eventos, tareas asíncronas, almacenamiento, infraestructura, seguridad, pruebas, observabilidad y más según necesidad.

Para cada componente explica por qué aplica o no aplica, alternativas, recomendación y riesgos. **El programador confirma o modifica las elecciones antes de continuar.** El agente registra esas decisiones y genera arquitectura C4, modelo de datos, contratos y ADR. **Salidas:** `docs/04-arquitectura/`.

```text
/ssdd-arquitectura
```

La aprobación formal de la fase es un comando **separado**: `/ssdd-aprobar arquitectura --por "Nombre"`.

### 5.5. `/backlog` → `/ssdd-backlog`

**Cuándo:** después de aprobar arquitectura. **Acciones:** convierte requisitos en épicas e historias de usuario, prioriza el MVP, divide historias grandes y prepara el primer sprint. **Salidas:** `docs/05-scrum/`, con backlog, Definition of Ready, Definition of Done y sprint.

```text
/ssdd-backlog
```

### 5.6. `/setup` → `/ssdd-setup`

**Cuándo:** después de aprobar el backlog. **Acciones:** genera/configura `AGENTS.md` desde el stack aprobado, prepara estructura de código, pruebas, lint, dependencias justificadas y CI. **Salidas:** base técnica del proyecto y pruebas de humo.

```text
/ssdd-setup
```

**No confundir** `/ssdd-setup` (skill dentro del agente) con `ssdd init` (CLI para instalar SSDD en el proyecto).

### 5.7. `/implementar` → `/ssdd-implementar`

**Cuándo:** cuando la historia está lista en el sprint. **Acciones:** ejecuta una historia mediante Specify → Clarify → Plan → Tasks → Implement → Converge, pruebas primero y revisión de criterios. **Salidas:** `specs/HU-XXX.md`, cambios de código y pruebas.

```text
/ssdd-implementar HU-001
```

Para una corrección urgente en proyecto preparado:

```text
/ssdd-implementar HU-042 --carril hotfix
```

### 5.8. `/auditar` → `/ssdd-auditar`

**Cuándo:** después de implementar una historia. **Acciones:** revisión independiente de cobertura, arquitectura, seguridad y flujo E2E; clasifica hallazgos. **Salida:** informe en `docs/06-pruebas/`. El auditor no debe ser el mismo contexto que implementó el código.

```text
/clear
/ssdd-auditar HU-001
```

`/clear` es un ejemplo para agentes que lo soporten: también puedes iniciar una sesión nueva o usar un subagente con contexto limpio. No es un skill SSDD.

### 5.9. `/aprobar` → `/ssdd-aprobar`

**Cuándo:** únicamente cuando una persona revisó y autoriza el cierre de una fase. **Acción:** registra nombre, fecha y huella del artefacto; las modificaciones posteriores invalidan su aprobación. **No equivale** a aprobar una historia.

```text
/ssdd-aprobar descubrimiento --por "Nombre Apellido"
/ssdd-aprobar requisitos --por "Nombre Apellido"
/ssdd-aprobar diseno --por "Nombre Apellido"
/ssdd-aprobar arquitectura --por "Nombre Apellido"
/ssdd-aprobar backlog --por "Nombre Apellido"
/ssdd-aprobar setup --por "Nombre Apellido"
```

Solo el humano debe invocar este skill; la regla del agente no sustituye autenticación técnica del sistema operativo.

### 5.10. `/aceptar` → `/ssdd-aceptar`

**Cuándo:** después de auditar una historia y realizar la prueba de aceptación del Product Owner. **Acción:** registra la aceptación humana de esa HU.

```text
/ssdd-aceptar HU-001 --por "Nombre Apellido"
```

### 5.11. `/estado` → `/ssdd-estado`

**Cuándo:** en cualquier momento para consultar el progreso. **Acción:** muestra fases aprobadas, historias en curso y pasos pendientes, sin modificar archivos.

```text
/ssdd-estado
```

### 5.12. `/trazabilidad` → `/ssdd-trazabilidad`

**Cuándo:** al verificar la cadena de requisitos o antes de cerrar una historia. **Acción:** valida referencias RF → CA → HU → pruebas. Una coincidencia de ID no garantiza por sí sola que la prueba sea funcionalmente suficiente; la auditoría debe revisarla.

```text
/ssdd-trazabilidad
/ssdd-trazabilidad HU-001
```

### 5.13. `/release` → `/ssdd-release`

**Cuándo:** cuando las historias del incremento están aceptadas. **Acciones:** prepara contenedores, pipeline, verificación de staging, notas de versión y runbook. **No implica** despliegue automático a producción sin configuración y aprobación externa.

```text
/ssdd-release
```

### 5.14. `/operar` → `/ssdd-operar`

**Cuándo:** después del primer despliegue de producción. **Acciones:** SLO/SLA, logs, métricas, alertas, respuesta ante incidentes y realimentación al backlog.

```text
/ssdd-operar
```

### 5.15. Skill adicional: `/ssdd-revertir`

**Cuándo:** necesitas rehacer una fase ya aprobada. Permite dos alternativas:

1. **Solo quitar aprobación (`--modo aprobacion`)**: conserva los documentos; archiva la fase y el estado previo; revoca su aprobación y las posteriores.
2. **Eliminar el paso (`--modo paso`)**: primero muestra qué retirará, solicita **confirmación humana adicional explícita**, verifica el respaldo y solo entonces retira los entregables activos de esa fase. No borra el código, las fuentes ni documentos de otras fases.

```text
/ssdd-revertir arquitectura --modo aprobacion --por "Nombre Apellido" --motivo "Revisar decisiones"
/ssdd-revertir arquitectura --modo paso --por "Nombre Apellido" --motivo "Rehacer desde cero"
```

Los respaldos se almacenan en `docs/historico-fases/`. Esto **no revierte commits Git** ni restaura automáticamente copias anteriores. Eliminar una fase aprobada puede obligar a revisar fases posteriores.

## 6. Flujo completo de ejemplo

Este ejemplo emplea **solo comandos vigentes**, escritos dentro del agente salvo que se indique lo contrario:

```bash
# En la terminal del sistema, una vez instalada la CLI
cd /ruta/a/mi-proyecto
ssdd init
ssdd doctor
```

```text
# Dentro del agente de programación
/ssdd-descubrir Un SaaS para reservas de servicios
/ssdd-aprobar descubrimiento --por "Nombre Apellido"
/ssdd-dercas
/ssdd-aprobar requisitos --por "Nombre Apellido"
/ssdd-diseno
/ssdd-aprobar diseno --por "Nombre Apellido"
/ssdd-arquitectura
# Revisar y contestar las propuestas técnicas; después:
/ssdd-aprobar arquitectura --por "Nombre Apellido"
/ssdd-backlog
/ssdd-aprobar backlog --por "Nombre Apellido"
/ssdd-setup
/ssdd-aprobar setup --por "Nombre Apellido"
/ssdd-implementar HU-001
# Abrir sesión nueva o contexto independiente
/ssdd-auditar HU-001
/ssdd-aceptar HU-001 --por "Nombre Apellido"
/ssdd-estado
/ssdd-trazabilidad HU-001
/ssdd-release
# Tras desplegar y comprobar producción:
/ssdd-operar
```

**Importante:** no ejecutes las aprobaciones automáticamente en bloque. Cada una requiere revisar lo generado, atender preguntas y tomar la decisión humana antes de avanzar. El agente puede detenerse para aclaraciones o correcciones.

## 7. Documentos fuente: con archivos y sin archivos

Para iniciar desde manuales, normas, formularios, matrices y requisitos, colócalos en la ruta de tu proyecto:

```text
docs/00-fuentes/
├── manuales/
├── lineamientos/
├── formularios/
├── matrices/
├── requerimientos/
└── otros/
```

Ejecuta `/ssdd-descubrir`, revisa la cobertura de lectura y después `/ssdd-dercas` una vez aprobado descubrimiento. Si no aportas documentos, SSDD trabaja con tu idea y preguntas de aclaración. La disponibilidad de lectura de PDF, Excel, Word o imágenes depende de las herramientas del agente.

## 8. Problemas frecuentes

| Problema | Solución |
| --- | --- |
| `ssdd: command not found` | Reabre la terminal después de instalar la CLI; comprueba que la carpeta de instalación esté en PATH. |
| `/ssdd-descubrir` no aparece | Ejecuta `ssdd init` en ese proyecto y reinicia el agente. |
| Solo veo `/descubrir` | Es una instalación antigua; instala la CLI actual y ejecuta `ssdd update` en el proyecto. |
| `ssdd update` no cambia la versión global | Actualiza primero la CLI con el nuevo instalador, luego actualiza el proyecto. |
| Un paso aparece BLOQUEADO | Consulta `/ssdd-estado` y revisa qué fase exige aprobación o qué artefacto cambió. |
| Quiero rehacer una decisión sin perder archivos | Usa `/ssdd-revertir <fase> --modo aprobacion ...`. |
| Quiero retirar una fase y rehacer documentos | Usa `/ssdd-revertir <fase> --modo paso ...`, confirma expresamente y comprueba el respaldo. |
| Cambié de agente | Abre el mismo proyecto actualizado; los agentes comparten documentos y estado en disco, no conversaciones internas. |

## 9. Alcance de la documentación

Este manual describe SSDD **v0.4.7**. Los comandos anteriores se muestran por compatibilidad histórica, no como garantía de ejecución. No modifica automáticamente la instalación ni el contenido del repositorio: copia el directorio `docs/` de este paquete en la raíz del repositorio SSDD.
