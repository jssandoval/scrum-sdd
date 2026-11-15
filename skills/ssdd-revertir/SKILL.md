---
name: ssdd-revertir
description: 'A solicitud humana, revoca la aprobación o retira los entregables completos de una fase archivándolos previamente.'
argument-hint: '<fase> --modo aprobacion|paso --por "<nombre>" --motivo "<razón>"'
disable-model-invocation: true
---

Argumentos recibidos: $ARGUMENTS

## Dos modalidades: debes ofrecer ambas al usuario
**A. Solo quitar aprobación (predeterminada)**:
`/ssdd-revertir arquitectura --modo aprobacion --por "Nombre" --motivo "Reconsiderar stack"`
- Archiva copia de la fase y estado anterior; retira la aprobación de esa fase y de todas las posteriores.
- **Conserva intactos los entregables**, archivos originales, código y HU para editar y volver a aprobar.

**B. Eliminar el paso completo (solamente tras confirmación humana explícita)**:
`/ssdd-revertir arquitectura --modo paso --por "Nombre" --motivo "Rehacer arquitectura"`
- Informa previamente qué directorio o archivo se retirará, qué aprobaciones posteriores se revocarán y que se guardará un respaldo restaurable.
- Pregunta al humano **«¿Confirmas eliminar los entregables de esta fase después de archivarlos?»** y DETENTE si todavía no confirmó explícitamente esta acción. La mera mención de revertir no es consentimiento de eliminación.
- Una vez que el humano confirme, ejecuta el comando con `--confirmar-eliminar-paso`.
- Archiva **toda la carpeta de entregables de la fase**, el estado previo y el manifiesto, verifica el respaldo y **solo entonces** retira los documentos de esa fase del directorio activo. En `setup`, el alcance es únicamente `AGENTS.md`, no el código, contenedores, infraestructura ni otros archivos del proyecto.
- No elimina entregables de otras fases, `docs/00-fuentes`, `docs/estado.json`, `specs/`, `src/`, `tests/`, ni commits Git. Las etapas siguientes dejan de estar aprobadas y sus documentos se conservan para revisión posterior.

## Restricción humana
Únicamente cuando el usuario invoca explícitamente este skill. No invocarlo desde agentes, otros skills ni automatizaciones. Verificar fase, persona y motivo; no inventar datos. La CLI Python **no autentica** identidad si alguien accede directamente a la terminal.

## Procedimiento
1. Si el usuario no especificó `--modo`, preguntar si desea solo retirar aprobación o retirar todo el paso. Si no desea eliminación, utilizar `aprobacion`.
2. Mostrar consecuencias y alcance concreto. Verificar si la fase consta como aprobada; si no está aprobada, no proceder.
3. Para `aprobacion`, ejecutar `python3 .framework/scripts/gate.py revert <fase> --modo aprobacion --por "<nombre>" --motivo "<razón>"`.
4. Para `paso`, confirmar explícitamente la eliminación y entonces ejecutar `python3 .framework/scripts/gate.py revert <fase> --modo paso --confirmar-eliminar-paso --por "<nombre>" --motivo "<razón>"`.
5. Comunicar directorio `docs/historico-fases/`, qué quedó archivado, qué se retiró del proyecto y cuál es el siguiente skill para rehacer la fase. No prometer restauración automática: el usuario puede recuperar la copia manualmente.

Revertir una fase no equivale a revertir Git ni a deshacer el código desarrollado.
