# Análisis descriptivo del conjunto completo

Se recalculan las frecuencias de las 24 razones, todos sus pares, atribuciones, alcance, funciones y cobertura sectorial desde los 228 anuncios del primer semestre. No se excluye ninguna razón por su nivel de detalle. La selección de hallazgos se hace después de generar los cruces; no se buscan únicamente los pares del artículo anterior.

## Hallazgos respaldados

- 201 anuncios tienen alguna explicación; 27 no tienen una clasificable.
- 72 incluyen IA: 48 junto a otra razón y 24 solo con razones de IA registradas.
- 79 contienen varias razones. Ahorro + consolidación (13), productividad con IA + ahorro (12), y dificultades financieras + cierre (9) son los pares más frecuentes.
- Productividad con IA aparece en 24 anuncios y sustitución en 8. Esto compara explicaciones, no puestos ni resultados reales.
- Las atribuciones de productividad proceden de la empresa en 22 de 24 casos; inversión en 12 de 14, y transición hacia IA en 10 de 13. No demuestra que sean correctas.
- 9 de 10 anuncios con dificultades financieras incluyen cierre; 9 de los 14 cierres incluyen dificultades financieras.
- En 57 de 72 anuncios con IA no se identifican funciones afectadas. Ingeniería y producto aparecen con IA en 8 anuncios cada uno, marketing en 6; no son tasas de riesgo profesional.
- La comparación de contratación incluye ahora todas las razones. Medianas 2019–2022: IA +79,84% (15 empresas), otras +50,87% (18). Medianas 2022–2025: IA +3,72% (28), otras +4,69% (38). Cambian las empresas observables y no se estima contratación excesiva.

## Interpretaciones no respaldadas

No inferimos productividad realizada, sustitución individual, porcentaje de puestos causado por IA, diferencias representativas entre industrias (66 anuncios sin industria), ni entre empresas públicas y privadas. No se observa una población de comparación de empresas sin recortes. Las razones generales no se recodificaron exhaustivamente junto a todas las decisiones específicas; sus frecuencias describen el registro, no toda la retórica empresarial. No se transforma la especificidad de una fuente en un comportamiento empresarial.

## Reproducibilidad

Ejecutar `python3 research/full-analysis/analyze.py`; `results.json` y `report/analysis.json` incluyen los IDs de cada razón y par. `python3 report/build.py` regenera el análisis, artículos, figuras, exploradores y estudio de contratación. Las anotaciones de especificidad se conservan en el dataset. No se modificaron clasificaciones ni cifras de personal para este análisis.
