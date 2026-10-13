# Despidos tecnológicos de 2026

Datos curados y análisis exploratorio de **228 anuncios de enero a junio de 2026**, recopilados a partir de Layoffs.fyi y ampliados con fuentes empresariales y periodísticas. Se clasifican explicaciones atribuidas, no causas demostradas ni puestos sustituidos por IA.

## Por dónde empezar

| Etapa | Qué contiene | Archivo |
|---|---|---|
| Datos curados | 235 registros con fuentes, clasificaciones y decisiones de revisión | [2026-categorized.json](2026-categorized.json) |
| Datos para analizar | 228 anuncios seleccionados, tablas CSV y SQLite | [data/normalized](data/normalized/README.md) |
| Insumos complementarios | Historiales de plantilla, clasificación de industrias, snapshot del tracker y taxonomías | [research](research/README.md) |
| Exploración principal | Recuentos, razones, evidencia, cobertura, crecimiento y comparación con el tracker | [explorar_despidos.ipynb](notebooks/explorar_despidos.ipynb) |
| Comparaciones exploratorias | Cruces por razones, funciones, plantilla e industria; incluye resultados que no justifican un hallazgo | [exploracion_hallazgos.ipynb](notebooks/exploracion_hallazgos.ipynb) |
| Resultados para leer | Copias HTML ejecutadas de los dos notebooks | [Principal](notebooks/explorar_despidos.html) · [Comparaciones](notebooks/exploracion_hallazgos.html) |

**Los resultados publicados en este repositorio son los notebooks ejecutados y sus HTML.** Los artículos, PDF, diseños y gráficos editoriales se mantienen fuera de Git. No hay un sitio `report/` que deba consultarse para entender o ejecutar el análisis.

## Alcance

La base conserva 235 registros. El análisis excluye dos entradas de julio y cinco medidas históricas o de período. Quedan 228 anuncios: **108 con razones vinculadas con IA, 98 solo con otras razones y 22 sin explicación clasificable**. Las razones pueden solaparse.

Cobertura general conciliada: 17 de septiembre de 2026. Última revisión de evidencia: 29 de septiembre. Ejecutar el código no actualiza las fuentes externas.

- [Método y límites](methodology.md) · [Esquema y categorías](schema.md).
- [Diferencias frente a Layoffs.fyi y su justificación](research/ai-tracker-comparison/README.md).
- [Cadena de auditoría](data/audit/README.md): se conserva para validar cómo se llegó a las clasificaciones actuales; no es otro análisis vigente.

## Reproducir

```sh
python3 -m pip install -r notebooks/requirements.txt
python3 scripts/validate_causes.py
python3 scripts/build_normalized.py
python3 scripts/build_notebooks.py
```

El último comando ejecuta ambos notebooks en una carpeta temporal que contiene únicamente los insumos necesarios y actualiza sus resultados y HTML. No requiere `report/`, credenciales ni acceso a fuentes externas. Detalles en [notebooks/README.md](notebooks/README.md).

El JSON es la fuente de verdad. Su [CSV de compatibilidad](2026-categorized.csv) conserva objetos anidados como texto; para pandas, R o SQL, usar las tablas normalizadas. No editar las exportaciones a mano. Los cambios de clasificación deben tener evidencia y una entrada en la cadena de auditoría.

## Qué se conserva y qué se retira

Se conservan datos, evidencia necesaria, definiciones, dos análisis reproducibles y sus resultados. Se retiraron del árbol publicado los artículos, cachés de descarga, prototipos, resultados intermedios y scripts de curación de una sola ejecución. Los archivos retirados siguen recuperables en el historial de Git y pueden mantenerse en local mediante `.gitignore`.
