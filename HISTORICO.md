# Historial de versiones de Scrum-SDD / SSDD

Este registro conserva la evolución del framework desde **Scrum-SDD** hasta su denominación actual **SSDD (Scrum SDD)**. Los archivos históricos no deben modificarse; las versiones se conservan como artefactos independientes.

| Versión | Artefacto histórico | Cambios principales | Estado |
| --- | --- | --- | --- |
| **0.1.0** | `history/framework-scrum-sdd-v0.1.0-documento-original.md` | Documento de diseño original del framework Scrum-SDD. | Solo documento de diseño; **no hay ZIP ejecutable original verificable**. |
| **0.2.0** | `history/scrum-sdd-v0.2.0.zip` | Primera distribución ejecutable conservada; skills, plantillas, puertas y trazabilidad. | ZIP original conservado. |
| **0.2.0 con guía** | `history/scrum-sdd-v0.2.0-con-guia.zip` | Se incorporó la guía de instalación y uso; misma versión funcional 0.2.0. | ZIP histórico conservado. |
| **0.3.0** | `history/scrum-sdd-v0.3.0-con-documentos.zip` | Incorporación de documentos fuente (manuales, formularios, matrices, normativas y requisitos) al descubrimiento y DERCAS, con inventario y trazabilidad. | ZIP conservado; base de 0.4.0. |
| **0.4.0** | `history/scrum-sdd-v0.4.0.zip` | CLI, inicialización y actualización de proyectos, instalación multiplataforma; metodología inalterada. | ZIP disponible. Existe además una variante preparada para GitHub. |
| **0.4.5** | `history/ssdd-v0.4.5-listo-github.zip` | Nombre oficial **SSDD**, CLI `ssdd` y comandos de skills con prefijo `ssdd-`; actualización de referencias y documentación. | ZIP preparado para GitHub. |
| **0.4.6** | `history/ssdd-v0.4.6-listo-github.zip` | Actualización de instalaciones existentes con `ssdd update`; selección humana del stack (frontend, backend, interoperabilidad, persistencia e infraestructura) durante arquitectura; nuevo skill `/ssdd-revertir` con archivo histórico de la fase. | ZIP preparado para GitHub; versión anterior conservada. |

| **0.4.7** | `history/ssdd-v0.4.7-listo-github.zip` | Arquitectura integral con recomendaciones por componente y confirmación humana; reversión en modalidad «solo aprobación» o «eliminar paso completo» con respaldo y confirmación adicional. | ZIP preparado para GitHub; versión más reciente de este registro. |

## Compatibilidad de comandos

| Versiones | CLI | Ejemplo de skill |
| --- | --- | --- |
| 0.4.0 | `scrum-sdd` | `/descubrir` |
| 0.4.5, 0.4.6 y 0.4.7 | `ssdd` | `/ssdd-descubrir` |

Para instalar o actualizar la CLI **0.4.7**, primero se ejecuta el instalador de esa versión (`sh install-cli.sh` en macOS/Linux o `install-cli.ps1` en Windows). Dentro del proyecto, `ssdd update` actualiza los archivos del framework. Se mantienen los documentos, el código y el estado del proyecto.

## Conservación y publicación

- El código fuente de la versión vigente se publica en `https://github.com/jssandoval/scrum-sdd`.
- Se recomienda crear las etiquetas Git `v0.1.0` a `v0.4.7` **solo cuando se disponga de un commit auténtico para cada versión**; no reconstruir ni atribuir commits históricos ficticios.
- Adjuntar los ZIP originales a sus respectivos **GitHub Releases**, sin introducirlos obligatoriamente en el árbol de código actual.
- El archivo de v0.1.0 es documentación histórica, **no un paquete ejecutable**.
- La existencia local de un ZIP no significa que ya esté publicado en GitHub; publicación y pruebas en cada sistema operativo deben verificarse por separado.

**Nota de trazabilidad:** las entradas describen los artefactos conservados y los cambios documentados. No certifican que versiones anteriores hayan sido publicadas como GitHub Releases. El nombre de la carpeta `history/` es la organización recomendada para un paquete histórico; no implica que estos archivos estén ya subidos al repositorio.
