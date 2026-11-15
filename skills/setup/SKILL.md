---
name: setup
description: 'Inicializa el repo: constitución, linters, entorno local y prueba de humo.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check setup`
En un proyecto existente usa `--carril feature` y detecta el stack desde el repo en lugar del ADR.

## Entradas
`docs/04-arquitectura/decisiones/ADR-001-stack-tecnologico.md` y `.framework/constitution/AGENTS.md.tmpl`.

## Rol
DevOps Engineer y Tech Lead.

## Pasos
1. Genera `AGENTS.md` desde la plantilla, reemplazando los marcadores con el bloque "Stack" del ADR-001.
2. Crea la estructura de `src/` y `tests/` según las capas de la arquitectura.
3. Configura linter, formateador y git hooks del stack elegido.
4. Crea `docker-compose.yml` con la base de datos y servicios auxiliares locales.
5. Crea `specs/memory.md` vacío con sus tres secciones: decisiones, preguntas abiertas, estado.
6. Escribe una prueba de humo y ejecútala.
7. Copia `.framework/ci/ci-cd.yml` a `.github/workflows/` y ajusta los comandos. Configura `scripts/deploy-staging.sh`, `scripts/smoke-staging.sh` y `scripts/deploy-production.sh` con los destinos y secretos reales; sin estos archivos, CI falla deliberadamente.

No agregues dependencias que no estén en un ADR.

## Verificación
El proyecto compila, la prueba de humo pasa y el lint no reporta errores.

## Puerta de salida
Un desarrollador verifica en su máquina. Luego:
`/aprobar setup --por "<nombre>"`
