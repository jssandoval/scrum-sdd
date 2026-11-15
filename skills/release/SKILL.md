---
name: release
description: 'Prepara infraestructura, pipeline y runbook, y verifica que el incremento puede ir a producción.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check release`
Exige que todas las historias registradas estén aceptadas.

## Rol
Ingeniero DevSecOps y Release Manager.

## Pasos
1. Dockerfile multi-stage con usuario no privilegiado e imagen mínima.
2. `docker-compose.prod.yml` o el equivalente del hosting definido en los ADR.
3. Verifica el workflow de CI/CD: lint, pruebas, trazabilidad, escaneo de dependencias, build, staging automático, producción con aprobación manual.
4. Runbook de despliegue paso a paso con procedimiento de rollback.
5. Notas de versión generadas desde las historias aceptadas.

## Salidas
`Dockerfile`, `docker-compose.prod.yml`, `.github/workflows/ci-cd.yml`, `docs/07-operacion/runbook.md`, `CHANGELOG.md`.

## Puerta de salida
Aprobación manual en la plataforma de CI/CD (environment `production`). El agente nunca despliega a producción.
