# Migrar de Scrum-SDD 0.4.0 a SSDD 0.4.5

No se modificaron la metodología, las diez fases, las aprobaciones humanas, los estados ni la estructura documental.

## Cambios de comandos

- CLI anterior: `scrum-sdd init`, `scrum-sdd doctor`, `scrum-sdd update`.
- CLI nueva: `ssdd init`, `ssdd doctor`, `ssdd update`.
- Skill anterior: `/descubrir`, `/dercas`, `/aprobar`, `/aceptar`, etc.
- Skill nuevo: `/ssdd-descubrir`, `/ssdd-dercas`, `/ssdd-aprobar`, `/ssdd-aceptar`, etc. (en Codex usar `$ssdd-...`).

El repositorio sigue alojado en `https://github.com/jssandoval/scrum-sdd`, por lo que no es necesario renombrarlo.

## Instalación

Instala SSDD 0.4.5 sobre la versión anterior con el instalador local o remoto publicado en GitHub. En el directorio de un proyecto existente ejecuta `ssdd update`.

**Compatibilidad:** `update` instala los skills prefijados y no elimina automáticamente los comandos antiguos personalizados. Si anteriormente instalaste 0.4.0, elimina manualmente las carpetas anteriores sin prefijo de `.claude/skills/` y `.agents/skills/` y los archivos antiguos de `.opencode/commands/` y `.pi/prompts/` si quieres evitar comandos duplicados. No borres archivos de usuario ni el estado `docs/estado.json`.

**Publicación:** cambia los enlaces de instalación del README solo cuando exista el tag `v0.4.5` en GitHub. `SSDD_VERSION=v0.4.5` permite elegir la versión remota.
