# Insumos de investigación utilizados

Esta carpeta contiene material que todavía usan los análisis o que justifica sus clasificaciones. No contiene artículos finales.

| Carpeta | Insumos vigentes | Uso |
|---|---|---|
| `hiring/` | `company-history.json`, `industry-review.json` | Series de plantilla con fuentes y exclusiones; clasificación exploratoria de industrias |
| `ai-tracker-comparison/` | Snapshot, decisiones, explicación de diferencias y cruce reproducible | Comparación con Layoffs.fyi |
| `functions/` | `taxonomy.json` | Vocabulario de funciones; exportación y validación |
| `explanations/` | `taxonomy.json` | Vocabulario de explicaciones generales; validación |

Las URL y notas de evidencia permanecen en los registros curados y estos insumos. Las cachés de páginas descargadas, prototipos y scripts de aplicación única ya no forman parte del árbol publicado. El historial de cambios de clasificaciones se conserva en `data/audit/` y `coverage/`, porque el validador lo utiliza.

`ai-tracker-comparison/comparison.csv` y `summary.json` son resultados auxiliares de conciliación, regenerados con `python3 research/ai-tracker-comparison/compare.py`. No son nuevas fuentes independientes.
