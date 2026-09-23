# Datos preparados para análisis

Exportación derivada de `../../2026-categorized.json`. No se edita a mano ni sustituye la fuente curada. Última revisión de evidencia y conciliación de cobertura: **17 de septiembre de 2026**. No es una actualización automática de Layoffs.fyi.

[Ejemplo completo en Jupyter](../../notebooks/explorar_despidos.ipynb) · [Leer sus resultados en HTML](../../notebooks/explorar_despidos.html)

## Empezar

- **`announcements.csv`**: 228 filas, una por anuncio incluido en el informe. Contiene dimensiones, cifras, estado de revisión, número de razones, indicador de IA y número de funciones identificadas. No hay listas ni objetos JSON en las celdas.
- **`layoffs.sqlite`**: todas las tablas, tipos, claves, relaciones y vistas, lista para SQL, pandas, R o herramientas BI.
- **`announcement_causes.csv`**: 304 filas anuncio–razón, con atribución, alcance, resumen y fuente. Unir por `record_id`.
- **`announcement_functions.csv`**: 116 filas anuncio–función. Unir por `record_id`.
- **`manifest.json`**: origen, hash de la fuente canónica, alcance, columnas, filas y comprobaciones.
- **`schema.sql`**: definición ejecutable de las tablas y vistas.
- **`examples.sql`**: consultas verificadas contra los hallazgos.

La base conserva los 235 registros internos. La vista `announcements` selecciona los mismos 228 del informe. `excluded_records.csv` explica las siete exclusiones: cinco medidas históricas o de período y dos entradas de julio. Los siete no se mezclan con los anuncios al usar las vistas `announcement_*`.

```python
import sqlite3
import pandas as pd

with sqlite3.connect("data/normalized/layoffs.sqlite") as db:
    announcements = pd.read_sql_query("SELECT * FROM announcements", db)
    reasons = pd.read_sql_query("SELECT * FROM announcement_causes", db)
    ai = announcements.loc[announcements.has_ai_reason.eq(1)]  # 72 filas

# Alternativa, sin base de datos:
announcements = pd.read_csv(
    "data/normalized/announcements.csv",
    parse_dates=["record_date", "review_date"],
    dtype={"laid_off": "Int64", "has_ai_reason": "boolean"},
)
```

## Granularidad y relaciones

| Tabla | Una fila representa | Clave / relación |
|---|---|---|
| `records` | Registro interno; `in_report` indica su inclusión | `record_id` |
| `companies` | Etiqueta exacta de empresa, no entidad jurídica deduplicada | `company_id` |
| `causes` | Categoría de razón, indicador IA y nivel de detalle | `cause_code` |
| `record_causes` | Razón atribuida a un registro | `record_id`, `cause_code` |
| `sources` | URL o referencia original de fuente, sin reescribirla | `source_id` |
| `record_sources` | Fuente consultada para una revisión y su papel | `record_id`, `source_id`, `role` |
| `functions` | Categoría de función afectada | `function_code` |
| `record_functions` | Función identificada en un registro | `record_id`, `function_code` |
| `function_evidence` | Evidencia sobre las funciones | `evidence_id`, `record_id` |
| `function_evidence_functions` | Función respaldada por esa evidencia | `evidence_id`, `function_code` |
| `context` | Observación de contexto, no causa | `context_id`, `record_id` |
| `denials` | Negación, con objeto y quién la formula | `denial_id`, `record_id` |
| `work_units`, `work_levels` | Unidad o nivel identificado; no equivale a una ocupación | `record_id` |
| `headcount_accounts` | Cifra alternativa o disputada con su atribución | `account_id`, `record_id` |
| `workforce_metrics` | Medida de plantilla distinta del anuncio de despidos | `record_id` |
| `related_records` | Relación explícita entre registros; no deduplicación automática | Ambos IDs |
| `review_issues` | Advertencia de calidad o alcance | `record_id`, `issue` |
| `locations` | Etiqueta de ubicación de la fuente | `record_id`, `position` |
| `coverage` | Metadatos de incorporación desde el rastreador | `record_id` |

`announcements`, `announcement_causes`, `announcement_functions` y `excluded_records` son vistas, también exportadas como CSV. `schema.sql` contiene los tipos y las claves de cada columna. Todas las tablas se exportan con cabecera aunque no tengan filas.

## Convenciones importantes

- Fechas ISO `YYYY-MM-DD`. `record_date` es la fecha registrada; en registros excluidos puede ser un cierre de período, no un anuncio. `review_date` es la revisión de evidencia, no la fecha de construcción del archivo.
- Valores desconocidos: `NULL` en SQLite y celda vacía en CSV. `Unknown` y cadenas vacías de industria, etapa y país se convierten a nulos. No se convierte un dato desconocido en cero.
- `workforce_fraction` es una **fracción**: `0.1` significa 10%. `laid_off` es una cifra registrada, no necesariamente una salida ejecutada.
- `raised_millions` conserva `raised_mm` de la fuente en millones; esta exportación no verifica ni armoniza moneda, fecha o perímetro.
- Indicadores como `in_report`, `has_ai_reason` e `is_ai` son enteros `0/1`. Ausencia de una razón de IA no demuestra ausencia de influencia de IA.
- Industria, etapa y ubicación permanecen en el registro: no se asume que sean constantes por empresa. Los IDs de empresa son hashes estables de la etiqueta exacta. No se fusionan matrices, filiales ni nombres parecidos.
- Los IDs de evidencia con sufijo numérico son locales al orden del registro; no son identificadores persistentes de una publicación.
- `specificity` se conserva como dato de auditoría. Todos los niveles cuentan en las vistas del informe.

## Cómo evitar dobles conteos

Después de unir anuncios con razones o funciones, un anuncio puede ocupar varias filas. Usar `COUNT(DISTINCT record_id)` para contar anuncios; **no sumar `laid_off` después de esos joins**. Incluso en la tabla de anuncios hay posibles planes solapados: no es un total auditado de personas únicas despedidas.

Las medidas netas anuales, los porcentajes alternativos y las cifras disputadas se mantienen separados. No se usan para rellenar automáticamente `laid_off`. Una ausencia de función identificada tampoco significa que esa función no estuviera afectada.

## Alcance y reconstrucción

Esta es una exportación analítica, no una copia reversible de todas las notas de trabajo: las revisiones históricas completas, notas de búsqueda, estados antes/después y decisiones editoriales permanecen en el JSON canónico, `coverage/` y `research/`. Las explicaciones, fuentes, atribuciones, funciones, contexto, negaciones y problemas de calidad sí tienen tablas propias.

```sh
python3 scripts/validate_causes.py
python3 scripts/build_normalized.py
```

El build del informe también regenera esta exportación. El script comprueba integridad SQLite, claves únicas y foráneas, preservación de IDs, causas y funciones de cada registro, tipos escalares y coincidencia de los recuentos con el JSON. No vuelve a investigar ni reclasifica eventos.
