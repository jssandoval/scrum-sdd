# DERCAS — [Nombre del proyecto]

Alineado con ISO/IEC/IEEE 29148.

## 1. Control documental

| Versión | Fecha | Autor | Cambio | Aprobado por |
| --- | --- | --- | --- | --- |
| 0.1 | AAAA-MM-DD | | Borrador inicial | |

## 2. Antecedentes y objetivos

Origen del proyecto, problema de negocio y metas cuantitativas.

## 3. Alcance y exclusiones

**Incluye:**

**Excluye explícitamente:**

## 4. Actores y roles

| Actor | Tipo | Permisos | Interacciones autorizadas |
| --- | --- | --- | --- |

## 5. Requisitos funcionales

### RF-001 [Título]

**Prioridad:** Must
**Actor:** [rol]
**Descripción:** El sistema debe [comportamiento observable].
**Reglas de negocio:** RN-001
**Origen documental:** [F-... y página/hoja/sección, o decisión humana]

## 6. Requisitos no funcionales

### RNF-001 [Título]

**Categoría:** Rendimiento
**Métrica:** latencia p95 < 300 ms con 100 usuarios concurrentes.
**Cómo se verifica:** prueba de carga en staging.

## 7. Reglas de negocio

### RN-001 [Título]

**Regla:** [validación, fórmula o restricción].
**Fuente:** [ley, política interna, decisión del cliente].

## 8. Criterios de aceptación

### CA-001 (RF-001) [Escenario principal]

```gherkin
Dado [precondición]
Cuando [acción]
Entonces [resultado verificable]
```

### CA-002 (RF-001) [Caso borde]

```gherkin
Dado [precondición]
Cuando [acción inválida]
Entonces [error esperado]
```

## 9. Matriz de trazabilidad

La genera `python3 .framework/scripts/trace.py`. No se edita a mano.

## 10. Informe de ambigüedades

| Término o requisito | Problema | Pregunta para el cliente |
| --- | --- | --- |

## 11. Fuentes y procedencia documental

Ver `docs/01-descubrimiento/inventario-fuentes.md`, `docs/01-descubrimiento/analisis-fuentes.md` y `docs/02-requisitos/matriz-trazabilidad-documental.md`. Los conflictos abiertos se gestionan en la sección 10. No interpretar una fuente inventariada como una fuente verificada.
