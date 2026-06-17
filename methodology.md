# Methodology — Layoffs 2026 Analysis

*Cómo se armó el dataset, qué fuentes se usaron, cómo se clasificó cada evento, y qué caveats tener en cuenta.*

Última actualización: 2026-05-27. Versión del dataset: snapshot 2026-05-26 de [layoffs.fyi](https://layoffs.fyi/).

---

## 1. Pipeline de data

El análisis se construyó en 9 fases. Cada fase produjo artefactos guardados en este repo para reproducibilidad.

### Fase 1 — Extracción raw de layoffs.fyi
- Fuente: el Airtable público de layoffs.fyi (URL: `app1PaujS9zxVGUZ4`).
- El share view de Airtable es un SPA con data cargada via JS — no scrappeable con WebFetch directo.
- **Workaround**: extraje el `accessPolicy` JSON embebido en la página inicial, luego llamé el endpoint `v0.3/view/{viewId}/readSharedViewData` con los headers correctos (`x-airtable-application-id`, etc.).
- Output: 4.420 layoff events totales (toda la historia layoffs.fyi). Filtré a `date >= 2026-01-01` → **160 eventos**.
- Archivo: [`2026-airtable-raw.json`](2026-airtable-raw.json)
- Labels select-field (Industry, Stage, Country, Location HQ): [`airtable-labels.json`](airtable-labels.json)

### Fase 2 — Enriquecimiento con razones públicas
- Cada evento tiene un campo `Source` con URL del medio que lo reportó.
- Splittee los 160 en 4 chunks de ~40 y lancé **4 agentes paralelos** que WebFetched cada URL y extrajeron la razón pública declarada.
- **Resultado**: 116 con razón recuperada, 44 con fuente bloqueada (paywalls de Bloomberg/Reuters/WSJ/NYT, X/Twitter posts, LinkedIn, etc.).
- Archivo intermedio: [`2026-reasons.json`](2026-reasons.json)

### Fase 3 — Recuperación de bloqueados en dos rondas

**Ronda 1** (los 12 más grandes): de los 44 bloqueados, los 12 con más personas cortadas eran críticos (Oracle 30k, Meta 8k+1.5k+700+200, PayPal 4.7k, Intuit 3k, Ericsson 1.6k, Snap 1k, Autodesk 1k, UKG 950, LinkedIn 875, Pinterest 700). Agente dedicado los recuperó vía WebSearch + Wayback Machine + SEC filings + medios locales. **Resultado: 12/12 recuperados.**

**Ronda 2** (priority cases adicionales): Después de la Ronda 1 quedaban 32 bloqueados (eventos chicos, mayormente <300 personas). Lanzé una segunda ronda sobre los 29 más significativos (>=100 personas o eventos en X/Twitter / fuentes self-hosted). **Resultado: 29/29 recuperados** vía outlets alternativos (Yahoo, GeekWire, Calcalist, Skift, Storyboard18, Decrypt, Music Business Worldwide, PetaPixel, etc.).

**Coverage final**:
- 145 / 160 eventos (90.6%) con razón pública identificada
- 15 eventos quedan `not_accessible` (eventos chicos, mayormente <100 personas, sin coverage alternativa)
- 10 eventos quedan `reason_primary = unknown` (subset de los 15 anteriores donde tampoco se podía inferir por slug)

- Archivos: [`2026_recovery_round2_results.json`](2026_recovery_round2_results.json) (ronda 2); ronda 1 está embebida en `2026-categorized.json` via el campo `source_used`.

### Fase 4 — Clasificación multi-eje
- Apliqué 3 ejes ortogonales + 1 columna estructural + 4 enriquecimientos opcionales. Ver `schema.md`.
- Implementación: [`categorize.py`](categorize.py) (rule-based + 14 manual overrides para casos high-confidence).
- Output: [`2026-categorized.json`](2026-categorized.json) y [`.csv`](2026-categorized.csv).

### Fase 5 — Análisis de profiles de los grandes
- Para Meta (4 rondas) y Oracle/PayPal/Amazon/Intuit/Snap: 2 agentes adicionales hicieron deep-research role-by-role.
- Output: [`meta-profile-breakdown.md`](meta-profile-breakdown.md), [`other-profiles-breakdown.md`](other-profiles-breakdown.md).

### Fase 6 — Cross-reference con The Pragmatic Engineer
- Source: [State of the software engineering job market in 2026](https://newsletter.pragmaticengineer.com/p/state-of-eng-market-2026), Gergely Orosz + Jessica Salmon, 26-may-2026.
- Data: Workforce.ai 2-yr SWE headcount growth, por empresa (May 2024 → May 2026).
- Aplicado a la columna `hire_overcorrection` (bool) — solo 11 de 160 eventos tienen valor por cobertura limitada del paper.
- Archivo: [`market-2026.md`](market-2026.md) (texto completo del deepdive).

### Fase 7 — LATAM via Get on Board public API
- Source: 9 endpoints públicos de `getonbrd.com/api/v0/insights/`.
- Tipo de cambio USD/CLP: scraped de `sii.cl/valores_y_fechas/dolar/` (semestre 2022-H1 a 2026-H1).
- CPI Chile: data anual INE Chile (vía Trading Economics como agregador).
- Archivos en [`getonboard/`](getonboard/).

### Fase 8 — Charts
- 10 PNG charts generados con matplotlib. Script: [`charts.py`](charts.py).
- Output: [`charts/`](charts/).

### Fase 9 — Newsletter + HTML
- Markdown drafts: [`top-findings.md`](top-findings.md) (EN), [`top-findings-es.md`](top-findings-es.md) (ES).
- HTML build: [`build_html.py`](build_html.py) → [`top-findings-es.html`](top-findings-es.html) (newsletter-ready, self-contained con CSS inline).

---

## 2. Fuentes de noticias usadas

### Distribución de `narrative_source` (calidad de evidencia, después de Ronda 2)

| Calidad | Eventos | Cómo se determinó |
|---|---:|---|
| `ceo_memo` | 12 | Memo leak con quote atribuida (Bosworth, Zuckerberg, Spiegel, Dorsey, Appoo, Ellison, Woodside, Mehrotra, etc.) |
| `press_release_sec` | 3 | SEC filing (8-K, annual report) o press release oficial |
| `news_with_quote` | 14 | Article con cita atribuida de exec/portavoz |
| `news_inferred` | 116 | Coverage clara pero sin cita directa |
| `not_accessible` | 15 | Eventos chicos sin coverage alternativa después de 2 rondas de recovery |

### Top 20 dominios fuente originales (layoffs.fyi reporting)

| Domain | Events | Tier |
|---|---:|---|
| calcalistech.com | 21 | Israel tech press (CTech) |
| reuters.com | 8 | Tier-1 (paywalled) |
| bloomberg.com | 7 | Tier-1 (paywalled) |
| cnbc.com | 6 | Tier-1 (paywalled) |
| inc42.com | 6 | India startups |
| finance.yahoo.com | 6 | Aggregator |
| techcrunch.com | 6 | Tier-2 |
| businessinsider.com | 5 | Tier-2 (paywalled) |
| bizjournals.com | 5 | Local US business |
| linkedin.com | 4 | Memo posts |
| betakit.com | 4 | Canada tech |
| entrackr.com | 3 | India startups |
| globes.co.il, geektime.co.il | 4 | Israel tech press |
| thekenyatimes.com | 2 | Kenya local |
| wsj.com | 2 | Tier-1 (paywalled) |
| variety.com | 2 | Entertainment (Snap, gaming) |
| nytimes.com | 2 | Tier-1 (paywalled) |

### Fuentes de recovery (los 12 blocked más grandes)

Cuando la URL original era paywall, se buscó alternativa:

| Dominio alternativo | Casos | Para qué |
|---|---:|---|
| techcrunch.com | 3 | Intuit (5/20), Meta Jan Reality Labs, Pinterest |
| dataconomy.com, fortune.com | 2 | Meta May 8k, Meta Mar 700 |
| hcamag.com | 1 | LinkedIn 875 (Reuters paywall workaround) |
| variety.com | 1 | Snap 1k |
| cbs12.com | 1 | UKG 950 (Florida local outlet) |
| thenextweb.com | 1 | Oracle 30k |
| layoffhedge.com | 1 | PayPal 4.76k |
| sec.gov | 1 | Autodesk 8-K filing |
| thelocal.se | 1 | Ericsson 1.6k (Swedish English-language) |

### Enumeración completa de fuentes

El dataset usó **105 dominios de noticias únicos** en total: 80 como fuente original de layoffs.fyi + 32 como fuente de recovery (algunos se solapan).

**Por-evento auditável**: la lista completa de los 160 eventos con su fuente original + fuente recovery está en [`sources.md`](sources.md) — un mapping fila-por-fila para que cualquier claim del análisis se pueda rastrear a su fuente.

**Las 80 fuentes originales** se reparten en tiers:
- **Tier-1 wire/business** (paywall): Reuters (8), Bloomberg (7), CNBC (6), WSJ (2), NYT (2), Business Insider (5), LA Times (2), Seattle Times, SF Chronicle, Axios, Morningstar.
- **Israel tech press**: Calcalist/calcalistech (21 — el dominio #1), Globes (2), GeekTime (2). Refleja la alta proporción de layoffs en tech israelí (Wix, Pentera, Foretellix, AI21, Tipalti, Guesty, LSports).
- **India startups**: inc42 (6), entrackr (3), yourstory, moneycontrol, whalesbook.
- **Tech press global**: TechCrunch (6), The Verge, The Register, Axios, The Block, CoinDesk, Decrypt.
- **Canada / regional**: BetaKit (4), The Logic, Crain's Cleveland, Boston.com, Sun-Sentinel, IBJ.
- **Vertical / nicho**: Variety (2, entertainment), Propmodo (proptech), Music Business Worldwide, PetaPixel (cameras), Business of Fashion, AIM Group / Next.io (gaming), EdTech Innovation Hub.
- **Company-direct**: blogs.cisco.com, blog.cloudflare.com, bill.com, upwork.com, aboutamazon.com, asml.com, epicgames.com, ir.angi.com, quorablog.quora.com, x.com (4 posts), linkedin.com (4 memos).

**Las 32 fuentes de recovery** (cuando la original era inaccesible) — top: TechCrunch (5), TheNextWeb (3), GeekWire (3), Calcalist (2), más Fortune, Benzinga, Skift, Music Business Worldwide, Decrypt, Unchained, Breakit (SE), HCAMag, SalesforceBen, TechBuzz, Crain's, SEC.gov, The Local (SE), entre otros.

### Cobertura de fuentes por evento (después de 2 rondas de recovery)

- **145 eventos** (90.6%) tienen razón pública recuperada con cita o coverage clara.
- **15 eventos** (9.4%) quedaron en `not_accessible` — eventos chicos (mayoría < 100 personas) sin coverage alternativa después de 2 rondas.
- **10 eventos** quedan en `reason_primary = unknown` (subset donde tampoco se pudo inferir por slug del URL).

---

## 3. Metodología de clasificación

### Schema de ejes ortogonales

Detalle completo en [`schema.md`](schema.md). Resumen:

| Eje | Tipo | Valores | Aplicación |
|---|---|---|---|
| `reason_primary` | single-value | 15 valores | Causa raíz financiera/estratégica declarada por la empresa |
| `ai_link` | single-value | 6 valores | Relación al ciclo AI (sustitución, capex, denied, etc.) |
| `narrative_source` | single-value | 6 valores | Calidad de la evidencia (memo, quote, inferred) |
| `ai_position` | single-value | 6 valores | Posición económica estructural en mercado AI (seller, buyer, vertical builder, hybrid, n/a) |
| `hire_overcorrection` | bool/null | True/False/null | ¿El cut corrige overhire previo? (cross-ref Workforce.ai) |
| `reassignment_observed` | bool/null | True/False/null | ¿Se observan redeployments en lugar de cuts? |
| `profiles_cut`, `profiles_hired` | list | tags | Roles específicos afectados (donde hay deep research) |

### Rule-based + manual override hybrid

La función `classify_reason_primary()` en `categorize.py` aplica patrones regex sobre el reason text recuperado:

```python
# Ejemplo simplificado del rule chain
if "shutdown" in text or pct == 1.0 → "shutdown_bankruptcy"
elif "redirect" in text + "ai infrastructure" → "ai_capex_reallocation"
elif "smaller teams using ai" → "ai_substitution_claim"
elif "new CEO" + named (Lores, Shapero, Morgan) → "new_ceo_turnaround"
elif "restructuring" + "aligning" → "restructuring_vague"
# ... 12 más
```

**Manual overrides** (14 casos high-confidence donde el rule-based no captura bien el matiz):
- Meta × 4 rondas (cada una con `profiles_cut`/`profiles_hired` específicos)
- Oracle, PayPal, Amazon, Intuit, Snap (los 5 con deep-research)
- Atlassian, Shopify (override en `hire_overcorrection`)
- Cloudflare (re-clasificado de capex_funding a direct_substitution)
- Wix (re-clasificado a cost_cutting tras revisar el reason)

Para `ai_position`, la clasificación es **keada por empresa**, no por evento (la posición estructural no cambia entre rondas de layoff de la misma compañía).

### Casos borderline conocidos

- **MercadoLibre**: inicialmente `vertical_builder`, reclasificado a `token_buyer` por no cumplir el criterio estricto (no foundation models propios, no silicon, no datacenters a escala). Documentado en `categorize.py`.
- **Amazon**: borderline entre `hybrid` y `vertical_builder` (Trainium + Nova + AGI team son construcción vertical pero AWS vende). Final: `hybrid`.
- **Atlassian**: borderline entre `hybrid` y `token_buyer` (Rovo AI vendido pero usa Anthropic underneath). Final: `hybrid`.
- **Cloudflare**: Workers AI inference puede ser sold pero el reason del layoff fue interno. Marcado `hybrid`.

---

## 4. External datasets utilizados

### Workforce.ai vía The Pragmatic Engineer
- **Para qué**: `hire_overcorrection` flag.
- **Cobertura**: ~10 empresas grandes US (Meta, Apple, Google, Microsoft, Amazon, Shopify, Stripe, Atlassian, Snap, Spotify).
- **Métrica**: SWE headcount % growth, ventana May 2024 → May 2026.
- **Threshold**: ≥+15% growth = hire_overcorrection: True.
- **Limitación**: para 149 de 160 eventos, no hay data → `hire_overcorrection: null`.

### Get on Board API (LATAM)
- **Para qué**: análisis salarial LATAM, AI skills evolution, junior collapse.
- **Endpoints usados** (9 working):
  - `expected_vs_offered_salaries`
  - `placement_rate_per_tags`
  - `tags_cloud_per_categories`
  - `offered_jobs_by_seniority`
  - `offered_jobs_by_category`
  - `offered_jobs_by_category_by_seniority`
  - `offered_jobs_by_headcounts`
  - `offered_jobs_by_remote_modality`
  - `offered_technologies_across_time_by_seniority`
- **Endpoints discovered pero rotos** (HTTP 500): los 7 `talent_supply_*` y `demanded_technologies_across_time_by_seniority`. Documentado en `getonboard/`.
- **Cobertura**: ~7,500 job postings/año en plataforma GoB, LATAM agregado.
- **Caveat**: el universo GoB ≠ todo el LATAM. LinkedIn directo y referidos no medidos.

### SII Chile — tipo de cambio USD/CLP
- **Para qué**: convertir salarios GoB (USD) a CLP nominal por semestre.
- **URL pattern**: `sii.cl/valores_y_fechas/dolar/dolar{year}.htm`
- **Parsing**: extracción de daily rates por regex, split por mitades para semester averages.
- **Caveat**: aproximación — split por mitad no es exacto (Q1 trading days ≠ Q4 trading days).

### INE Chile — CPI anual
- **Para qué**: deflactar CLP nominal a CLP real (poder adquisitivo).
- **Source**: data anual INE Chile vía Trading Economics como agregador secundario.
- **Years**: 2022 (11.6%), 2023 (7.6%), 2024 (4.3%), 2025 (~4%), 2026 H1 (~1.5%).
- **Caveat**: 2025-26 son estimaciones; pueden mover ±1pp el cálculo final de cumulative deflator.

### Web search para data adicional
- Uber AI budget exhaustion → Fortune, Briefs, AI Magazine (2026-05-26)
- Microsoft cancela Claude Code → People Matters, Windows Central
- GitHub Copilot pricing → GitHub blog oficial
- $300B Oracle-OpenAI contract → DCD, Built In, Tomasz Tunguz analysis

---

## 5. Reproducibilidad

Toda la cadena es reproducible localmente:

```bash
# Comando único: regenera todos los artefactos derivados en orden
python3 build_all.py            # categorize → charts → build_html
python3 build_all.py --quiet    # sin los cross-tabs verbosos

# O paso por paso si querés debuggear uno:
python3 categorize.py   # → 2026-categorized.{json,csv} + sources.md
python3 charts.py       # → charts/*.png
python3 build_html.py   # → top-findings-es.html
```

**Fuente de verdad**: `2026-enriched.json` (más el dict de overrides en `categorize.py`). Los artefactos derivados — `2026-categorized.{json,csv}`, `sources.md`, `charts/*.png`, `top-findings-es.html` — **no se editan a mano**; se regeneran con `build_all.py`.

Re-fetch de raw data (solo si caducó):
- **layoffs.fyi**: ya en `2026-airtable-raw.json`. Re-extracción requiere refrescar el `accessPolicy` token de Airtable.
- **GoB / SII**: re-descargables con curl (lista de endpoints en sección 4).

Archivos clave para auditoría:
- [`2026-categorized.csv`](2026-categorized.csv) — vista plana en Excel/Sheets
- [`2026-categorized.json`](2026-categorized.json) — vista estructurada con todos los campos
- [`categorize.py`](categorize.py) — toda la lógica de clasificación + overrides en una sola file ~700 líneas

---

## 6. Limitaciones conocidas

### Del dataset original
- **layoffs.fyi sub-representa empresas no-US**. Las empresas que reportan layoffs a layoffs.fyi son mayoritariamente del ecosistema VC US/Israel. LATAM está sub-representado (2 empresas) vs el peso real del fenómeno.
- **`# Laid Off` es self-reported o inferido**. No hay verificación independiente; algunos eventos tienen `null` count cuando el medio no reporta número.
- **`%` es a veces porcentaje de toda la empresa, a veces de una división**. layoffs.fyi no distingue.

### De la clasificación
- **`reason_primary` es single-valued**. Eventos con múltiples drivers simultáneos (ej. Meta May: AI capex + middle management + hire correction + new strategy memo) quedan reducidos a uno solo. Capturamos los demás en `ai_link` + `hire_overcorrection`, pero la primary se simplifica.
- **`hire_overcorrection` solo cubre 11/160 eventos**. Los demás 149 son null porque no hay Workforce.ai data — no significa False, significa unknown.
- **Las CEOs declaraciones son self-serving**. Que un memo diga "AI-first" no prueba que el motivo real sea AI; sí prueba que esa es la narrativa pública que la empresa elige. El bucket `ai_denied_but_adjacent` captura esto.

### Del análisis LATAM
- **Chile como proxy de LATAM**. Para el ajuste FX+CPI usé datos chilenos. Argentina (peso colapsado), Brasil (real más estable), Colombia (intermedio) tendrían números distintos. La dirección y magnitud relativa cross-roles se mantiene, los números absolutos varían por país.
- **Get on Board es uno de varios job boards**. Concentrado en LATAM tech remoto/hybrid; no captura In-office puro local de cada país.
- **Junior collapse podría tener efectos de muestra**. La caída de 31% a 9% es dramática pero también el total de postings cayó ~30% — parte del efecto podría ser composición de quién publica en GoB, no del mercado real.

### Del framing
- **"AI capex reallocation" vs "AI substitution"** es una distinción analítica nuestra. Una empresa puede genuinamente combinar ambas en un solo memo. La clasificación elige el dominante.
- **"Vertical builder" tiene umbral arbitrario**. ¿Cuánto silicon propio se necesita? ¿Cuánto capex? En la práctica, Meta es la única clara en el dataset; Apple/Tesla/ByteDance califican pero no están. La frontera con `hybrid` puede ser borrosa para empresas de tamaño medio.

---

## 7. Versionado y updates

Este análisis es un **snapshot de 2026-05-26 / 2026-05-27**. Cosas que pueden cambiar:

- Más eventos 2026 publicados después de mayo (la segunda mitad del año podría tener picos en Q3, históricamente la peor temporada para layoffs).
- Empresas en `unknown` que liberen información (rompiendo paywalls, leaks, etc.) → upgrade de su clasificación.
- Empresas en `hire_overcorrection: null` que aparezcan en data Workforce.ai futura → flag se llena.
- Reclasificaciones de borderline cases (ya pasó: MercadoLibre).

Para mantener el análisis vivo: re-correr el pipeline cuando hay un evento significativo nuevo. La estructura del repo soporta updates incrementales sin re-trabajo.

---

## 8. Contacto y feedback

Este es un análisis exploratorio en colaboración con Claude. Si encontrás errores, fuentes alternativas, o argumentos contra alguna clasificación, los caveats están escritos para que cuestionar puntos específicos sea fácil.

Áreas donde feedback sería más útil:
- **Reclasificaciones de borderline cases** (revisar el dict en `categorize.py`)
- **Cobertura de fuentes recovered** para los 32 que quedaron en `unknown` (especialmente PayPal Chicago/Omaha y Meta Apr WARN)
- **Validación cross-país de la curva salarial LATAM** (Chile como proxy puede ser engañoso para Argentina/Brasil)
- **Verificación de cifras de capex AI** (Meta $125-145B, Oracle $50B, Amazon ~$100B) — son guías de empresa que pueden revisarse
