# Methodology — complete record review, 2026-09-16

Every one of the 235 records received an individual assessment: 198 have reviewed source
material, 35 have partial evidence and two remain unavailable. Sources include reporting, company statements and regulatory filings; the coverage extension was assessed on 2026-09-17. Partial
and unavailable records are explicitly retained. This is an evidence review, not an
independent audit of every job loss or every source's accuracy.

1. Identify the event and the period covered by the source. Do not transfer an explanation
   from another round, acquisition, annual filing or industry trend.
2. Record attributed reasons and their specificity, separating who attributes them from whether they are proven.
   Company, worker, press and explicitly inferred explanations can all be retained visibly.
3. Remove unsupported assignments. A new CEO, weaker revenue, an IPO, an acquisition or
   earlier hiring is context unless the source connects it to the staffing reduction.
4. Use one cause vocabulary. Retire `reason_primary`, `ai_link`, `papel_ia`, `fuente_ia`,
   `ai_claim_verdict`, `es_causa_ia` and related competing axes from the active dataset.
5. Keep separate contextual facts and scoped denials, with sources. Do not create an
   “AI observation” duplicate for every AI cause. No denial found means no recorded denial,
   not affirmative acceptance of AI causality.
6. Preserve all records and original values in the full audit and legacy snapshot. Mark
   historical/annual records separately; preserve non-layoff quantities as scoped metrics.
7. Generate the CSV, all-record review register and counts from the same current JSON.
   Validate the previous audit chain, all 235 individual assessments and CSV consistency.

## Scope and denominators

233 H1 records contain 228 announcement records and five period/annual records.
Two July records are excluded from H1 analysis. Possible duplicate rounds remain visible;
counts describe records, not a fully deduplicated universe of independent events.
All 231 H1 entries in the 2026-09-17 Layoffs.fyi snapshot are accounted for, with two additional H1 records retained from other sources. The collection covers this tracker, not every layoff worldwide. Source access and possible overlaps remain explicit.

Count a record once within each cause or pair, even when evidence has multiple sources.
Categories overlap. Never attribute its entire headcount to every listed cause. No aggregate
people total is promoted here: missing numbers, annual net changes, planned reductions,
cumulative rounds, possible overlaps and unverified estimates make an unqualified sum misleading.

## Oracle boundary

The FY2026 filing was read, including Risk Factors, Note 7 and workforce totals. It
acknowledges past AI-related reductions and includes AI integration in a broader efficiency
plan. That is evidence worth displaying; it does not allocate the March announcement to AI.
The 21,000 annual net decrease cannot substitute for the gross size of that event.
The March termination email supplies a generic organizational explanation, but no
event-level AI mechanism. The record carries the
filing evidence as broader-plan context, with the annual number stored separately.

PayPal's record describes a multi-year plan itself, for which the company explicitly names
organizational changes and AI process redesign. Those are plan-scoped causes, not an
allocation of its reported headcount or a statement that cuts were completed in H1.

## Gaps that constrain comparisons

- Overhiring needs comparable historical employment series, acquisition adjustments and
  event-specific attribution. The earlier binary flag was not a complete or causal measure.
- Public/private status uses an incomplete tracker stage field; “Unknown” is not private.
  Denials have different targets and sources and were not elicited uniformly.
- Context is not an exhaustive extraction of financial or hiring facts. Absence cannot serve
  as a negative observation for a correlation analysis.
- Source-reviewed is not corroborated. Productivity claims and promised future savings may
  be unmeasured; reported mechanisms may themselves be disputed.

Original pipeline history is preserved in `archive/methodology-before-full-review.md`.
That document and historical analyses contain superseded totals and classifications.


## Source recovery and affected functions, 17 September 2026

Reviewed all 228 H1 announcements for explicit affected occupations, using retrieved
source bodies and preserved review evidence. Searched alternative reporting for all
37 incomplete source cases; 21 now have sufficient source material, 14 remain partial
and 2 unavailable. Full source access does not imply a specific causal explanation.
Wrong-year reports, unsupported aggregator summaries and general AI workflow examples
were not used to infer affected jobs. Evidence access remains visible per function.
The source-recovery ledger describes search scope and unresolved limits; it is not
a claim that every possible source was exhausted. The audit preserves before/after
records, and research/functions/curate.py reproduces these manual decisions from its
baseline. Taxonomy, source links and attribution accompany each positive classification.


## General reasons and concrete mechanisms

The explanation review in research/explanations/curate.py reclassifies all 65
source-reviewed H1 announcements previously left unspecified. Reasons remain in
causes, with per-reason specificity and attribution. Forty-two have general reasons,
three have concrete mechanisms, and twenty have no reason identified in reviewed
material. No source-access status was promoted by this classification change.
Full cached source bodies, freshly retrieved original/secondary reporting, and
explicitly marked retained review evidence support the decisions. No causal proof
is inferred from a detailed statement. Existing concrete-mechanism records retain
their classifications; counts of generic categories concern generic-only records.
The narrative, explorer, static figures and workforce-history groups now count all
attributed reasons. Specificity remains an evidence annotation, not an inclusion filter.
Generic reasons were not exhaustively re-coded alongside every previously concrete
account; counts describe the recorded evidence and may omit additional general language.

## Additional explanation search
All 20 remaining source-reviewed records without an identified reason received an individual reread and alternative-source search. Seven were reclassified: four generic explanations, two concrete company accounts, and one external analyst inference (Salesforce, February). Thirteen remain without a recovered event-specific reason; this is a search limitation, not proof of silence. See research/explanations/recheck-review.json. Credit Karma evidence explicitly names the subsidiary but remains plan-scoped; Zondacrypto evidence concerns the employing subsidiary Orion Software, not formal bankruptcy of the whole exchange.

## Generic-explanation follow-up
All 46 generic-only announcements were reread and searched individually for more precise event-level accounts. Five now contain a concrete attributed mechanism; 38 retain only general published explanations, and three have a material original-source access limit (Aleph Alpha, Snowflake, MRI Software). Scope and attribution remain explicit: NetApp concerns one worker’s cancelled project; Glossier is a press attribution in a publicly accessible excerpt; Amdocs and Pentera are press-reported; Eventbrite is its new lead’s statement. None is independently proven causality. The 12 initial generic AI cases remain generic. Amdocs adds a generic AI attribution alongside a concrete non-AI mechanism. See research/generic-review/review.json and coverage/generic-followup-2026-09-17.json.

## Full-population descriptive analysis

`research/full-analysis/analyze.py` computes all reason frequencies, all pairs, attribution and scope distributions, affected-function coverage, industry coverage and mutually exclusive AI groups directly from the canonical 228 H1 announcements. No specificity exclusion is applied. The published analysis is `report/analysis.json`; it preserves the record IDs underlying each reason and pair. There are 206 records with a classifiable reason, 107 with an AI reason, 78 with AI and another reason, 29 with only AI reasons recorded, 99 with only other reasons and 22 without a classifiable reason. One hundred and six records have multiple reasons. These are descriptive co-occurrences, not causal effects or population estimates.

The workforce-history analysis uses the same all-reasons definition at company-label level. Its fixed coverage is unchanged; grouping and estimates are recomputed. Historical specificity annotations remain available for audit, but do not establish a behavioral difference between companies.

## Consistency check against the AI tracker — 2026-09-28

All 235 stored assessments were screened against the same event-link rule; selected sources were reread, not every original source retrieved again. Sixteen announcements gained an AI attribution already supported by an event-specific investment or transition account; Veritone's scope note was corrected without adding AI. Before adopting the tracker-first policy below, that review produced 88 AI announcements, 64 with another reason and 94 with multiple reasons. These are historical intermediate counts, not current results. The general coverage snapshot remains September 17; the AI tracker comparison uses a separate September 28 snapshot. See `research/ai-tracker-comparison/`.


## Tracker-first AI attribution policy (September 28, 2026)

Layoffs.fyi’s event-level AI classifications are the baseline. Lack of access to its linked source, lack of company confirmation, or a more general corporate explanation is not enough to remove a classification. We preserve additional AI attributions documented in other sources, and diverge only for a documented event or scope mismatch, correction, or later clarification. A later publication must concern the same event.

Twelve general AI links are retained from the tracker without independently corroborating its detailed mechanism. They use `ai_transition`, `reported_inference`, and the tracker as `source_url`; summaries explicitly identify this provenance. Full access to the tracker is not full access to its underlying article. These cases are counted as attributed AI links, not confirmed replacement or company statements. Seven other additions have additional source or plan-level context. Verily remains excluded from AI classification because the tracker names a devices closure announced in August 2025 for a June 2026 notice. The 16 additional AI announcements absent from the tracker remain included. See `coverage/ai-tracker-baseline-2026-09-28.json`.
