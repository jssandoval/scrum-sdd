---
name: backlog
description: 'Descompone el DERCAS en épicas e historias INVEST y prepara el Sprint Planning.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check backlog`

## Entradas
DERCAS, `docs/04-arquitectura/` y la plantilla `.framework/templates/product-backlog.md`.

## Rol
Product Owner y Scrum Master certificados.

## Pasos
1. Organiza el trabajo en épicas e historias priorizadas para el MVP.
2. Escribe cada historia con la plantilla: ID, historia, RF, CA, puntos, pantalla, API, dependencias.
3. Divide con INVEST toda historia de más de 3 puntos.
4. Elabora el story map y marca la línea de corte del Sprint 1 como una rebanada vertical funcional.
5. Documenta la Definition of Ready y la Definition of Done.
6. Propón el Sprint 1 en `sprints/sprint-01.md`: objetivo, historias, capacidad.

## Salidas
En `docs/05-scrum/`: `product-backlog.md`, `story-map.md`, `definition-of-ready.md`, `definition-of-done.md`, `sprints/sprint-01.md`.

## Verificación
`python3 .framework/scripts/trace.py` en OK: todo RF Must cubierto por una historia.

## Puerta de salida
En el Sprint Planning el equipo fija el Sprint Goal y el Sprint Backlog. Luego:
`/aprobar backlog --por "<nombre>"`
