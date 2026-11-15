---
name: ssdd-arquitectura
description: 'Diseña arquitectura C4, modelo de datos, contrato OpenAPI, modelo de amenazas y ADRs.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check arquitectura`

## Entradas
DERCAS y `docs/03-diseno/`. Plantilla `.framework/templates/ADR.md`.

## Rol
Arquitecto de software principal con práctica en seguridad de aplicaciones (OWASP ASVS).

## Decisión obligatoria de stack por el programador (ANTES de generar la arquitectura)
1. Leer el DERCAS, los RNF y los ADR existentes, si los hay. No asumir tecnologías ni proveedores.
2. Presentar al programador opciones razonadas para **frontend**, **backend**, **interoperabilidad / integración** (REST, eventos, mensajería, ETL o "no aplica"), **persistencia** (bases de datos, almacenamiento) y **despliegue/infraestructura**; explicar implicaciones y recomendar una opción por categoría, marcándola como recomendación, no como decisión.
3. Preguntar explícitamente: «¿Qué stack deseas utilizar para cada categoría? ¿Aceptas mis recomendaciones o prefieres otras tecnologías?» Permitir decidir individualmente y dejar constancia cuando una categoría no aplique.
4. **DETENERSE** y esperar respuesta humana. No generar ADR-001 ni diseñar la arquitectura definitiva hasta tener elección del programador. No interpretar el silencio como aceptación.
5. Registrar las elecciones y la persona que decidió en `docs/04-arquitectura/decisiones/ADR-001-stack-tecnologico.md` mediante el modelo `.framework/templates/ADR.md`. Incluir el bloque `## Stack` exigido por `/ssdd-setup` y la sección `## Decisiones del programador` con Frontend, Backend, Interoperabilidad, Persistencia, Infraestructura y Responsable.
6. Si existen restricciones incompatibles con la decisión, explicar la incompatibilidad y pedir nueva decisión; no sustituir tecnologías unilateralmente.

## Pasos
1. Diagramas C4 nivel 1 (contexto) y nivel 2 (contenedores) en Mermaid.
2. Patrón arquitectónico, justificado contra los RNF.
3. Modelo de datos: ERD en Mermaid, diccionario de datos, claves, índices justificados, restricciones.
4. Contrato OpenAPI 3.1: endpoints, DTOs, códigos HTTP, validaciones.
5. Modelo de amenazas STRIDE, autenticación, autorización RBAC multi-tenant y controles ASVS aplicables.
6. Completar ADR-001 con el stack elegido por el programador (no el sugerido automáticamente), ADR-002 (persistencia) y uno por cada decisión adicional.

## Salidas
En `docs/04-arquitectura/`: `arquitectura-c4.md`, `modelo-datos.md`, `contratos-api.json`, `seguridad.md`, `decisiones/ADR-*.md`.

## Verificación
Cada RNF está atendido por una decisión de arquitectura identificable. Verifica que ADR-001 registra la selección humana de frontend, backend, interoperabilidad, persistencia e infraestructura; lista los RNF sin decisión.

## Puerta de salida
El Tech Lead revisa viabilidad y costos. Luego:
`/ssdd-aprobar arquitectura --por "<nombre>"`
