# SSDD v0.4.6 — Actualizar y revertir

## Actualizar desde 0.4.5
1. Actualizar la instalación global ejecutando nuevamente el instalador remoto de tu sistema o desde el paquete descargado.
2. Dentro de cada proyecto: `ssdd update --agent all`.
3. Comprobar: `ssdd version` y `ssdd doctor`.
4. Conservar los comandos antiguos instalados por migraciones anteriores, si existen: no se eliminan para no afectar personalizaciones. Utilizar `ssdd-*`.

No se borran `src/`, `tests/`, `docs/estado.json`, DERCAS ni fuentes. Se actualizan exclusivamente los archivos distribuidos por SSDD.

## Definir tecnologías
`/ssdd-arquitectura` lee el DERCAS, recomienda tecnologías en frontend/backend/interoperabilidad/persistencia/infraestructura y **se detiene para pedir la elección humana**. Documenta la decisión en ADR-001 y luego permite seguir el proceso de aprobación normal.

## Reversión
`/ssdd-revertir arquitectura --por "Persona" --motivo "Revisar ADR-001"` archiva la fase y el estado antes de revocar la aprobación de esta y las siguientes. Las historias y el código se preservan; revisar manualmente dependencias y cambios. Solo se admite por orden explícita del usuario; los scripts no pueden autenticar identidades.

Histórico: `docs/historico-fases/<fecha>-<fase>-<id>/`.
