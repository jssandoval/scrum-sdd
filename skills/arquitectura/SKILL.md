---
name: arquitectura
description: 'Diseña arquitectura C4, modelo de datos, contrato OpenAPI, modelo de amenazas y ADRs.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check arquitectura`

## Entradas
DERCAS y `docs/03-diseno/`. Plantilla `.framework/templates/ADR.md`.

## Rol
Arquitecto de software principal con práctica en seguridad de aplicaciones (OWASP ASVS).

## Pasos
1. Diagramas C4 nivel 1 (contexto) y nivel 2 (contenedores) en Mermaid.
2. Patrón arquitectónico, justificado contra los RNF.
3. Modelo de datos: ERD en Mermaid, diccionario de datos, claves, índices justificados, restricciones.
4. Contrato OpenAPI 3.1: endpoints, DTOs, códigos HTTP, validaciones.
5. Modelo de amenazas STRIDE, autenticación, autorización RBAC multi-tenant y controles ASVS aplicables.
6. ADR-001 (stack, con el bloque "Stack" completo), ADR-002 (persistencia) y uno por cada decisión adicional.

## Salidas
En `docs/04-arquitectura/`: `arquitectura-c4.md`, `modelo-datos.md`, `contratos-api.json`, `seguridad.md`, `decisiones/ADR-*.md`.

## Verificación
Cada RNF está atendido por una decisión de arquitectura identificable. Lista los que no.

## Puerta de salida
El Tech Lead revisa viabilidad y costos. Luego:
`/aprobar arquitectura --por "<nombre>"`
