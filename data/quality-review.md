# Estado de los datos y del repositorio

Comprobación local del **22 de septiembre de 2026**. No se realizó una nueva consulta de cobertura externa: el snapshot y la revisión de evidencia más recientes utilizados siguen siendo del **17 de septiembre**.

## Fuente vigente y coherencia

La fuente curada es `2026-categorized.json`, con 235 registros. La selección de los 228 anuncios publicados coincide exactamente con `report/records.json`. El CSV canónico también coincide y la cadena de auditorías reconstruye el JSON. No hay IDs duplicados ni pares empresa–fecha repetidos. Eso no descarta planes que se solapan entre fechas o filiales.

La base es consistente para los recuentos del informe; no es un conjunto completo de todos los despidos ni de todas las explicaciones posibles. Una revisión de fuente no demuestra causalidad.

## Vacíos de los 228 anuncios públicos

| Campo o revisión | Sin dato / incompleto |
|---|---:|
| Industria | 66 |
| Etapa de financiación / cotización | 88 |
| Número de personas despedidas | 82 |
| Fracción de plantilla afectada | 105 |
| Financiación acumulada de la fuente | 94 |
| Función afectada identificada | 168 |
| Fuente parcial | 14 |
| Fuente causal no recuperada | 2 |

Hay 201 anuncios con alguna razón clasificable y 27 sin ella. La información de funciones identifica ocupaciones en 60 anuncios; ocho de los restantes solo identifican unidades de negocio. Las razones generales no se recodificaron exhaustivamente junto a todas las decisiones específicas. La exportación conserva estos límites; no los rellena por inferencia.

Las cifras de plantilla y razones pueden tener alcances distintos. Las variaciones netas, cifras alternativas y relaciones de planes permanecen separadas. No debe sumarse personal después de unir tablas de razones o funciones.

## Problemas encontrados y corregidos

- El README tenía estados de fuente antiguos (198/35/2) frente a los vigentes (219/14/2 sobre 235 registros), y aún describía una exclusión de razones generales que el informe ya no hace.
- Referenciaba `full-review-2026-09-17.json`, que no existe. La cadena comienza en `full-review-2026-09-16.json` y continúa en `coverage/`.
- Los resúmenes auxiliares seguían destacando los 59 casos de IA con explicación específica. Se regeneraron para contar todas las razones: 72 con IA, 48 con IA y otra razón, 79 con varias razones.
- El CSV canónico incluye JSON dentro de celdas. Sigue disponible como copia de compatibilidad; la nueva exportación relacional contiene campos escalares y tipos explícitos.
- Las credenciales locales no estaban ignoradas por Git. Se añadieron patrones `.env` sin abrir ni modificar su contenido.

## Limpieza realizada y criterios de conservación

Se eliminaron cachés de Python y metadatos `.DS_Store`, que se regeneran sin pérdida de investigación. `hallazgos.md` y `auditoria-sobrecontratacion.md`, sin uso en el pipeline actual, se trasladaron a `archive/legacy-analysis/` para que no compitan con la documentación vigente.

Se conservan las auditorías y los snapshots de ingestión: el validador y la trazabilidad dependen de ellos. También se conservan fuentes recuperadas, aunque no sean parte del CSV público; son evidencia, no caché descartable.

`charts_marca/`, los notebooks originales y las carpetas editoriales anteriores no intervienen en el build actual. Se marcan como históricos en el README. No se borran en bloque: pueden contener trabajo distinto, material original o dependencias propias. Los checkpoints de notebooks se conservan porque podrían contener cambios no incorporados al archivo principal.

No es necesario reducir todo el repositorio a los 228 anuncios: basta con tener una única fuente canónica y una entrada analítica inequívoca. La exportación incluye `excluded_records.csv`, con los siete registros fuera del informe y su motivo.

## Exportación para análisis

[Guía de uso](normalized/README.md). Incluye 24 tablas/vistas en CSV y SQLite. Las tablas principales para el informe son 228 anuncios, 304 atribuciones de razones y 116 relaciones anuncio–función. Los nombres de empresa no se fusionaron con matrices ni se deduplicaron por similitud.

`manifest.json` registra el hash del JSON canónico y del generador, conteos, columnas, convenciones de nulos y unidades. El build comprueba claves foráneas, unicidad, preservación de causas y funciones por registro, integridad SQLite y concordancia con los recuentos del informe.

La exportación es reproducible; la renovación de cobertura externa sigue siendo una tarea de investigación separada.
