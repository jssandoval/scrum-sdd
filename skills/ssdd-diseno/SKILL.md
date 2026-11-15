---
name: ssdd-diseno
description: 'Diseña procesos BPMN, navegación, design system e inventario de pantallas a partir del DERCAS.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check diseno`

## Entradas
`docs/02-requisitos/DERCAS.md`.

## Rol
Lead UX/UI y analista de procesos BPMN 2.0.

## Pasos
1. Modela los procesos clave en BPMN 2.0: actividades descritas y diagrama en Mermaid.
2. Elabora el mapa de navegación y los user flows de las tareas más frecuentes.
3. Especifica el design system con WCAG AA: paleta con contraste validado, escala tipográfica, espaciado y componentes base (Atomic Design).
4. Elabora el inventario de pantallas: nombre, ruta, componentes, estados (carga, vacío, error, éxito) y RF que satisface.

Enfoque mobile-first. No generes código de aplicación.

## Salidas
En `docs/03-diseno/`: `procesos-bpmn.md`, `mapa-navegacion.md`, `design-system.md`, `inventario-pantallas.md`.

## Verificación
Todo RF activo con interfaz aparece en al menos una pantalla del inventario. Lista los que falten.

## Puerta de salida
Validación de flujos con usuarios representativos. Luego:
`/ssdd-aprobar diseno --por "<nombre>"`
