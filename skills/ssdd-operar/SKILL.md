---
name: ssdd-operar
description: 'Define SLOs, telemetría, alertas y postmortems, y convierte la telemetría en ítems de backlog.'
---

## Puerta de entrada
Existe al menos un despliegue en producción.

## Rol
Site Reliability Engineer.

## Pasos
1. Define SLO y SLA de latencia, tasa de error y disponibilidad, derivados de los RNF.
2. Configura telemetría: logs JSON estructurados y métricas de las cuatro señales doradas (latencia p95/p99, tráfico, errores, saturación).
3. Si el sistema usa modelos de IA: consumo y costo de tokens por usuario, calidad de inferencia y plan de actualización de índices o reentrenamiento.
4. Matriz de alertas con umbrales y canales.
5. Plantilla de postmortem sin culpables.
6. Antes de cada retrospectiva: resume la telemetría del sprint y propone historias nuevas con su RF.

## Salidas
En `docs/07-operacion/`: `slo.md`, `telemetria.md`, `alertas.md`, `plantilla-postmortem.md`.

## Puerta de salida
El equipo revisa en la Sprint Review y la Retrospectiva y reordena el backlog.
