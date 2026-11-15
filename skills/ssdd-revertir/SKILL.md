---
name: ssdd-revertir
description: 'Revierte el cierre aprobado de una fase y guarda un histórico, exclusivamente por solicitud humana explícita.'
argument-hint: '<fase> --por "<nombre>" --motivo "<razón>"'
disable-model-invocation: true
---

Argumentos recibidos: $ARGUMENTS

## Uso
`/ssdd-revertir arquitectura --por "Nombre" --motivo "Cambiar stack"`

## Restricción humana
Únicamente cuando el usuario escribe explícitamente este skill. No invocarlo desde agentes, otros skills ni automatizaciones. Verificar nombre y motivo; no inventarlos. La CLI no autentica la identidad de quien invoca Python directamente.

## Procedimiento
1. Confirmar que la fase indicada está aprobada y explicar que las aprobaciones **de esa fase y las posteriores** serán invalidadas.
2. Ejecutar `python3 .framework/scripts/gate.py revert <fase> --por "<nombre>" --motivo "<razón>"` solo tras una solicitud explícita del humano mediante este skill.
3. El script archiva una copia de documentos de esa fase, la fotografía del estado previo y una bitácora en `docs/historico-fases/` y revoca las aprobaciones dependientes.
4. **No borrar, sobrescribir ni revertir automáticamente** código, documentos originales, aprobaciones de historias o archivos de trabajo; quedan para revisión y corrección con el skill de fase que corresponda.
5. Mostrar la ubicación del histórico y el siguiente skill para rehacer la fase. Después se volverá a aprobar con `/ssdd-aprobar`.

No reabrir o modificar la fase sin petición del usuario. Revertir aprobación no equivale a Git rollback; cambios de código necesitan reversión Git independiente.
