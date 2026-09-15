# Layoffs 2026 categorization schema

Five classification axes plus four optional enrichment columns. Applied to 163 entries: 158 from the layoffs.fyi public Airtable (pull through 2026-05-25; one Vimeo duplicate merged, GitLab's May 11 announcement superseded by its June 3 execution), plus 5 hand-added June–July events (GitLab, Robinhood, Bungie, Microsoft ×2).

## Source files

| File | What it is |
|---|---|
| `2026-airtable-raw.json` | Raw 160 entries from the layoffs.fyi public Airtable share view (extracted via the `readSharedViewData` endpoint). Industry/stage/country are still in select-ID form. |
| `airtable-labels.json` | The ID-to-label maps for the Industry / Stage / Country / Location HQ select columns. |
| `2026-enriched.json` | 163 entries enriched with resolved labels and the public reason recovered from each source URL (158 from the raw extract after dedup/supersede, + 5 hand-added Jun–Jul events). |
| `2026-reasons.json` | The intermediate file with `reason` + `theme_original` per entry (before categorization). It's a snapshot and doesn't include the 5 hand-added Jun–Jul events. |
| `2026-categorized.json` | The main artefact. Full structured records with all 3 axes + enrichment columns. |
| `2026-categorized.csv` | Flat tabular version (good for spreadsheet ingest). |
| `meta-profile-breakdown.md` | Hand-researched role-by-role detail for Meta's 4 rounds. |
| `other-profiles-breakdown.md` | Same for Oracle / PayPal / Amazon / Intuit / Snap. |
| `methodology.md` | How the axes and cause tags were derived: rule-based first pass, manual overrides, primary-source adjudication. |
| `market-2026.md` | Pragmatic Engineer / Workforce.ai data on hiring trends, context for the `hire_overcorrection` flag. |

## Base columns (carried through from layoffs.fyi / enrichment, previously undocumented)

| column | meaning |
|---|---|
| `company`, `date` | Company name and announcement date (not effective date). Together they key every override dict. |
| `laid_off` | Disclosed headcount; `null` when undisclosed (45 of 161 Jan–Jun events, incl. all full shutdowns). |
| `pct` | Share of workforce cut as a 0–1 fraction (0.14 = 14%). |
| `industry`, `stage`, `country`, `location_hq` | layoffs.fyi select fields, label-resolved via `airtable-labels.json`. `country` = layoff location. |
| `source_url` / `source_used` | Original layoffs.fyi source / alternative source used when the original was blocked. |
| `raised_mm` | Total raised in $M per layoffs.fyi. (The redundant `$_raised_mm` duplicate was dropped from outputs 2026-07-10.) |

## Axis 1: `reason_primary` (single value, financial root cause)

What's actually moving cash flow. Mutually exclusive. Picking one forces the analyst to identify the dominant mechanism.

| value | meaning | canonical example |
|---|---|---|
| `ai_capex_reallocation` | OpEx (payroll) cut to fund AI capex (GPUs, datacenters, training). Requires explicit "redirect / shift investment toward AI" + concrete capex target. | Meta (May 20), Cisco |
| `ai_substitution_claim` | CEO publicly claims AI does the work of cut employees. Substitution is the framing. | Block, WiseTech, Snap |
| `cost_cutting` | Generic margin / cost discipline. AI may be present but not the engine. | Bill.com, Ericsson, Wix |
| `path_to_profitability` | Specific cash-flow / profit target stated publicly. | Ocado £150M, GoCardless |
| `new_ceo_turnaround` | A new CEO uses the layoff as a signaling event. AI / cost framing may follow but the trigger is leadership change. | PayPal (Lores), LinkedIn (Shapero), UKG (Morgan) |
| `restructuring_vague` | "Aligning with strategic priorities" / "reducing layers", no specific mechanism stated. Largest catch-all. | Amazon, Intuit, ASML, Expedia |
| `m_and_a_consolidation` | Cuts driven by overlapping roles post-acquisition. | CyberArk (Palo Alto), Verint (Thoma Bravo), Vimeo (Bending Spoons) |
| `ipo_prep` | Streamlining ahead of a stated IPO. | Adda247, Axonius |
| `strategic_pivot` | Company changes its market / product (incl. into AI as a market). | Atlassian, Hailo→robotics, Supernal, Digg |
| `shutdown_bankruptcy` | 100% layoff, company closes. | Entropy, Yupp, Parker, Rec Room |
| `lost_contract_market_exit` | Specific client lost or specific country / market exited. | Sama (lost Meta), Deliveroo (DoorDash exiting Qatar) |
| `geographic_relocation` | Pure offshoring / HQ shift, no headcount-down strategy. | MessageBird (EU → US), One Identity (Germany → abroad) |
| `regulatory` | Regulatory change forces the cut. | Zupee (Indian online-gaming law) |
| `demand_collapse` | Market for the product shrank. | Ericsson (5G capex slowdown), Epic Games (Fortnite engagement), Remarkable |
| `unknown` | Public source wasn't accessible. | The 32 paywall-blocked entries we couldn't recover |

## Axis 2: `ai_link` (relationship to the AI cycle)

How AI shows up in the story, independent of root cause. Separates the AI question from the financial question.

Vocabulary revised 2026-07-10. The axis now carries only the mechanism; who claims it moved to `ai_link_basis` (Axis 2b). The old `ai_denied_but_adjacent` and `ai_pivot_market` values were retired. They conflated mechanism with basis, and the primary-source adjudication proved `ai_denied_but_adjacent` factually wrong for 3 of its 8 large members: PayPal, Wix, and Playtika never denied anything, they affirmed substitution. Legacy values migrate mechanically to `ai_narrative_only`.

| value | meaning |
|---|---|
| `direct_substitution` | "AI does or reduces the cut work". Matches the 16 `ai_substitution_claim` events in the causes layer (Block, WiseTech, Snap, Coinbase, and others). Oracle, PayPal and Wix were re-coded `ai_narrative_only` under the genuineness principle; ZoomInfo is `capex_funding`. |
| `capex_funding` | "The cuts free money for AI investment/infrastructure" (Meta May 20, Cisco, Atlassian, Pinterest). |
| `ai_narrative_only` | AI appears in the company's or press framing, including explicit denials, but no mechanism was stated (Amazon, Intuit, Cloudflare, UKG). Pair with `ai_link_basis` to distinguish denial from vague framing. |
| `unrelated` | No AI in the story at all (Dell, LinkedIn, Ericsson, Sama, Bungie). |
| `unknown` | Can't tell, source blocked. Currently unused (0 records): low-evidence rows carry a substantive label with `narrative_source=not_accessible` instead. Filter on the evidence axis before leaning on those labels. |

## Axis 2b: `ai_link_basis` (who established the AI connection)

Added 2026-07-10 so labels are honest about what is known vs inferred. The old schema forced a false choice: Amazon's 16k cut had a real CEO memo (`narrative_source=ceo_memo`), but the AI label itself was an analyst inference the evidence axis couldn't express.

| value | meaning |
|---|---|
| `company_stated` | The company itself made/supported the `ai_link` reading through a formal channel (memo, filing, earnings call, named exec quote). |
| `company_informal` | The company itself invoked AI, but through an informal channel: a CEO/founder tweet or LinkedIn/blog post, "AI-native"/"AI-first" self-positioning, or a casual spokesperson quote, not a formal filing/earnings call. Added 2026-07: 23 events upgraded from `press_inferred` via a per-event read, recorded in the dataset; two later reverted to press (Envato, Gemini) where AI was an investment target or incidental to financial distress, not a stated cause. Separates "the company said it casually" from "the press added the AI angle". Only upgrades `press_inferred`, never overrides `company_stated`/`company_denied`. |
| `company_denied` | The company explicitly denied AI as the cause. Assigned only via adjudication with verified denial language, currently exactly 3 records: Amazon (via AP), Intuit (on CNBC), Autodesk (SEC-filed email). Never defaulted: the referee pass found the legacy mechanical default had stamped 15 records with no denial evidence. |
| `analyst_inferred` | This dataset's analyst inferred the link. Currently empty: the two events that lived on inference (Amazon, Oracle) resolved to `company_denied` / `company_stated` on adjudication. |
| `press_inferred` | The press/analysts made the AI connection; the company gave a non-AI reason (or none). After the 2026-07 `company_informal` split, only 16 events with a real AI mechanism remain pure-press (e.g. Meta's March/April rounds, Salesforce, Shopify, Expedia, Envato, Gemini). |
| `unknown` | Source not accessible. |

Basis for the 31 adjudicated events (the ≥500-head events plus Amazon, ~94.9% of AI-linked headcount) comes from primary sources. The decisive quote and URL per event are recorded in the dataset. Small events get a default derived from `narrative_source` (memo/filing/quote → `company_stated`, `news_inferred` → `press_inferred`), with two documented failure modes: a `ceo_memo` doesn't guarantee the memo makes the AI claim, and a legacy denial label doesn't guarantee a denial exists.

On headcount reporting, don't collapse `ai_link`/`ai_link_basis` into one "AI-related %". A blended headline of that kind was published earlier (roughly half of disclosed heads counted as "AI-caused by the companies' own account") and is retired: it mixed formal company statements, informal ones, and denials into a single number. The 2026-09 multi-causal layer replaced it with an event-count funnel (see Cause vocabulary below): of 161 Jan–Jun announcements, 71 touch AI in some form, 16 have the company claiming substitution, and only 1 of those 16 holds up against the facts (MercadoLibre, 116 people). Report the mechanism split per basis tier instead of a blended percentage. Audited totals use Oracle's 10-K net figure of 21,000, not the never-confirmed 30,000 press estimate; the viral Oracle Catz/Ellison capex quotes couldn't be traced to any real source, so Oracle's coding rests only on its sworn 10-K.

## Axis 3: `narrative_source` (evidence quality)

How well-sourced the public reason is. Filter on this when you need defensible claims.

| value | meaning |
|---|---|
| `ceo_memo` | Public or leaked memo with attributed quote. Highest confidence. |
| `press_release_sec` | Filing / earnings call / company blog (official). |
| `news_with_quote` | News article with a quote from a named exec or spokesperson. |
| `news_inferred` | Coverage exists but without direct quotes. |
| `slug_only` | URL slug or aggregator headline only (rare, not produced by current rules). |
| `not_accessible` | Paywall / X-Twitter / blocked, original source unreadable, no alternative found. |

## Axis 4: `ai_position` (structural relationship to the AI economy)

The 4th axis was added after distinguishing token-buying from GPU/silicon-buying. A company that PAYS Anthropic per token (Uber, PayPal) is in a fundamentally different economic position from one that BUILDS its own foundation models on its own infrastructure (Meta).

Keyed by company, not by date (this is structural, not per-round).

| value | meaning | what happens when AI demand/cost rises |
|---|---|---|
| `compute_seller` | Sells compute / cloud AI / model APIs to third parties (Oracle, Snowflake, AI21 Labs, DeepL, C3.ai, Firebolt). | Revenue up, they're the supply side. |
| `infra_seller` | Sells hardware, silicon, networking, or data services that enable AI (Cisco, Dell, ASML, Sama, Hailo, Foretellix). | Revenue up, picks-and-shovels. |
| `vertical_builder` | Builds own AI stack end-to-end (foundation models + silicon + datacenters) for own products. Strict criterion: foundation models + own silicon + hyperscaler-scale capex. In our 2026 layoffs dataset, Meta is the only company that qualifies. Apple, Tesla, and ByteDance would qualify but had no 2026 layoffs. Companies like MercadoLibre, Spotify, and Netflix train task-specific models but don't reach this bar and are classified `token_buyer` instead. | Cost up (Nvidia exposure), but no token-price exposure. Bets value flows through downstream products. |
| `token_buyer` | Pays third-party providers (Anthropic, OpenAI, Microsoft) through APIs / partnerships (PayPal, Intuit, Snap, Pinterest, Coinbase, ZoomInfo, Block, WiseTech, dozens more). | Margin squeeze, the Uber paradigm. |
| `hybrid` | Combines two or more of the above (Amazon AWS+Bedrock+Trainium+Nova, Cloudflare Workers AI + internal usage, Microsoft Azure, Atlassian Rovo, LinkedIn via Azure). | Mixed exposure. |
| `n/a` | AI is not material to the business model: telecom, EVs, consumer fitness, fashion, etc. | No AI exposure. |

## Enrichment columns (optional, sparse)

These are filled in only where deep research exists, currently the ~9 manually-researched company-rounds (Meta×4, Oracle, PayPal, Amazon, Intuit, Snap, Atlassian, Shopify, Cloudflare, Wix).

| column | type | what it captures |
|---|---|---|
| `profiles_cut` | list[str] | Specific job functions / teams / levels cut. Tags like `middle_management`, `SDE_II`, `recruiting`, `VR_game_studios_shutdown`, `Reality_Labs`, `support_ops`. |
| `profiles_hired` | list[str] | Specific functions being hired into. Tags like `AI_researchers_foundation_models`, `data_center_technicians_no_degree`, `AR_hardware`, `Trainium_chip_team`. |
| `hire_overcorrection` | bool/null | Superseded: `over_hiring` was retired as a cause tag (see Cause vocabulary below), so this field no longer feeds it. The honest read is the two-window trajectory in `auditoria-sobrecontratacion.md` (a single 2-yr window is misleading). Kept as a raw field. Was the cut a correction of recent over-hiring? `True` if 2-yr growth ≥ +15%. Currently set on 30 events: 24 `True` (e.g. Meta, Atlassian, Block +127%, Pinterest, Coinbase, Intuit, Cloudflare, ZoomInfo, C3.ai, Freshworks, Upwork, Robinhood) and 6 `False` (Amazon, Oracle, WiseTech, M&A-driven, PayPal, Cisco, Playtika); `null` on the other 133 (no growth data means unknown, not False). |
| `reassignment_observed` | bool/null | Did the same restructuring redeploy employees internally rather than cut them? Currently `True` only for Meta May 20 (~7,000 redeployed to four new AI orgs). |
| `revenue_health` | enum/null | Last reported quarter before the layoff: `strength` (growing + profitable) / `mixed` / `weakness` / `unknown`. From the 2026-07-10 external cross-check pass; only the 24 adjudicated stated-AI events carry values. |
| `backfill_verdict` | enum/null | Post-cut hiring behavior: `ai_only` / `frozen` / `rehiring_same` / `offshore_swap` / `mixed` / `unknown`. Null for capex events (backfill doesn't test a capex claim). Same 24-event coverage. |
| `story_integrity` | enum/null | Combined external-evidence call on the company's AI narrative: `holds` / `cracked` (≥1 material fact contradicts the clean story) / `busted` (rehiring/offshoring evidence) / `unknown`. Per-event evidence is recorded in the dataset. An earlier aggregate over company-stated AI heads is retired: the headline is the funnel 161 to 71 to 16 to 1, not a share. |

## Multi-causal layer: `causes`, `cause_evidence`, `ai_claim_verdict` (added 2026-09-02, additive)

Reframe: whether a company uses AI is irrelevant. The thing in dispute is the claim that AI replaced specific jobs. Layoffs are multi-causal, so the single-value `reason_primary` is complemented by a list of cause tags plus a verdict that grades only the substitution claim. The original axes `reason_primary` and `ai_link` were not fully re-derived under the genuineness principle, so where they diverge from `causes`/`ai_mention` (for example `reason_primary=ai_substitution_claim` on Oracle, which the causes layer codes as framing), the causes layer is authoritative. The derivation starts from the existing axes (`reason_primary`, `ai_link`, `ai_link_basis`, `hire_overcorrection`, `story_integrity`, `backfill_verdict`, `revenue_health`) plus manual per-event refinements whose facts sit in the `reason` text or in the event's evidence notes. `2026-categorized.json` is the hand-audited source of truth for the counts below. All 163 records carry the field (the two July events are tagged too but excluded from the counts below). Not added to the CSV. No existing column was renamed or removed.

Genuineness principle: a cause tag is recorded only when it names a real mechanism, not whenever AI gets mentioned. The company (or, rarely for `ai_substitution_claim`, the press on its behalf) has to assert that AI operationally caused or enabled the cut, not merely name AI in passing, in risk-factor boilerplate, or in aspirational framing. Calibration example: Oracle's AI sentence sits in Item 1A Risk Factors of its FY26 10-K, hedged risk language, not an operational "we cut because of AI" claim, so Oracle does not carry `ai_substitution_claim`. It's coded `ai_mention=framing` instead. Whether a claim holds up against the facts is a separate question, graded by `ai_claim_verdict`, not decided by whether the tag gets applied.

| column | type | meaning |
|---|---|---|
| `causes` | list[str] | ≥1 tag from the vocabulary below. The two `ai_*` tags (`ai_substitution_claim`, `ai_capex_reallocation`) are mutually exclusive with each other and gated by the genuineness principle above. All other tags co-occur freely. `unknown` only ever stands alone. |
| `cause_evidence` | dict | tag → one-line note on what the tag rests on (which axis fired, or the documented fact). |
| `ai_mention` | enum | A lens, not a cause: how AI shows up in the announcement regardless of whether it's genuine. Values: `none` (90 events, AI wasn't mentioned at all), `substitution` (16, matches `ai_substitution_claim` in causes), `capex` (5, matches `ai_capex_reallocation`), `framing` (46, AI was named without an operational mechanism, whether by the company or the press), `denied` (4: Amazon, Intuit, Autodesk, Epic Games). |
| `ai_claim_verdict` | enum | Grades only the AI-substitution claim: `plausible` / `thin_evidence` / `contradicted_soft` / `contradicted_hard` / `capex_not_substitution` / `not_claimed`. |

Cause vocabulary (Jan–Jun 2026: 161 events; 125 mono-causal, 36 multi-causal). "Multi-causal" was overstated in an earlier version of this schema, which counted an AI mention as a second cause on its own; once that's corrected, most events have a single, usually vague, cause.

| tag | rule | events |
|---|---|---|
| `ai_substitution_claim` | the disputed claim: `ai_link=direct_substitution` with `ai_link_basis` company_stated/company_informal, passing the genuineness principle above. All 16 are company-stated; none are press-only. Zendesk's internal-memo-only mention (no public source) doesn't qualify and is coded `ai_mention=framing` instead | 16 (10%) |
| `ai_capex_reallocation` | `ai_link=capex_funding`, company-stated: payroll cut to fund AI investment (real, ≠ substitution) | 5: Meta, Cisco, Pinterest, ZoomInfo, GitLab |
| `cost_cutting` | `reason_primary` cost_cutting/path_to_profitability, or explicit savings/margin/profitability language | 42 (26%) |
| `restructuring_unspecified` | `reason_primary=restructuring_vague`, no concrete mechanism stated | 65 (40%) |
| `strategic_pivot` | `reason_primary=strategic_pivot` | 15 (9%) |
| `m_and_a` | `m_and_a_consolidation` + documented merger integration (WiseTech/e2open, Oracle/Cerner, Vimeo/Bending Spoons, eBay/Depop, Staffbase) | 12 (7%) |
| `financial_distress` | `revenue_health=weakness`, or same-day guidance cut / losses on the record | 11 (7%) |
| `unknown` | source not accessible, nothing recoverable | 10 (6%) |
| `demand_collapse` | sector/market downturn (5G capex, crypto cycle, engagement decline) | 9 (6%) |
| `shutdown` | `shutdown_bankruptcy` | 9 (6%) |
| `offshoring` | `backfill_verdict=offshore_swap` (ZoomInfo, Playtika, UKG) or `geographic_relocation` (MessageBird, One Identity) | 5 |
| `market_exit` | lost contract / country exit (+ GitLab's 22-country exit) | 5 |
| `ipo_prep` | as `reason_primary` | 4 |
| `new_ceo_turnaround` | `reason_primary=new_ceo_turnaround` | 4 |
| `rehiring_same_roles` | only where a citable source exists: Block (≥4 named same-role rehires, Business Insider). The raw `backfill_verdict=rehiring_same` cases lacked archivable sources and were dropped | 1 |
| `performance_cull` | performance-review framing (Zillow, Flipkart, Pocket FM) | 3 |
| `regulatory` | as `reason_primary` | 1 |

`ai_framing_vague`, `ai_press_narrative`, `ai_denied`, and `over_hiring` are retired as cause tags. Framing and denial are tracked by `ai_mention` above, not by a `causes` entry; over-hiring lives only in `auditoria-sobrecontratacion.md` (see `hire_overcorrection` above).

`ai_claim_verdict` rules (applied when `ai_substitution_claim` is present, with per-event manual overrides recorded in the dataset):

| value | rule | events |
|---|---|---|
| `plausible` | `story_integrity=holds`, external evidence consistent (no rehiring, revenue as stated). Means "not contradicted", not "proven" | 1: MercadoLibre |
| `contradicted_hard` | `story_integrity=busted` or `rehiring_same_roles` / `offshoring` co-tag | 1: Block |
| `contradicted_soft` | `story_integrity=cracked`: ≥1 material fact cuts against the clean story (same-day guidance cut, M&A synergy in AI clothing, partial backfill) | 6: WiseTech, Snap, Coinbase, Playtika, Upwork, Kraken |
| `thin_evidence` | claim made but not externally testable: informal channel with no cross-check, or the claim itself is unquantified | 8: Freshworks, Angi, ClickUp, Jumia, ApnaMart, Stone, Firebolt, Snowflake |
| `capex_not_substitution` | company's own framing is capex, so there is no substitution claim to grade | 5: Meta, Cisco, Pinterest, ZoomInfo, GitLab |
| `not_claimed` | everything else (unrelated, press-only, vague framing, denied) | 140 |

Headline on the reframe: of the 16 company-made substitution claims, 1 holds (MercadoLibre), 7 are contradicted (1 hard: Block, 6 soft), 8 are too thin to test. Widen the lens to `ai_mention` and the funnel gets starker: of 161 Jan–Jun announcements, 71 touch AI in some form, 16 turn into an actual substitution claim, and only 1 of those 16 survives contact with the facts. Over-hiring is no longer counted as a claim property; a uniform audit showed it is window-dependent and doesn't distinguish claimers from the rest (see `auditoria-sobrecontratacion.md`). Oracle is not among the 16: its AI language sits in Item 1A Risk Factors of the FY26 10-K, not an operational substitution claim, so it's coded `ai_mention=framing` (see the genuineness principle and the Oracle correction below).

Oracle correction (2026-09-02): the FY26 10-K AI sentence lives in Item 1A Risk Factors and Note 7, not the Human Capital section as previously recorded (`source_used` fixed); `profiles_cut` trimmed to the two evidence-backed profiles (KC/Cerner WARN 539; India ~12k press-sourced). SVOS/NetSuite/OCI-support figures trace only to SEO content mills. `story_integrity=cracked` still applies at the `ai_link` level, but Oracle does not carry `ai_substitution_claim` in the causes layer: risk-factor language isn't an operational claim, so it's coded `ai_mention=framing` per the genuineness principle above.

## Methodology notes

- A rule-based classifier was the first pass; 59 event-level manual overrides (deep-research rounds, SEC audit passes, and bucket-audit recodes) were applied on top.
- 163 entries total. Reason recovery has improved since the first snapshot: 10 entries remain `reason_primary=unknown` and 15 are `narrative_source=not_accessible` (originally 44 blocked / 32 unknown).
- `pct` is a 0–1 fraction (0.14 = 14%), not a percentage: a known footgun for anyone consuming the CSV.
- Coverage window: the raw layoffs.fyi pull ends 2026-05-25. Jan–May is complete as-per-layoffs.fyi; the June–July events (GitLab, Robinhood, Bungie, Microsoft ×2) are hand-added high-profile picks, a curated tail, not a collected sample. Do not read May-June deltas as a trend.
- People-counts are based on the `# Laid Off` column from layoffs.fyi, which is `null` for many smaller / 100%-shutdown rounds. So "people per category" only sums entries with a disclosed count.
- The rule base is intentionally over-conservative on `ai_capex_reallocation`: it requires both a redirect verb and a concrete capex target (GPU, infra, named project). Otherwise the bucket would swell with cases where AI merely appears in the framing.
- `narrative_source = ceo_memo` requires explicit memo-language in the reason text. Many entries with quotes from CEOs in news articles land as `news_with_quote`.

## How to add a record

The dataset is edited by hand. Add a new row directly to `2026-categorized.json` (and its CSV) following this schema, with its per-event evidence noted alongside it.
