# Layoffs 2026 categorization schema

Five classification axes, a multi-causal layer, a role-of-AI axis (`papel_ia`, reconciled 2026-09), plus four optional enrichment columns. Applied to 163 entries: 158 from the layoffs.fyi public Airtable (pull through 2026-05-25; one Vimeo duplicate merged, GitLab's May 11 announcement superseded by its June 3 execution), plus 5 hand-added June–July events (GitLab, Robinhood, Bungie, Microsoft ×2).

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
| `direct_substitution` | "AI does or reduces the cut work". 16 records carry it, but only 6 pass the genuineness gate into `ai_substitution_claim` in the causes layer (Angi, MercadoLibre, WiseTech, Snowflake, Freshworks, Kraken). The other 10 (Block, Snap, Coinbase, Upwork, Playtika, Firebolt, ApnaMart, Jumia, ClickUp, Stone) said "smaller teams" or "efficiency", not "AI replaced these people", and read as `papel_ia=eficiencia` or `vaga`. Oracle, PayPal and Wix were re-coded `ai_narrative_only` under the genuineness principle; ZoomInfo is `capex_funding`. |
| `capex_funding` | "The cuts free money for AI investment/infrastructure" (Meta May 20, Cisco, Atlassian, Pinterest). Cisco keeps this legacy label but lost the `ai_capex_reallocation` cause tag in the 2026-09 reconciliation (its AI mention was vague, `papel_ia=vaga`). |
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

On headcount reporting, don't collapse `ai_link`/`ai_link_basis` into one "AI-related %". A blended headline of that kind was published earlier (roughly half of disclosed heads counted as "AI-caused by the companies' own account") and is retired: it mixed formal company statements, informal ones, and denials into a single number. The 2026-09 multi-causal layer replaced it with an event-count funnel (see Cause vocabulary and Role of AI below): of 161 Jan–Jun announcements, AI plays some role in 70, is a real cause in 16, and of the 6 company-stated substitution claims only 1 holds up against the facts (MercadoLibre, 116 people). Report the mechanism split per basis tier instead of a blended percentage. Audited totals use Oracle's 10-K net figure of 21,000, not the never-confirmed 30,000 press estimate; the viral Oracle Catz/Ellison capex quotes couldn't be traced to any real source, so Oracle's coding rests only on its sworn 10-K.

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
| `story_integrity` | enum/null | Combined external-evidence call on the company's AI narrative: `holds` / `cracked` (≥1 material fact contradicts the clean story) / `busted` (rehiring/offshoring evidence) / `unknown`. Per-event evidence is recorded in the dataset. An earlier aggregate over company-stated AI heads is retired: the headline is the funnel 161 to 70 to 16 to 6 to 1, not a share. |

## Multi-causal layer: `causes`, `cause_evidence`, `ai_claim_verdict` (added 2026-09-02, additive)

Reframe: whether a company uses AI is irrelevant. The thing in dispute is the claim that AI replaced specific jobs. Layoffs are multi-causal, so the single-value `reason_primary` is complemented by a list of cause tags plus a verdict that grades only the substitution claim. The original axes `reason_primary` and `ai_link` were not fully re-derived under the genuineness principle, so where they diverge from `causes`/`ai_mention` (for example `reason_primary=ai_substitution_claim` on Oracle, which the causes layer codes as framing), the causes layer is authoritative. The derivation starts from the existing axes (`reason_primary`, `ai_link`, `ai_link_basis`, `hire_overcorrection`, `story_integrity`, `backfill_verdict`, `revenue_health`) plus manual per-event refinements whose facts sit in the `reason` text or in the event's evidence notes. `2026-categorized.json` is the hand-audited source of truth for the counts below. All 163 records carry the field (the two July events are tagged too but excluded from the counts below). Not added to the CSV. No existing column was renamed or removed.

Genuineness principle: a cause tag is recorded only when it names a real mechanism, not whenever AI gets mentioned. The company (or, rarely for `ai_substitution_claim`, the press on its behalf) has to assert that AI operationally caused or enabled the cut, not merely name AI in passing, in risk-factor boilerplate, or in aspirational framing. Calibration example: Oracle's AI sentence sits in Item 1A Risk Factors of its FY26 10-K, hedged risk language, not an operational "we cut because of AI" claim, so Oracle does not carry `ai_substitution_claim`. It's coded `ai_mention=framing` instead. Whether a claim holds up against the facts is a separate question, graded by `ai_claim_verdict`, not decided by whether the tag gets applied.

| column | type | meaning |
|---|---|---|
| `causes` | list[str] | ≥1 tag from the vocabulary below. The two `ai_*` tags (`ai_substitution_claim`, `ai_capex_reallocation`) are mutually exclusive with each other and gated by the genuineness principle above. All other tags co-occur freely. `unknown` only ever stands alone. |
| `cause_evidence` | dict | tag → one-line note on what the tag rests on (which axis fired, or the documented fact). |
| `ai_mention` | enum | A lens, not a cause: how AI shows up in the announcement regardless of whether it's genuine. Values: `none` (90 events, AI wasn't mentioned at all), `substitution` (16), `capex` (5), `framing` (46, AI was named without an operational mechanism, whether by the company or the press), `denied` (4: Amazon, Intuit, Autodesk, Epic Games). Kept as recorded in 2026-09-02; the 2026-09 reconciliation did not re-derive it, so `substitution` (16) and `capex` (5) no longer match the tightened cause tags (6 and 4). `papel_ia` (see Role of AI below) supersedes it as the primary AI lens. |
| `ai_claim_verdict` | enum | Grades the AI-substitution claim: `plausible` / `thin_evidence` / `contradicted_soft` / `contradicted_hard` / `capex_not_substitution` / `not_claimed`. Graded on the 16 events that carried `ai_substitution_claim` before the 2026-09 tightening; the 10 events that lost the tag keep their verdict as a record of what the earlier grading found. |

Cause vocabulary (Jan–Jun 2026: 161 events; 123 mono-causal, 38 multi-causal). "Multi-causal" was overstated in an earlier version of this schema, which counted an AI mention as a second cause on its own; once that's corrected, most events have a single, usually vague, cause.

| tag | rule | events |
|---|---|---|
| `ai_substitution_claim` | the disputed claim: the company itself says AI does the work of the people cut, passing the genuineness principle above. Tightened 2026-09 from 16 to 6. All 6 come from the company (4 `company_stated`, 2 `company_informal`: Angi, Snowflake); none are press-only. The 10 that lost the tag (Block, Snap, Coinbase, Upwork, Playtika, Firebolt, ApnaMart, Jumia, ClickUp, Stone) said "smaller teams" or "efficiency with AI" without claiming AI replaced specific people, and now carry only their mundane cause (mostly `restructuring_unspecified` or `cost_cutting`). DraftKings (press-only) and Zendesk (internal memo, no public source) read as `papel_ia=reemplazo` but don't qualify | 6 (4%): Angi, MercadoLibre, WiseTech, Snowflake, Freshworks, Kraken |
| `ai_capex_reallocation` | `ai_link=capex_funding`, company-stated: payroll cut to fund AI investment (real, ≠ substitution). Cisco lost the tag 2026-09: its AI mention was vague, recoded as plain restructuring | 4: Meta, Pinterest, ZoomInfo, GitLab |
| `cost_cutting` | `reason_primary` cost_cutting/path_to_profitability, or explicit savings/margin/profitability language | 42 (26%) |
| `restructuring_unspecified` | `reason_primary=restructuring_vague`, no concrete mechanism stated. Rose from 65 to 69 in the 2026-09 tightening, as most of the ex-substitution events landed here | 69 (43%) |
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

`ai_claim_verdict` rules (graded on the 16 events that carried `ai_substitution_claim` on 2026-09-02, with per-event manual overrides recorded in the dataset; the 2026-09 tightening cut the tag to 6 and left the verdicts in place). Events still tagged are listed first; the rest are the 10 recoded events, which keep their verdict as a record:

| value | rule | events |
|---|---|---|
| `plausible` | `story_integrity=holds`, external evidence consistent (no rehiring, revenue as stated). Means "not contradicted", not "proven" | 1: MercadoLibre |
| `contradicted_hard` | `story_integrity=busted` or `rehiring_same_roles` / `offshoring` co-tag | 1: Block (recoded `papel_ia=eficiencia`, keeps `rehiring_same_roles`) |
| `contradicted_soft` | `story_integrity=cracked`: ≥1 material fact cuts against the clean story (same-day guidance cut, M&A synergy in AI clothing, partial backfill) | 6: WiseTech, Kraken; recoded Snap, Coinbase, Playtika, Upwork |
| `thin_evidence` | claim made but not externally testable: informal channel with no cross-check, or the claim itself is unquantified | 8: Angi, Snowflake, Freshworks; recoded ClickUp, Jumia, ApnaMart, Stone, Firebolt |
| `capex_not_substitution` | company's own framing is capex, so there is no substitution claim to grade | 5: Meta, Pinterest, ZoomInfo, GitLab; recoded Cisco |
| `not_claimed` | everything else (unrelated, press-only, vague framing, denied) | 140 |

Headline on the reframe: of the 6 company-made substitution claims, 1 holds (MercadoLibre, 116 people, 0.1% of the 108,089 laid off), 2 are contradicted (WiseTech, Kraken, both soft), 3 are too thin to test (Angi, Snowflake, Freshworks). Widen the lens to `papel_ia` and the funnel reads: of 161 Jan–Jun announcements, AI plays some role in 70, is a real cause in 16 (6 substitution claims, 4 capex reallocations, 6 products made obsolete by AI), and only 1 of the 6 substitution claims survives contact with the facts. Over-hiring is no longer counted as a claim property; a uniform audit showed it is window-dependent and doesn't distinguish claimers from the rest (see `auditoria-sobrecontratacion.md`). Oracle is not among the 6: its AI language sits in Item 1A Risk Factors of the FY26 10-K, not an operational substitution claim, so it's coded `ai_mention=framing` and `papel_ia=vaga` (see the genuineness principle and the Oracle correction below).

Oracle correction (2026-09-02): the FY26 10-K AI sentence lives in Item 1A Risk Factors and Note 7, not the Human Capital section as previously recorded (`source_used` fixed); `profiles_cut` trimmed to the two evidence-backed profiles (KC/Cerner WARN 539; India ~12k press-sourced). SVOS/NetSuite/OCI-support figures trace only to SEO content mills. `story_integrity=cracked` still applies at the `ai_link` level, but Oracle does not carry `ai_substitution_claim` in the causes layer: risk-factor language isn't an operational claim, so it's coded `ai_mention=framing` per the genuineness principle above.

## Role of AI: `papel_ia`, `papel_sub`, `fuente_ia`, `nego_ia`, `es_causa_ia` (added 2026-09, reconciled)

The causes layer answers "did the company claim AI replaced these people". It says nothing about the far more common case where AI is in the announcement without being the mechanism. `papel_ia` covers that gap. It is set on every record and classifies the role AI plays in the announcement, whoever put it there. It supersedes `ai_mention` as the primary AI lens; `ai_mention` stays for continuity but was not re-derived.

The two axes are reconciled. `ai_substitution_claim` in `causes` is exactly `papel_ia=reemplazo` with `fuente_ia=empresa` (6 events); `ai_capex_reallocation` is exactly `papel_ia=inversion` with `fuente_ia=empresa` (4 events). A company that only said "smaller teams" or "more productive with AI" is `eficiencia`, not `reemplazo`, and carries no AI cause tag.

| column | type | meaning |
|---|---|---|
| `papel_ia` | enum | Role of AI in the announcement. Values below. |
| `papel_sub` | enum/null | Sub-value for `vaga` and `disrupcion`; null otherwise. |
| `fuente_ia` | enum | Who linked AI to the cut: `empresa` (52), `prensa` (21), `desconocida` (4, AI appears but the source can't be established, e.g. an internal memo with no public footprint), `ninguna` (84, nobody did). |
| `nego_ia` | bool | The company explicitly denied AI as the cause. True for 4: Amazon, Epic Games, LinkedIn, Intuit. Overlaps `ai_mention=denied` on Amazon, Epic Games and Intuit; Autodesk carries `ai_mention=denied` and `ai_link_basis=company_denied` but not `nego_ia`, LinkedIn the reverse. |
| `es_causa_ia` | bool | Is AI a real cause of this cut. True for 16: the 6 `reemplazo` from the company, the 4 `inversion` from the company, and the 6 `mercado_roto`. |

`papel_ia` values (Jan–Jun 2026, 161 events):

| value | meaning | events |
|---|---|---|
| `ninguna` | AI not mentioned, or mentioned without any operating role (a press aside, a denial with no AI mechanism behind it). | 91 |
| `vaga` | AI is named but does nothing in the story. `papel_sub`: `de_pasada` (24, mentioned in passing, e.g. Cisco's "areas of strongest demand in the AI era"), `perfiles_obsoletos` (3, the skill mix or roles are said to change "in the AI era", with no claim that AI does the work: Atlassian, Crypto.com, Wix), `boilerplate_legal` (1, Oracle's 10-K risk-factor sentence). | 28 |
| `eficiencia` | "Smaller teams using AI", productivity, "AI-first" self-positioning. The company does not claim AI replaced specific people. Block, Snap, Coinbase, Upwork, Firebolt, ApnaMart, Jumia, ClickUp live here. | 19 |
| `disrupcion` | AI changed the company's market. `papel_sub`: `mercado_roto` (6, the product was made obsolete by AI, usually a shutdown: Digg, Yupp, NeuroPixel.AI, Productboard, Epidemic Sound, AI21 Labs), `pivote_producto` (4, the company pivots its product toward AI: Hailo, Shopify, Pendo, Dune). | 10 |
| `reemplazo` | The company or the press says AI does the cut work. 6 from the company (the `ai_substitution_claim` set), 1 from the press (DraftKings), 1 from an unknown source (Zendesk). | 8 |
| `inversion` | The cut funds AI infrastructure. 4 from the company (the `ai_capex_reallocation` set), 1 from the press (Arctic Wolf). | 5 |

Reading the funnel on this axis: AI plays some role in 70 of 161 announcements (`papel_ia != ninguna`); someone linked it in 77 (`fuente_ia != ninguna`, the difference being 7 events where the press or an unknown source mentioned AI with no operating role); it is a real cause in 16 (`es_causa_ia`); the company claims substitution in 6; 1 of those holds.

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
