---
name: auditar
description: 'Auditoría independiente de calidad y seguridad de una historia implementada. Uso: /auditar HU-001'
---

## Puerta de entrada
Ejecuta `python3 .framework/scripts/gate.py status`. La historia debe estar en estado `implementada`.

## Independencia (obligatorio)
Esta auditoría NO puede correr en la sesión que escribió el código. Lanza un subagente con contexto limpio, o pide al usuario abrir una sesión nueva. El auditor recibe solo: el diff del Pull Request, el DERCAS, la arquitectura y la spec de la historia. No recibe la conversación de implementación.

## Rol
Ingeniero de seguridad senior y Lead QA.

## Pasos
1. **Cobertura.** Verifica que cada CA de la historia tiene una prueba que realmente comprueba el `Entonces`, no solo que lo nombra.
2. **Seguridad.** Revisa contra OWASP ASVS: inyección, exposición de datos sensibles, gestión de sesiones, y con prioridad la elevación de privilegios y el aislamiento multi-tenant.
3. **Arquitectura.** Verifica las capas y que no haya dependencias fuera de los ADR.
4. **E2E.** Escribe la prueba Playwright del flujo completo de la historia.
5. Clasifica cada hallazgo: Crítica, Alta, Media, Baja.

No corrijas el código. Entrega el informe.

## Salidas
`docs/06-pruebas/auditoria-HU-XXX.md` desde `.framework/templates/informe-auditoria.md`.

## Puerta de salida
Si hay hallazgos críticos o altos: veredicto Rechazado; la historia vuelve a `/implementar`.
Si no: escribe en el informe `Veredicto: Aprobado` (sin hallazgos críticos/altos) y luego ejecuta `python3 .framework/scripts/gate.py hu HU-XXX auditada`
El Product Owner ejecuta la UAT contra los CA y, si acepta, el usuario ejecuta:
`/aceptar HU-XXX --por "<nombre>"`
