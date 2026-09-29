# Despidos tecnológicos de 2026: datos, evidencia y análisis

La **fuente de verdad es [2026-categorized.json](2026-categorized.json)**: 235 registros curados, con razones atribuidas, fuentes, alcance y revisión. El informe utiliza **228 anuncios de enero–junio**. Cinco medidas históricas o de período y dos entradas de julio quedan fuera de ese análisis, pero se conservan para trazabilidad.

**Cobertura general conciliada con Layoffs.fyi: 17 de septiembre de 2026. Revisión de evidencia: 29 de septiembre de 2026.** Los archivos publicados coinciden con la fuente curada. Esto no significa que se hayan incorporado cambios posteriores del rastreador. El snapshot de cobertura utilizado es `coverage/layoffs-fyi-2026-09-17.json`.

## Elegir el archivo adecuado

| Necesidad | Recurso |
|---|---|
| Leer hallazgos | [Artículo](report/index-es.html) |
| Explorar anuncios y evidencia | [Explorador](report/explorar.html) |
| Aprender con un ejemplo ejecutado | [Notebook exploratorio](notebooks/explorar_despidos.ipynb) · [HTML](notebooks/explorar_despidos.html) |
| Analizar con SQL, pandas, R o BI | [Exportación normalizada](data/normalized/README.md) |
| Una tabla plana de los 228 anuncios | [announcements.csv](data/normalized/announcements.csv) |
| Base relacional con todas las tablas | [layoffs.sqlite](data/normalized/layoffs.sqlite) |
| Consultar o editar las clasificaciones completas | [JSON canónico](2026-categorized.json) |
| Definiciones y límites | [Esquema](schema.md) · [Método](methodology.md) |
| Estado de calidad y organización | [Auditoría del repositorio](data/quality-review.md) |
| Evidencia adicional, cambios aplicados y límites restantes | [Seguimiento de 14 casos](research/ai-tracker-comparison/evidence-followup-2026-09-28.md) |

## Qué está vigente

Se cuentan **todas las razones atribuidas**, incluidas las generales: 206 anuncios tienen alguna explicación, 108 incluyen una razón de IA, 80 combinan IA con otra razón y 108 tienen varias razones. Los otros 22 no tienen una explicación clasificable. No son cifras de puestos causados por IA ni causas verificadas de forma independiente.

En los 235 registros internos hay 219 con fuentes revisadas, 14 parciales y 2 no recuperadas; dentro de los 228 del informe son 212, 14 y 2. El estado de revisión no implica corroboración independiente. Contexto, negaciones y causas permanecen separados.

La especificidad de una explicación se conserva en los datos para auditoría; no excluye casos del artículo, el explorador ni el estudio de contratación. [Ver análisis reproducible](research/full-analysis/README.md).



<!--AI-TRACKER-COMPARISON-->
## Nuestro dataset frente a Layoffs.fyi

**Partimos de sus etiquetas de IA y ampliamos la evidencia.** Una diferencia requiere una justificación documentada: otra ronda, distinto alcance, una corrección o información posterior sobre el mismo evento. No recuperar una noticia no basta para descartar su clasificación.

Comparación de **enero–junio de 2026**, usando el snapshot del AI Layoffs Tracker del **28 de septiembre de 2026**:

| Recuento | Layoffs.fyi — AI Layoffs Tracker | Nuestro análisis |
|---|---:|---:|
| Registros en el universo del semestre | 231 | 228 |
| Registros con vínculo atribuido a IA | 95 | 108 |
| Porcentaje de registros | 41,1% | 47,4% |

**¿De dónde sale la diferencia?** Coincidimos en 91 anuncios. Nosotros añadimos 17 con atribuciones documentadas fuera de su listado de IA; mantenemos diferente 1 (Verily, por una explicación de otra ronda) y excluimos 3 medidas de período de nuestro análisis de anuncios (Oracle, Dell y Multiverse).

- **Layoffs.fyi:** 91 coincidencias + 1 diferencia + 3 medidas de período = **95**.
- **Nuestro análisis:** 91 coincidencias + 17 incorporaciones = **108**.

Los universos completos no son idénticos. Tampoco debe confundirse este porcentaje de anuncios con el **82,8% de empleados en eventos etiquetados con IA** que resulta del snapshot del tracker para el semestre: ponderan unidades distintas.

En **11 de las 91 coincidencias** conservamos la atribución del tracker sin corroborar por separado su mecanismo. La fuente queda identificada; no se presenta como confirmación empresarial ni sustitución demostrada. La ausencia de nuestros 17 casos adicionales del listado tampoco demuestra que Layoffs.fyi los haya descartado.

**[Ver las diferencias caso por caso, las fuentes y el criterio de revisión](research/ai-tracker-comparison/README.md)** · [Cruce completo en CSV](research/ai-tracker-comparison/comparison.csv) · [Reproducir en Jupyter](notebooks/explorar_despidos.ipynb).
<!--/AI-TRACKER-COMPARISON-->

## Organización

- `2026-categorized.json`: base curada. Su CSV es una copia de compatibilidad con objetos anidados serializados; para DS usar `data/normalized/`.
- `data/normalized/`: tablas escalares, SQLite, SQL de ejemplo, esquema y manifest con hashes. Generado; no editar a mano.
- `report/`: artículos, explorador, figuras, descargas y sus generadores. `records.json` es una selección exacta del JSON canónico.
- `research/`: decisiones de revisión, fuentes recuperadas, taxonomías y análisis. Se utiliza para reproducir y justificar clasificaciones.
- `coverage/` y auditorías JSON: cadena de cambios y conciliación; necesarios para validar los registros.
- `notebooks/`: ejemplo exploratorio vigente en Jupyter, con resultados y versión HTML.
- `scripts/`: validación, exportación normalizada y resúmenes de revisión.
- El material histórico, los notebooks anteriores y las visualizaciones antiguas quedan fuera de Git; pueden conservarse localmente mediante las exclusiones de `.gitignore`.

Se conservan `2026-legacy-classifications.json`, las auditorías y `coverage/` porque el validador utiliza esa cadena para reconstruir la base actual. Los snapshots antiguos de ingestión sin dependencias en el pipeline vigente quedan excluidos de Git. Los ZIP se generan como entregables locales; no se versionan. Los posts editoriales de principales hallazgos se conservan solo en local; el repositorio prioriza datos, análisis reproducibles y gráficos.

## Reproducir y comprobar

```sh
python3 scripts/validate_causes.py
python3 scripts/build_review_report.py
python3 scripts/build_normalized.py
python3 report/build.py
```

La validación comprueba la cadena de auditoría, el JSON y su CSV. El build del informe regenera ambos idiomas, las figuras, el estudio de contratación y la exportación normalizada. Requiere las dependencias de visualización del proyecto; el exportador normalizado usa únicamente la biblioteca estándar de Python.

Cambiar el JSON es una decisión de curación: debe quedar respaldada por una fuente y registrada en la cadena de auditoría. Regenerar archivos no actualiza automáticamente las fuentes externas.

El informe está destinado a [trabajoremoto.cl](https://trabajoremoto.cl).

## Licencia

Datos: dominio público / fair use (citas de prensa pública).
Código: MIT.

## Trazabilidad de los hallazgos

El [notebook independiente](notebooks/explorar_despidos.html) reproduce recuentos, cruces, atribuciones, negaciones, cobertura y crecimiento previo; permite consultar evidencia de los ejemplos. El [mapa de respaldo](notebooks/respaldo-editorial.md) enlaza las afirmaciones de los artículos con esas consultas.

Después de regenerar los datos y artículos, ejecutar `python3 scripts/build_notebooks.py` para actualizar resultados, HTML y paquete independiente. Las comprobaciones de referencia fallan si cambian valores publicados; hay que revisar los textos antes de cambiar las expectativas.
