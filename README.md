# 2026 Tech Layoffs — dataset categorizado

Dataset auditable de los layoffs tech del primer semestre de 2026 (Ene–Jun,
**161 eventos** en la ventana `date < 2026-07-01`) con clasificación multi-causa
por evento (`causes`) y un veredicto sobre el reclamo de sustitución por IA
(`ai_claim_verdict`), sobre los ejes base `reason_primary`, `ai_link`,
`ai_link_basis`, `narrative_source`, `ai_position`. Pipeline reproducible desde el
scrape original de [layoffs.fyi](https://layoffs.fyi). La reproducción de cada dato
del análisis está en `verificacion.md` y `auditoria-sobrecontratacion.md`.

Este repo contiene el **dataset y la metodología**. El reporte construido
sobre estos datos será publicado en [trabajoremoto.cl](https://trabajoremoto.cl).

## Estructura

| Archivo | Qué es |
|---|---|
| `methodology.md` | Cómo se construyó el dataset, paso a paso |
| `schema.md` | Definición de los ejes y tags de clasificación |
| `verificacion.md` / `.py` | Reproduce cada dato agregado del análisis, con su consulta |
| `auditoria-sobrecontratacion.md` | La sobre-contratación como trayectoria (por qué no es un porcentaje) |
| `sources.md` | Fuente original (URL) de cada evento del dataset |
| `categorize.py` | Lógica de clasificación (regex + overrides manuales) |
| `2026-airtable-raw.json` | Snapshot del Airtable de layoffs.fyi |
| `2026-reasons.json` | Razones públicas recuperadas por empresa |
| `2026_recovery_round2_results.json` | Recovery de URLs con paywall |
| `2026-enriched.json` | Fuente de verdad: raw + razones + overrides |
| `2026-categorized.json` / `.csv` | Output de `categorize.py` |
| `airtable-labels.json` | Etiquetas de campos del Airtable original |

## Reproducir el dataset

```bash
python3 categorize.py
```

Lee `2026-enriched.json` y genera `2026-categorized.{json,csv}` + actualiza
`sources.md`. Las correcciones manuales viven en el dict `MANUAL` dentro
de `categorize.py` — no editar los JSON derivados a mano.

## Licencia

Datos: dominio público / fair use (citas de prensa pública).
Código: MIT.
