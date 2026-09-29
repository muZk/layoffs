# Análisis descriptivo del conjunto completo

Se recalculan las frecuencias de las 24 razones, todos sus pares, atribuciones, alcance, funciones y cobertura sectorial desde los 228 anuncios del primer semestre. No se excluye ninguna razón por su nivel de detalle. La selección de hallazgos se hace después de generar los cruces; no se buscan únicamente los pares del artículo anterior.

## Hallazgos respaldados

- 206 anuncios tienen alguna explicación; 22 no tienen una clasificable.
- 108 incluyen IA: 80 junto a otra razón y 28 solo con razones de IA registradas.
- 108 contienen varias razones. Ahorro + consolidación (13), productividad con IA + ahorro (13), y dificultades financieras + cierre (9) son los pares más frecuentes.
- Productividad con IA aparece en 25 anuncios y sustitución en 8. Esto compara explicaciones, no puestos ni resultados reales.
- Las atribuciones de productividad proceden de la empresa en 23 de 25 casos; inversión en 19 de 25, y transición hacia IA en 14 de 34. No demuestra que sean correctas.
- 9 de 10 anuncios con dificultades financieras incluyen cierre; 9 de los 14 cierres incluyen dificultades financieras.
- En 80 de 108 anuncios con IA no se identifican funciones afectadas. Ingeniería aparece con IA en 15 anuncios, producto en 12 y marketing en 9; no son tasas de riesgo profesional.
- Medianas de contratación: 2019–2022, IA +88,2% (22 empresas), otras +22,0% (12); 2022–2025, IA +6,7% (40), otras +3,7% (27). Cambian las empresas observables; no se estima contratación excesiva.

## Interpretaciones no respaldadas

No inferimos productividad realizada, sustitución individual, porcentaje de puestos causado por IA, diferencias representativas entre industrias (66 anuncios sin industria), ni entre empresas públicas y privadas. No se observa una población de comparación de empresas sin recortes. Las razones generales no se recodificaron exhaustivamente junto a todas las decisiones específicas; sus frecuencias describen el registro, no toda la retórica empresarial. No se transforma la especificidad de una fuente en un comportamiento empresarial.

## Reproducibilidad

Ejecutar `python3 research/full-analysis/analyze.py`; `results.json` y `report/analysis.json` incluyen los IDs de cada razón y par. `python3 report/build.py` regenera el análisis, artículos, figuras, exploradores y estudio de contratación. Las anotaciones de especificidad se conservan en el dataset. Las clasificaciones siguen la política de partir del tracker y conservar ampliaciones y excepciones documentadas. Once vínculos generales dependen solo de su clasificación. No se modificaron cifras de personal.

## Selección editorial

El análisis desarrolla tres temas: trayectorias previas de plantilla, vías de impacto de IA y consolidación organizacional. Los cruces de ahorro quedan como contexto; negaciones y cobertura de funciones se utilizan como límites de interpretación, no como hallazgos principales separados. ZoomInfo aporta un ejemplo de productividad y cambio de mercado; Oracle, una atribución periodística de inversión con alcance de plan.
