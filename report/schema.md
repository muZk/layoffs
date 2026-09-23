# Layoffs 2026 — schema v2

One causal vocabulary, reviewed across all 235 records on 2026-09-17. The previous
competing AI axes are archived in `2026-legacy-classifications.json`. They must not be
joined back into current causal counts. No `ai_cause` versus `ai_observation` axis exists.

`causes` means reasons **attributed by the cited source**, with their level of detail. It is not
an independent determination of what caused the layoffs. Multiple causes can coexist.
An empty array means the available evidence does not identify an event-specific reason; it does not
mean there was no cause or no AI contribution.

## Explore these fields

| Field | Meaning |
|---|---|
| `coverage_source` | Where present, tracker name, retrieval date and tracker date for the coverage extension. |
| `record_id` | Stable ID, independent of corrections to dates. |
| `company`, `date` | Name and recorded announcement/report date. Date issues remain flagged where unresolved. |
| `record_type` | `announcement`, `historical_report`, or `annual_workforce_change`. |
| `causes` | Overlapping list of attributed reasons; filter by specificity for concrete mechanisms. |
| `cause_details` | One entry per cause: `summary`, `attribution`, `scope`, `source_url`, `specificity`; optional `evidence_access`. |
| `cause_status` | `specified` (at least one concrete mechanism), `generic` (only generic reasons), `unspecified` (no event-specific explanation identified in reviewed material), `unresolved` (limited evidence), `unavailable`. |
| `context` | Separate facts that do not establish an event-level mechanism. Kind, short summary and source. Not an exhaustive fact inventory or second AI classification. |
| `denials` | Exact target, speaker, summary and source. No generic “denies AI” boolean. |
| `review` | Review date, status, individual assessment, source URLs and remaining issues. |
| `laid_off`, `pct` | Recorded announced headcount and fraction; unknown is null. Neither means completed layoffs. Check scope and issues before summing. |
| `headcount_scope` | Distinguishes event, multi-year plan, multi-round report, derived residual and uncertain figures. |
| `reported_workforce_change` | Preserved numbers that must not be treated as the event's gross layoffs, including annual net reductions. |
| `industry`, `stage` | Original descriptive categories. `stage=Unknown` is unknown, not private. Acquired entities are not classified as public merely because the parent is listed. |
| `country`, `location_hq`, `raised_mm` | Retained source descriptors; not used in this analysis. |
| `source_url`, `source_used` | Original reference and alternate reference. Original reference can be wrong; follow cause-level sources and review issues. |
| `reason` | Concise reviewed synopsis. Use structured causes for counting. |

## Cause vocabulary

| Cause | Inclusion rule |
|---|---|
| `ai_substitution` | Source links AI/automation performing or eliminating work to affected roles. Mixed automation is disclosed; no assumption that all jobs are replaced by AI alone. |
| `ai_productivity` | Source links a smaller workforce to AI-enabled output or capacity. Expected gains count as an attribution, not measured results. |
| `ai_work_redesign` | Specific AI-related changes in role requirements, team structure or workflows are linked to cuts. Generic AI-first branding is insufficient. |
| `ai_investment_reallocation` | Explicit reallocation of resources from cuts toward AI roles, products or infrastructure. Not all investment is capex. |
| `ai_market_disruption` | AI changes demand, distribution or viability of the firm's product and that change is linked to cuts. Selling AI products or entering an AI market is insufficient. |
| `cost_cutting` | Explicit lower costs, margin, profitability or cash-savings objective. |
| `organizational_consolidation` | Specified duplication, merging of functions/sites or removal of management layers. |
| `strategic_pivot` | Specified change in product, customer segment, business model, or explicitly discontinued workstreams. |
| `m_and_a` | Acquisition integration or duplicate roles explicitly linked to cuts; timing alone is insufficient. |
| `financial_distress` | Financing, solvency or business-viability constraint linked to cuts/closure. Weak results alone are insufficient. |
| `demand_decline` | Lower demand or engagement explicitly linked to the reduction. Renamed from `demand_collapse` to avoid exaggerating magnitude. |
| `shutdown` | Closure of the company/business as a whole. |
| `unit_closure` | Closure of a particular unit or site. |
| `work_relocation` | Work moves elsewhere; not automatically lower-cost offshoring. |
| `market_exit` | Company withdraws from a customer market; reducing employment locations while still serving customers is relocation. |
| `lost_contract` | Loss of specific customer work linked to the reduction. |
| `regulatory` | Specified regulatory change linked to cuts. |
| `ipo_prep` | Source explicitly links cuts to listing preparation; proximity alone is insufficient. |
| `performance_cull` | Source identifies performance reviews as the selection mechanism; this does not verify individual performance. |
| `overhiring_correction` | Reserved for explicit event-specific attribution to excess hiring. Currently unassigned; workforce growth alone is insufficient. |

Do not automatically assign both productivity and substitution to the same statement.
Use the mechanism actually described. Multiple AI mechanisms require distinct evidence.

Attribution: `company_stated`, `press_reported`, `worker_reported`,
`reported_inference`, or `company_and_worker_reported`. A company statement quoted by
a newspaper is still company attribution. Anonymous reporting is not company attribution.
These labels describe provenance, not truth scores.

Scope: normally `event`; also `announced_plan`, `multi_year_plan`, `multi_round_period`,
`year_to_date`, `historical_period`, or `annual_period`. An announced multi-year plan
can be analyzed as an announcement; its headcount must not be presented as completed H1 cuts.
Broad plan facts without attribution to the specific event belong in context (Oracle).

Review status: `source_reviewed` means relevant source material was inspected, not that
every number was independently corroborated; `partial` means previews/secondary summaries
or restricted originals limit assessment; `unavailable` means no usable causal source.
A record can have a supported cause and still have partial source access.

## Counting and matrix

There are 233 H1 records. Five concern period-level departures or annual net changes
(Multiverse, GoCardless, Dell, Oracle annual report, SoundThinking quarterly report), leaving 228 announcement records. These are not guaranteed
to be 228 unique independent rounds: possible overlaps remain flagged for Expedia, Meta
and Vimeo. Two July records remain in the dataset but outside H1 counts.

Cross **non-AI mechanisms × AI mechanisms**, deriving both from `causes`. Include a
“No other specified cause” row and “No AI mechanism specified” column so every retained
announcement has a place. The latter is not a no-AI verdict. Show unresolved evidence and
context in drill-down. Cause-pair co-occurrence is also valid; it is descriptive, not proof
of statistical association or causal effect. Never cross AI cause against a duplicate AI
narrative label and call it correlation. Display unique-record denominators and warn that
rows and columns overlap.

CSV encodes nested values as JSON. Null scalar values export as empty cells. Archived
classifications and old charts/notebooks are historical and require migration before reuse.


## Affected work (reviewed 2026-09-17)

All 228 H1 announcement records have `affected_work`. `status` is `identified` (60),
`unit_only` (8), or `not_identified` (160). `functions` uses the 12 keys in
`research/functions/taxonomy.json`; multiple functions may apply. `details` supplies
source URL, attribution, summary and `evidence_access` (`full`, `partial`, or
`prior_review`). Four identified records rely on partial extracts; seven retain
prior-review evidence. `units` records business units separately; `levels` records
seniority, not occupations. `review` records date, method, sources and limitations.
No function identified means no explicit affected occupation found in reviewed
material, not proof that no information exists. Industry, AI use, hiring destinations
and business-unit names are not evidence of eliminated occupations.

Function × cause cells count records, never jobs. Function rows overlap. The four
explanation groups partition each row; individual-cause columns overlap. The unknown
function row includes both unit_only and not_identified (168 records).
`related_records` flags Credit Karma as a reported subset of Intuit's plan.
`headcount_accounts` retains disputed or multi-notice counts without treating them
as a settled event size. Recovery outcomes are in research/functions/recovery-log.json.


## Specificity of attributed explanations

`causes` is the single collection of attributed reasons, including general reasons.
Every `cause_details` entry has `specificity: concrete | generic`; this describes
explanatory detail, not confidence, truth or source access. Concrete mechanisms
describe an operating change or an explicit causal constraint; they do not require
measured effects or an independently proven causal link. Generic reasons retain
meaningful attributed language without inventing a specific mechanism.

Generic taxonomy: organizational_realignment, strategic_priorities, operational_efficiency,
market_conditions, ai_transition. Event-specific AI transition language is different
from background AI products or investment. The latter stays in context. Transferred
AI claims are removed from ai_link_unspecified context to avoid duplicate axes.

Current H1 coverage: 160 announcements with at least one concrete mechanism,
41 with generic reasons only, 13 with no reason identified, 12 with insufficient
causal evidence and 2 without a recovered causal source (228 total).
Generic-only counts cover those 41 records; generic language is not exhaustively
coded alongside previously concrete explanations across the whole collection.

Concrete AI mechanisms occur in 59 records. Another 13 have only generic AI
attributions: 12 generic-only records and Amdocs, which also has a concrete non-AI
mechanism. All-explanation mode counts 72 AI-attributed records. Neither measure
counts verified AI job replacement. Hiring comparisons include all attributed causes, matching the narrative and explorer.

`generic_review` documents the follow-up of all 46 announcements initially carrying
only generic reasons: `outcome` = mechanism_recovered (5),
published_reason_remains_general (38), or investigation_limited (3).
It stores the review date, Spanish assessment and open question, search scope and
consulted source URLs. This is research provenance, not another causal category.
Access limits in Aleph Alpha, Snowflake and MRI do not erase their already available
generic attribution or move them into the unrelated evidence-limited cause_status.
An available statement and an inaccessible potentially richer original can coexist.

Reproduction order: research/explanations/curate.py, research/explanations/recheck.py,
research/generic-review/curate.py, then report/build.py. Each curation step reads its
immutable baseline. The source-review audit chain includes all three follow-ups;
the published explanation ledgers reflect the current classifications.
