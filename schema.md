# Layoffs 2026 — Categorization Schema

Three orthogonal axes plus four optional enrichment columns. Applied to 160 entries from the layoffs.fyi public Airtable, filtered to 2026 events.

## Source files

| File | What it is |
|---|---|
| `2026-airtable-raw.json` | Raw 160 entries from the layoffs.fyi public Airtable share view (extracted via the `readSharedViewData` endpoint). Industry/stage/country are still in select-ID form. |
| `airtable-labels.json` | The ID-to-label maps for the Industry / Stage / Country / Location HQ select columns. |
| `2026-enriched.json` | 160 entries enriched with resolved labels and the public reason recovered from each source URL. |
| `2026-reasons.json` | The intermediate file with `reason` + `theme_original` per entry (before our 3-axis categorization). |
| `2026-categorized.json` | **The main artefact.** Full structured records with all 3 axes + enrichment columns. |
| `2026-categorized.csv` | Flat tabular version (good for spreadsheet ingest). |
| `meta-profile-breakdown.md` | Hand-researched role-by-role detail for Meta's 4 rounds. |
| `other-profiles-breakdown.md` | Same for Oracle / PayPal / Amazon / Intuit / Snap. |
| `categorize.py` | The categorizer (rule-based + manual overrides). Re-runnable. |
| `market-2026.md` | Pragmatic Engineer / Workforce.ai data on hiring trends — context for the `hire_overcorrection` flag. |

## Axis 1 — `reason_primary` (single value, financial root cause)

What's actually moving cash flow. Mutually exclusive — picking one forces the analyst to identify the dominant mechanism.

| value | meaning | canonical example |
|---|---|---|
| `ai_capex_reallocation` | OpEx (payroll) cut to fund AI capex (GPUs, datacenters, training). Requires explicit "redirect / shift investment toward AI" + concrete capex target. | Oracle 30k → Stargate |
| `ai_substitution_claim` | CEO publicly claims AI does the work of cut employees. Substitution is the framing. | Block, WiseTech, Snap |
| `cost_cutting` | Generic margin / cost discipline. AI may be present but not the engine. | Bill.com, Ericsson, Wix |
| `path_to_profitability` | Specific cash-flow / profit target stated publicly. | Ocado £150M, GoCardless |
| `new_ceo_turnaround` | A new CEO uses the layoff as a signaling event. AI / cost framing may follow but the trigger is leadership change. | PayPal (Lores), LinkedIn (Shapero), UKG (Morgan) |
| `restructuring_vague` | "Aligning with strategic priorities" / "reducing layers" — no specific mechanism stated. Largest catch-all. | Amazon, Intuit, ASML, Expedia |
| `m_and_a_consolidation` | Cuts driven by overlapping roles post-acquisition. | CyberArk (Palo Alto), Verint (Thoma Bravo), Vimeo (Bending Spoons) |
| `ipo_prep` | Streamlining ahead of a stated IPO. | Adda247, Axonius |
| `strategic_pivot` | Company changes its market / product (incl. into AI as a market). | Atlassian, Hailo→robotics, Supernal, Digg |
| `shutdown_bankruptcy` | 100% layoff — company closes. | Entropy, Yupp, Parker, Rec Room |
| `lost_contract_market_exit` | Specific client lost or specific country / market exited. | Sama (lost Meta), Deliveroo (DoorDash exiting Qatar) |
| `geographic_relocation` | Pure offshoring / HQ shift, no headcount-down strategy. | MessageBird (EU → US), One Identity (Germany → abroad) |
| `regulatory` | Regulatory change forces the cut. | Zupee (Indian online-gaming law) |
| `demand_collapse` | Market for the product shrank. | Ericsson (5G capex slowdown), Epic Games (Fortnite engagement), Remarkable |
| `unknown` | Public source wasn't accessible. | The 32 paywall-blocked entries we couldn't recover |

## Axis 2 — `ai_link` (relationship to the AI cycle)

How AI shows up in the story, independent of root cause. Separates the AI question from the financial question.

| value | meaning |
|---|---|
| `direct_substitution` | "AI does the work" — public and explicit (Block, WiseTech, Cloudflare, Snap). |
| `capex_funding` | "We're cutting to fund GPU / training infrastructure" (Oracle, Meta, PayPal). |
| `ai_pivot_market` | The company's *product* is shifting to AI as the new market (Hailo, Digg, StarkWare, Atlassian). |
| `ai_denied_but_adjacent` | Public denial of AI as the cause, OR vague restructuring where AI surfaces in the framing without being declared the engine (Intuit, LinkedIn, Dell, ASML). |
| `unrelated` | Genuinely not AI-driven (Ericsson 5G, Sama lost contract, regulatory, pure M&A consolidation). |
| `unknown` | Can't tell — source blocked. |

## Axis 3 — `narrative_source` (evidence quality)

How well-sourced the public reason is. Filter on this when you need defensible claims.

| value | meaning |
|---|---|
| `ceo_memo` | Public or leaked memo with attributed quote. Highest confidence. |
| `press_release_sec` | Filing / earnings call / company blog (official). |
| `news_with_quote` | News article with a quote from a named exec or spokesperson. |
| `news_inferred` | Coverage exists but without direct quotes. |
| `slug_only` | URL slug or aggregator headline only (rare — not produced by current rules). |
| `not_accessible` | Paywall / X-Twitter / blocked — original source unreadable, no alternative found. |

## Axis 4 — `ai_position` (structural relationship to the AI economy)

The 4th axis was added after distinguishing token-buying from GPU/silicon-buying. A company that PAYS Anthropic per token (Uber, PayPal) is in a fundamentally different economic position from one that BUILDS its own foundation models on its own infrastructure (Meta).

Keyed by company, not by date (this is structural, not per-round).

| value | meaning | what happens when AI demand/cost rises |
|---|---|---|
| `compute_seller` | Sells compute / cloud AI / model APIs to third parties (Oracle, Snowflake, AI21 Labs, DeepL, C3.ai, Firebolt). | Revenue ↑ — they're the supply side. |
| `infra_seller` | Sells hardware, silicon, networking, or data services that enable AI (Cisco, Dell, ASML, Sama, Hailo, Foretellix). | Revenue ↑ — picks-and-shovels. |
| `vertical_builder` | Builds own AI stack end-to-end (foundation models + silicon + datacenters) for own products. **Strict criterion**: foundation models + own silicon + hyperscaler-scale capex. In our 2026 layoffs dataset, **Meta is the only company that qualifies** — Apple, Tesla, ByteDance would qualify but had no 2026 layoffs. Companies like MercadoLibre, Spotify, Netflix train task-specific models but don't reach this bar and are classified `token_buyer` instead. | Cost ↑ (Nvidia exposure), but no token-price exposure. Bets value flows through downstream products. |
| `token_buyer` | Pays third-party providers (Anthropic, OpenAI, Microsoft) through APIs / partnerships (PayPal, Intuit, Snap, Pinterest, Coinbase, ZoomInfo, Block, WiseTech, dozens more). | Margin squeeze — the Uber paradigm. |
| `hybrid` | Combines two or more of the above (Amazon AWS+Bedrock+Trainium+Nova, Cloudflare Workers AI + internal usage, Microsoft Azure, Atlassian Rovo, LinkedIn via Azure). | Mixed exposure. |
| `n/a` | AI is not material to the business model — telecom, EVs, consumer fitness, fashion, etc. | No AI exposure. |

## Enrichment columns (optional, sparse)

These are filled in only where deep research exists — currently the ~9 manually-researched company-rounds (Meta×4, Oracle, PayPal, Amazon, Intuit, Snap, Atlassian, Shopify, Cloudflare, Wix).

| column | type | what it captures |
|---|---|---|
| `profiles_cut` | list[str] | Specific job functions / teams / levels cut. Tags like `middle_management`, `SDE_II`, `recruiting`, `VR_game_studios_shutdown`, `Reality_Labs`, `support_ops`. |
| `profiles_hired` | list[str] | Specific functions being hired into. Tags like `AI_researchers_foundation_models`, `data_center_technicians_no_degree`, `AR_hardware`, `Trainium_chip_team`. |
| `hire_overcorrection` | bool/null | Was the cut a correction of recent over-hiring? Cross-referenced with Workforce.ai 2-yr SWE growth data from market-2026.md. `True` if 2-yr growth ≥ +15%. Currently set for Meta×4 (+20%), Atlassian (+23%), Shopify (+36%), Snap (+15%); `False` for Amazon (-1.3%), Oracle (no growth); `null` everywhere else (no data). |
| `reassignment_observed` | bool/null | Did the same restructuring redeploy employees internally rather than cut them? Currently `True` only for Meta May 20 (~7,000 redeployed to four new AI orgs). |

## Methodology notes

- **Rule-based classifier** (in `categorize.py`) is the first pass; manual overrides for ~14 high-confidence rounds.
- **160 entries total**, of which **128 have a public reason recovered** (44 sources were paywalled or blocked; we recovered the 12 largest via alt sources, leaving 32 `unknown`).
- **People-counts** are based on the `# Laid Off` column from layoffs.fyi, which is `null` for many smaller / 100%-shutdown rounds. So "people per category" only sums entries with a disclosed count.
- **The rule base is intentionally over-conservative** on `ai_capex_reallocation` — it requires BOTH a redirect verb AND a concrete capex target (GPU, infra, named project). Otherwise the bucket would swell with cases where "AI" merely appears in the framing.
- **`narrative_source = ceo_memo`** requires explicit memo-language in the reason text. Many entries with quotes from CEOs in news articles land as `news_with_quote`.

## How to extend

Add a row → re-run `python3 categorize.py` → diff `2026-categorized.csv`. Manual overrides go in the `MANUAL` dict at the top of `categorize.py`.
