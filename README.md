# 2026 Tech Layoffs: dataset categorizado

Dataset auditable de los layoffs tech del primer semestre de 2026 (enero a
junio, 161 eventos en la ventana `date < 2026-07-01`). Cada evento tiene
causas clasificadas (`causes`) y un veredicto sobre el reclamo de sustitución
por IA (`ai_claim_verdict`), sobre los ejes base `reason_primary`, `ai_link`,
`ai_link_basis`, `narrative_source`, `ai_mention`. El dataset parte de un scrape de
[layoffs.fyi](https://layoffs.fyi) y luego se curó a mano, evento por evento. Cada dato
del análisis y su consulta están en `verificacion.md` y `auditoria-sobrecontratacion.md`.

Este repo contiene el dataset y la metodología. El reporte construido
sobre estos datos será publicado en [trabajoremoto.cl](https://trabajoremoto.cl).

## Estructura

| Archivo | Qué es |
|---|---|
| `methodology.md` | Cómo se construyó el dataset, paso a paso |
| `schema.md` | Definición de los ejes y tags de clasificación |
| `verificacion.md` | Cada dato agregado del análisis, con su consulta |
| `auditoria-sobrecontratacion.md` | La sobre-contratación como trayectoria (por qué no es un porcentaje) |
| `sources.md` | Fuente original (URL) de cada evento del dataset |
| `2026-airtable-raw.json` | Snapshot del Airtable de layoffs.fyi |
| `2026-reasons.json` | Razones públicas recuperadas por empresa |
| `2026_recovery_round2_results.json` | Recovery de URLs con paywall |
| `2026-enriched.json` | Fuente de verdad: raw + razones + overrides |
| `2026-categorized.json` / `.csv` | Dataset curado a mano (fuente de verdad) |
| `airtable-labels.json` | Etiquetas de campos del Airtable original |

## Sobre el dataset

`2026-categorized.json` es un dataset curado a mano y final, no la salida de
un script. El método completo (reglas de clasificación, overrides manuales,
adjudicación con fuentes primarias) está descrito paso a paso en
`methodology.md`.

## Licencia

Datos: dominio público / fair use (citas de prensa pública).
Código: MIT.
