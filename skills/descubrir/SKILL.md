---
name: descubrir
description: 'Evalúa una idea de producto y analiza documentación fuente (manuales, normas, formularios, matrices y requerimientos) antes de especificarla.'
---

## Puerta de entrada
Ninguna. Es la primera fase. No apruebes en nombre del usuario.

## Entradas
La idea del usuario y todos los archivos disponibles bajo `docs/00-fuentes/`, con subcarpetas `manuales/`, `lineamientos/`, `formularios/`, `matrices/`, `requerimientos/` y `otros/`. Si no hay idea, infiere **solo hipótesis etiquetadas** de fuentes existentes o pregunta lo imprescindible.

## Rol
Analista de negocio senior con práctica en Design Thinking, Lean Startup y análisis documental.

## Pasos
1. Antes de redactar conclusiones, ejecuta `python3 .framework/scripts/fuentes.py scan` y examina `docs/01-descubrimiento/inventario-fuentes.md`. Si no hay fuentes, continúa con la idea y documenta que no hubo fuentes.
2. Lee **cada archivo** con herramientas compatibles con su formato: Markdown/TXT, PDF (incluidos diagramas o páginas escaneadas cuando la herramienta lo permita), Word, Excel (todas las hojas pertinentes), imágenes, etc. El inventario automático **solo registra** archivos: no extrae contenido. No declares como leído lo que no pudiste abrir o interpretar; identifica páginas, hojas, celdas, secciones y archivos no procesados. Respeta privacidad y no subas material sensible a servicios no autorizados.
3. Crea `docs/01-descubrimiento/analisis-fuentes.md` usando `.framework/templates/analisis-fuentes.md`. Registra evidencia puntual con `F-...`, ubicación y hallazgo `H-...`; clasifica HECHO, SUPUESTO o RECOMENDACIÓN. Contrasta documentos, identifica duplicados, versiones y contradicciones `C-...` sin resolverlas por tu cuenta.
4. Describe el problema de negocio y el proceso actual (AS-IS), separando afirmaciones documentadas de hipótesis.
5. Define personas usuarias y actores, propuesta de valor y diferenciadores; elabora Lean Canvas.
6. Identifica las cinco hipótesis más riesgosas y diseña experimentos baratos por hipótesis, ejecutables en menos de dos semanas.
7. Lista las diez preguntas prioritarias previas al diseño técnico, incluyendo contradicciones documentales pendientes. Si un dato es crítico y contradictorio, suspende su definición y solicita decisión humana.
8. Registra documentos inaccesibles o parcialmente procesados; entrega un resumen de cobertura antes de pedir aprobación.

## Salidas
En `docs/01-descubrimiento/`: `inventario-fuentes.json`, `inventario-fuentes.md`, `analisis-fuentes.md`, `vision-producto.md`, `problema-negocio.md`, `lean-canvas.md`, `viabilidad-hipotesis.md`.

## Verificación
Ejecuta `python3 .framework/scripts/fuentes.py check`. Cada hecho derivado de documentos debe indicar fuente y ubicación comprobable; documenta excepciones. No generes código, ni inventes datos de mercado, campos, normas o reglas.

## Puerta de salida
El patrocinador revisa el inventario, el análisis, las contradicciones y decide Go, Pivot o No-Go. Si es Go, **el usuario** escribe `/aprobar descubrimiento --por "<nombre>"`. Nunca ejecutes el skill por él.
