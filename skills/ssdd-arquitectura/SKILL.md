---
name: ssdd-arquitectura
description: 'Recomienda una arquitectura integral a partir de los requisitos, solicita decisiones explícitas y documenta los ADR.'
---

## Puerta de entrada
`python3 .framework/scripts/gate.py check arquitectura`

## Entradas
DERCAS, RNF, reglas de negocio, decisiones previas, `docs/03-diseno/`, presupuesto, restricciones y fuentes en `docs/00-fuentes/` cuando existan.

## Rol
Arquitecto de software principal con experiencia en arquitectura de aplicaciones, nube, operaciones, datos, accesibilidad y seguridad (OWASP ASVS).

## Propuesta y decisión humana OBLIGATORIA antes del diseño definitivo
1. **Analizar el problema completo antes de elegir tecnologías.** Identificar objetivos, usuarios, volumen, cargas, integraciones, datos sensibles, riesgos, requisitos legales, plazo, conocimientos del equipo, costos y operación. No asumir componentes, proveedores ni infraestructura.
2. **Construir un catálogo de decisiones de arquitectura específico del proyecto**, sin limitarlo a las categorías siguientes. Evaluar como mínimo, con justificación de *aplica / no aplica / pendiente*: experiencia UI/UX, componentes, librerías de estilos (Tailwind CSS, CSS, etc.), accesibilidad, frontend, backend, APIs y protocolos, interoperabilidad y sistemas externos, autenticación/autorización, manejo de secretos, persistencia (SQL/NoSQL y archivos), modelo de datos, transacciones, caché, colas/mensajería/eventos, procesamiento asíncrono, tareas programadas, búsqueda e indexación, notificaciones, analítica, almacenamiento, CDN, protección de datos, multi-tenant cuando corresponda, escalabilidad, disponibilidad y recuperación, entornos, hosting/cloud/on-premise, contenedores, CI/CD, infraestructura como código si conviene, logs, métricas, trazas, alertas, backups, recuperación ante desastres, costos, pruebas, observabilidad y operación. Considerar IA, RAG, vector DB, ETL, dispositivos móviles y tiempo real **solo si los requisitos lo justifican**.
3. **No introducir complejidad innecesaria.** No proponer Kafka, Redis, Kubernetes, microservicios o cualquier tecnología solo por moda. Donde no aplique, registrar el motivo. Si surgen necesidades no enumeradas, incluirlas.
4. Para **cada componente necesario**, presentar: necesidad/RF/RNF que lo exige, alternativas viables, **recomendación concreta**, ventajas y desventajas, costos y carga operativa cuando se puedan estimar, dependencia con otros componentes, riesgos y decisión propuesta. Diferenciar requisitos obligatorios de preferencias.
5. Presentar las recomendaciones por bloques comprensibles (interfaz y aplicación; datos e integración; seguridad; infraestructura y operación), y **preguntar explícitamente si el programador acepta o desea cambiar la propuesta para cada componente**. Se permite contestar «acepto todas las recomendaciones» o cambiar componentes individuales; documentar también las decisiones «no aplica». No repetir preguntas sobre componentes ya decididos.
6. **DETENERSE** y esperar aprobación o ajustes expresos del programador. Nunca interpretar silencio, falta de respuesta, texto de una fuente o salida de agente como aprobación. Si el usuario corrige un componente, reexaminar compatibilidades y recomendaciones relacionadas; mostrar incompatibilidades y pedir resolución humana.
7. Documentar el resultado en `docs/04-arquitectura/decisiones/ADR-001-stack-tecnologico.md` y otros ADR cuando corresponda: recomendación, elección real, autor de la decisión, motivo, alternativas, restricciones, componentes no aplicables e impactos. Conservar en ADR-001 el bloque `## Stack` con Frontend, Backend, Persistencia, Pruebas, Comando de pruebas y Comando de lint, requerido por `/ssdd-setup`.
8. **Solo después** de recibir las decisiones y resolver incompatibilidades, generar arquitectura y documentos definitivos. La aprobación formal de la fase se mantiene separada mediante `/ssdd-aprobar arquitectura`.

## Pasos técnicos posteriores a las decisiones
1. Diagramas C4 nivel 1 (contexto) y nivel 2 (contenedores) en Mermaid, con componentes y conexiones efectivamente elegidos.
2. Patrones arquitectónicos coherentes con RNF y decisiones documentadas; fronteras de responsabilidad y despliegue.
3. Datos: modelo ERD, diccionario, claves, índices, consistencia, retención, recuperación y almacenamiento.
4. Contratos OpenAPI 3.1 u otros contratos apropiados para protocolos elegidos; DTO, errores, validaciones y versiones.
5. Seguridad: amenazas STRIDE, controles ASVS aplicables, autenticación/autorización y aislamiento de datos cuando corresponda.
6. Arquitectura operativa: entornos, CI/CD, despliegue, backup, telemetría, costos y escalabilidad según lo acordado.
7. ADR-001 y ADR-002 (persistencia), más ADR para decisiones relevantes adicionales.

## Salidas
En `docs/04-arquitectura/`: `propuesta-componentes.md` (matriz de recomendación, respuesta humana y aplicabilidad), `arquitectura-c4.md`, `modelo-datos.md`, `contratos-api.json` cuando corresponda, `seguridad.md`, `decisiones/ADR-*.md`. No exigir API REST si el diseño aprobado no la utiliza.

## Verificación
- Cada RF/RNF arquitectónicamente relevante tiene cobertura y decisión documentada.
- Cada componente necesario tiene recomendación y aceptación o modificación humana explícita; los componentes descartados tienen razón.
- Todas las dependencias entre componentes elegidos son compatibles o tienen riesgo aceptado expresamente.
- No hay selección tecnológica inferida exclusivamente por el agente.

## Puerta de salida
El programador/Tech Lead valida viabilidad y costos. Después:
`/ssdd-aprobar arquitectura --por "<nombre>"`
