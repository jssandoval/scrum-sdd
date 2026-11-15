---
name: ssdd-dercas
description: 'Genera o actualiza DERCAS desde descubrimiento y documentación fuente, con trazabilidad y resolución de conflictos.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check requisitos` (en proyecto existente usa `--carril feature`). La aprobación humana sigue siendo exclusiva de `/ssdd-aprobar`.

## Entradas
`docs/01-descubrimiento/`, todas las fuentes en `docs/00-fuentes/`, `.framework/templates/DERCAS.md` y `.framework/templates/matriz-trazabilidad-documental.md`.

## Rol
Especialista en ingeniería de requisitos ISO/IEC/IEEE 29148 y análisis documental.

## Pasos
1. Ejecuta `python3 .framework/scripts/fuentes.py check`. Si falla, vuelve a inventariar con `scan`, analiza nuevas versiones y señala que las aprobaciones previas pueden caducar. Nunca ignores cambios de fuentes.
2. Verifica cobertura y hallazgos de `analisis-fuentes.md`; **lee directamente las fuentes pertinentes** para corroborar cada requisito propuesto, sus tablas, imágenes y anexos. No sustituyas verificación con resúmenes previos.
3. Copia la plantilla DERCAS si no existe. Completa control documental, antecedentes, alcance, exclusiones, actores y roles.
4. Redacta RF y prioridades MoSCoW, RNF cuantificables, RN con sus fuentes, y al menos dos CA por RF activo (normal y borde) en Gherkin.
5. Produce `docs/02-requisitos/matriz-trazabilidad-documental.md`: para cada RF, RNF, RN y CA extraído, registra fuente `F-...`, ubicación (página/hoja/celda/sección), hallazgo `H-...` y si es explícito o derivado. Una propuesta no sustentada por archivos debe identificarse como **propuesta del analista pendiente de validación**, no como obligación documental.
6. Consolida duplicados preservando referencias a todas las fuentes; registra contradicciones `C-...` y preguntas en `DERCAS.md` sin elegir arbitrariamente una versión. Antes de aprobar, exige decisión humana sobre contradicciones que afecten requisitos obligatorios o seguridad.
7. Respeta IDs de tres dígitos y no reutilices IDs; no alteres requisitos no relacionados en carril feature.
8. Convierte términos subjetivos en métricas solo si hay evidencia o decisión aprobada; en caso contrario registra una pregunta.

## Verificación
`python3 .framework/scripts/fuentes.py check` y `python3 .framework/scripts/trace.py` deben terminar en OK. Valida manualmente trazabilidad documental y cobertura de fuentes; `trace.py` no certifica la veracidad de documentos.

## Salidas
`docs/02-requisitos/DERCAS.md`, `docs/02-requisitos/matriz-trazabilidad-documental.md` e informe de ambigüedades incluido en DERCAS.

## Puerta de salida
Presenta fuentes no leídas, contradicciones y requisitos derivados. Cuando el cliente resuelva lo crítico y revise, **el usuario** escribe `/ssdd-aprobar requisitos --por "<nombre>"`. Cualquier edición del DERCAS o cambio en fuentes vinculadas invalida el hash de aprobación correspondiente.
