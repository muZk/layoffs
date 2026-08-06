# Layoffs 2026 — Categorization Schema

Five classification axes plus four optional enrichment columns. Applied to **163 entries**: 158 from the layoffs.fyi public Airtable (pull through 2026-05-25; one Vimeo duplicate merged, GitLab's May 11 announcement superseded by its June 3 execution), plus 5 hand-added June–July events (GitLab, Robinhood, Bungie, Microsoft ×2).

## Source files

| File | What it is |
|---|---|
| `2026-airtable-raw.json` | Raw 160 entries from the layoffs.fyi public Airtable share view (extracted via the `readSharedViewData` endpoint). Industry/stage/country are still in select-ID form. |
| `airtable-labels.json` | The ID-to-label maps for the Industry / Stage / Country / Location HQ select columns. |
| `2026-enriched.json` | 163 entries enriched with resolved labels and the public reason recovered from each source URL (158 from the raw extract after dedup/supersede, + 5 hand-added Jun–Jul events). |
| `2026-reasons.json` | The intermediate file with `reason` + `theme_original` per entry (before categorization). **Snapshot**: does not include the 5 hand-added Jun–Jul events. |
| `2026-categorized.json` | **The main artefact.** Full structured records with all 3 axes + enrichment columns. |
| `2026-categorized.csv` | Flat tabular version (good for spreadsheet ingest). |
| `meta-profile-breakdown.md` | Hand-researched role-by-role detail for Meta's 4 rounds. |
| `other-profiles-breakdown.md` | Same for Oracle / PayPal / Amazon / Intuit / Snap. |
| `categorize.py` | The categorizer (rule-based + manual overrides). Re-runnable. |
| `market-2026.md` | Pragmatic Engineer / Workforce.ai data on hiring trends — context for the `hire_overcorrection` flag. |

## Base columns (carried through from layoffs.fyi / enrichment, previously undocumented)

| column | meaning |
|---|---|
| `company`, `date` | Company name and **announcement** date (not effective date). Together they key every override dict. |
| `laid_off` | Disclosed headcount; `null` when undisclosed (45 of 161 Jan–Jun events, incl. all full shutdowns). |
| `pct` | Share of workforce cut as a **0–1 fraction** (0.14 = 14%). |
| `industry`, `stage`, `country`, `location_hq` | layoffs.fyi select fields, label-resolved via `airtable-labels.json`. `country` = layoff location. |
| `source_url` / `source_used` | Original layoffs.fyi source / alternative source used when the original was blocked. |
| `raised_mm` | Total raised in $M per layoffs.fyi. (The redundant `$_raised_mm` duplicate was dropped from outputs 2026-07-10.) |

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

**Vocabulary revised 2026-07-10** — the axis now carries only the *mechanism*; who claims it moved to `ai_link_basis` (Axis 2b). The old `ai_denied_but_adjacent` and `ai_pivot_market` values were retired: they conflated mechanism with basis, and the primary-source adjudication proved `ai_denied_but_adjacent` factually wrong for 3 of its 8 large members (PayPal, Wix, and Playtika never denied anything — they affirmed substitution). Legacy values migrate mechanically to `ai_narrative_only`.

| value | meaning |
|---|---|
| `direct_substitution` | "AI does or reduces the cut work" (Oracle per its FY26 10-K, Block, WiseTech, Snap, PayPal, Wix, ZoomInfo). |
| `capex_funding` | "The cuts free money for AI investment/infrastructure" (Meta May 20, Cisco, Atlassian, Pinterest). |
| `ai_narrative_only` | AI appears in the company's or press framing — including explicit denials — but no mechanism was stated (Amazon, Intuit, Cloudflare, UKG). Pair with `ai_link_basis` to distinguish denial from vague framing. |
| `unrelated` | No AI in the story at all (Dell, LinkedIn, Ericsson, Sama, Bungie). |
| `unknown` | Can't tell — source blocked. **Currently unused (0 records)**: low-evidence rows carry a substantive label with `narrative_source=not_accessible` instead — filter on the evidence axis before leaning on those labels. |

## Axis 2b — `ai_link_basis` (who established the AI connection)

Added 2026-07-10 so labels are honest about what is known vs inferred. The old schema forced a false choice: Amazon's 16k cut had a real CEO memo (`narrative_source=ceo_memo`) but the *AI label itself* was an analyst inference the evidence axis couldn't express.

| value | meaning |
|---|---|
| `company_stated` | The company itself made/supported the `ai_link` reading through a **formal** channel (memo, filing, earnings call, named exec quote). |
| `company_informal` | The company itself invoked AI, but through an **informal** channel — a CEO/founder tweet or LinkedIn/blog post, "AI-native"/"AI-first" self-positioning, or a casual spokesperson quote — not a formal filing/earnings call. **Added 2026-07: 23 events upgraded from `press_inferred` via a per-event read (see `INFORMAL_AI` in `categorize.py`); two later reverted to press (Envato, Gemini) where AI was an investment target / incidental to financial distress, not a stated cause.** Separates "the company said it casually" from "the press added the AI angle". Only upgrades `press_inferred`; never overrides `company_stated`/`company_denied`. |
| `company_denied` | The company explicitly denied AI as the cause. **Assigned only via adjudication with verified denial language — currently exactly 3 records: Amazon (via AP), Intuit (on CNBC), Autodesk (SEC-filed email).** Never defaulted: the referee pass found the legacy mechanical default had stamped 15 records with no denial evidence. |
| `analyst_inferred` | This dataset's analyst inferred the link. Currently empty: the two events that lived on inference (Amazon, Oracle) resolved to `company_denied` / `company_stated` on adjudication. |
| `press_inferred` | The press/analysts made the AI connection; the company gave a non-AI reason (or none). After the 2026-07 `company_informal` split, only **16** events with a real AI mechanism remain pure-press (e.g. Meta's March/April rounds, Salesforce, Shopify, Expedia, Envato, Gemini). |
| `unknown` | Source not accessible. |

Basis for the 31 adjudicated events (the ≥500-head events plus Amazon, ~94.9% of AI-linked headcount) comes from primary sources — see the `ADJUDICATION` dict in `categorize.py`, with decisive quote + URL per event. Small events get a default derived from `narrative_source` (memo/filing/quote → `company_stated`, `news_inferred` → `press_inferred`), with two documented failure modes: a `ceo_memo` doesn't guarantee the memo makes the AI claim, and a legacy denial label doesn't guarantee a denial exists.

**Headline usage:** report the mechanism share per basis tier instead of a single "AI-related %". On the audited totals (Oracle at its 10-K net figure of 21,000, not the never-confirmed 30,000 press estimate): of **108,089** disclosed Jan–Jun heads, **34.9% substitution-stated + 13.6% capex-stated = 48.5% AI-caused by the companies' own account**; +1.6% AI mechanism (substitution/capex) attributed outside a formal company statement (1,742 heads, mostly `company_informal`, only ~262 heads pure-press); +23.3% AI-narrative-only (including Amazon's denied 16k); 26.6% genuinely unrelated. (Contested-figure alerts: the viral Oracle Catz/Ellison capex quotes could not be traced to any real source — its substitution coding rests on its sworn 10-K; the 30,000 headline has the same provenance problem, hence 21,000.)

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
| `hire_overcorrection` | bool/null | Was the cut a correction of recent over-hiring? Cross-referenced with Workforce.ai / SEC 10-K 2-yr growth. `True` if 2-yr growth ≥ +15%. Currently set on **30 events: 24 `True`** (e.g. Meta, Atlassian, Block +127%, Pinterest, Coinbase, Intuit, Cloudflare, ZoomInfo, C3.ai, Freshworks, Upwork, Robinhood) and **6 `False`** (Amazon, Oracle, WiseTech — M&A-driven, PayPal, Cisco, Playtika); `null` on the other 133 (no growth data — means unknown, not False). |
| `reassignment_observed` | bool/null | Did the same restructuring redeploy employees internally rather than cut them? Currently `True` only for Meta May 20 (~7,000 redeployed to four new AI orgs). |
| `revenue_health` | enum/null | Last reported quarter *before* the layoff: `strength` (growing + profitable) / `mixed` / `weakness` / `unknown`. From the 2026-07-10 external cross-check pass; only the 24 adjudicated stated-AI events carry values. |
| `backfill_verdict` | enum/null | Post-cut hiring behavior: `ai_only` / `frozen` / `rehiring_same` / `offshore_swap` / `mixed` / `unknown`. Null for capex events (backfill doesn't test a capex claim). Same 24-event coverage. |
| `story_integrity` | enum/null | Combined external-evidence call on the company's AI narrative: `holds` / `cracked` (≥1 material fact contradicts the clean story) / `busted` (rehiring/offshoring evidence) / `unknown`. Headline result (on audited Oracle-21k figures): of company-stated AI heads, **27.7% holds, 68.3% cracked, 4.0% busted**. Evidence per event in `categorize.py`'s `CROSS_CHECK` dict. |

## Methodology notes

- **Rule-based classifier** (in `categorize.py`) is the first pass; **59 event-level manual overrides** (deep-research rounds, SEC audit passes, and bucket-audit recodes) in the `MANUAL` dict.
- **163 entries total.** Reason recovery has improved since the first snapshot: **10** entries remain `reason_primary=unknown` and **15** are `narrative_source=not_accessible` (originally 44 blocked / 32 unknown).
- **`pct` is a 0–1 fraction** (0.14 = 14%), not a percentage — a known footgun for anyone consuming the CSV.
- **Coverage window**: the raw layoffs.fyi pull ends **2026-05-25**. Jan–May is complete as-per-layoffs.fyi; the June–July events (GitLab, Robinhood, Bungie, Microsoft ×2) are hand-added high-profile picks — a curated tail, not a collected sample. Do not read May→June deltas as a trend.
- **People-counts** are based on the `# Laid Off` column from layoffs.fyi, which is `null` for many smaller / 100%-shutdown rounds. So "people per category" only sums entries with a disclosed count.
- **The rule base is intentionally over-conservative** on `ai_capex_reallocation` — it requires BOTH a redirect verb AND a concrete capex target (GPU, infra, named project). Otherwise the bucket would swell with cases where "AI" merely appears in the framing.
- **`narrative_source = ceo_memo`** requires explicit memo-language in the reason text. Many entries with quotes from CEOs in news articles land as `news_with_quote`.

## How to extend

Add a row → re-run `python3 categorize.py` → diff `2026-categorized.csv`. Manual overrides go in the `MANUAL` dict at the top of `categorize.py`.
