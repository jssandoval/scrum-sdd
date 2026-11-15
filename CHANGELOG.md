# Historial de cambios

## 0.4.6
- Actualización de CLI global y proyectos existentes con `ssdd update`; conserva archivos del usuario.
- Decisión humana obligatoria del stack (frontend, backend, interoperabilidad, persistencia, infraestructura) en `/ssdd-arquitectura`.
- Nuevo skill `/ssdd-revertir` con archivo histórico, revocación de aprobación de fase y fases siguientes y sin borrar código.
- Se conservan las 10 fases y todos los skills anteriores.

## 0.4.5 — Nombre SSDD y prefijo uniforme (15-11-2026)

- CLI `ssdd` (antes `scrum-sdd`).
- 14 skills renombrados a `ssdd-*` y referencias internas actualizadas.
- Instaladores y documentación actualizados sin cambiar metodología, validadores ni aprobaciones.
- Repositorio conservado: `jssandoval/scrum-sdd`.

## 0.4.5 — 2026-11-15

- Añadida CLI multiplataforma `scrum-sdd`: `init`, `update`, `doctor`, `version`.
- Instalación global local con un único script para macOS/Linux (`install-cli.sh`) y Windows (`install-cli.ps1`). Python 3.9+ estándar, sin pip, npm, uv o dependencias nuevas.
- Inicialización segura de proyectos nuevos o existentes; selección opcional del agente.
- Conservado el instalador Bash anterior por retrocompatibilidad.
- Nuevas pruebas de la CLI y empaquetado de versiones históricas originales disponibles.
- **Sin cambios** a fases, skills, validadores, mecanismo de aprobación, plantillas de negocio o metodología.

## 0.3.0 — 2026-11-14

- Soporte explícito a documentos fuente antes y durante descubrimiento/DERCAS.
- Inventario automático con IDs estables por ruta, tamaños y SHA-256; detección de cambios con `fuentes.py check`.
- Plantillas de análisis de fuentes y matriz de trazabilidad documental, con ubicación verificable y contradicciones.
- Actualizados skills `/ssdd-descubrir` y `/ssdd-dercas`, constitución e instalador.
- Aprobaciones de descubrimiento y requisitos invalidables ante cambios en fuentes relacionadas.
- README, guía paso a paso y ejemplo ficticio con documentos contradictorios actualizados.
- Sin cambios al mecanismo de aprobación humana por invocación explícita del skill.

# Cambios

## 0.2.0 — 2026-11-14

- Conservados `/ssdd-aprobar` y `/ssdd-aceptar` como controles de aprobación humana explícitos, sin autenticación adicional.
- Documentadas las limitaciones de esa restricción cuando el usuario tiene acceso directo a Python o al repositorio.
- Validadas transiciones HU con especificación, trazabilidad e informe de auditoría aprobado.
- Rechazadas transiciones hacia atrás o saltos de estado.
- Validación de trazabilidad más estricta: CA declarados por HU y aserciones estructurales; no se equipara esa validación con ejecutar las pruebas.
- CI/CD falla si faltan scripts de despliegue reales; no más despliegues simulados mediante `echo`.
- Cinco pruebas automatizadas del framework.
- README actualizado.

### Distribución GitHub (sin cambios de metodología)

- Instaladores remotos `install-remote.sh` y `install-remote.ps1` para `jssandoval/scrum-sdd`.
- Workflow de releases por etiqueta con pruebas y checksums SHA-256.
- `.gitignore` y guía de publicación desde el repositorio.
