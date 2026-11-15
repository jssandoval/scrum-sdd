---
name: implementar
description: 'Implementa UNA historia de usuario con el ciclo SDD de seis pasos y TDD. Uso: /implementar HU-001 [--carril feature|hotfix]'
argument-hint: 'HU-XXX [--carril feature|hotfix]'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check sprint` (agrega `--carril <carril>` si el usuario lo indicó).
Verifica que la historia cumple la Definition of Ready. Si no, detente y di qué falta.

## Entradas
La historia en el backlog, sus RF, RN y CA en el DERCAS, `AGENTS.md`, `specs/memory.md`, la pantalla y el endpoint referenciados.

## Rol
Desarrollador full-stack senior.

## Pasos
Trabaja sobre `specs/HU-XXX.md`, creado desde `.framework/templates/spec-HU.md`. Una rama por historia.

1. **Specify.** Redacta comportamiento esperado, casos borde y fuera de alcance. Cita RF, RN y CA por ID.
2. **Clarify.** Busca vacíos y contradicciones. Si hay preguntas, escríbelas en la tabla y DETENTE hasta que el usuario responda.
3. **Plan.** Lista los archivos a crear o modificar y los patrones a usar. Muestra el plan y espera confirmación.
4. **Tasks.** Divide el plan en tareas pequeñas y secuenciales. La primera siempre es escribir las pruebas.
   Registra: `python3 .framework/scripts/gate.py hu HU-XXX especificada`
5. **Implement.** Para cada CA: escribe la prueba nombrando el CA, ejecútala y confirma que FALLA, implementa lo mínimo para que pase. Marca cada tarea al terminarla.
6. **Converge.** Ejecuta lint, formateador y la suite completa. Revisa que no haya código sin tarea asociada. Completa la lista de la sección 6 de la spec.

## Verificación
`python3 .framework/scripts/trace.py --hu HU-XXX` en OK y suite completa en verde.

## Puerta de salida
`python3 .framework/scripts/gate.py hu HU-XXX implementada` (exige spec y trazabilidad válidas)
Actualiza `specs/memory.md`, abre el Pull Request y detente. No audites tu propio trabajo: eso es `/auditar`.
