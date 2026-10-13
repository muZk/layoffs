# Methodology

This repository describes a curated collection, not a census or a causal study of technological unemployment. General coverage was reconciled on September 17, 2026; evidence was last reviewed on September 29. The AI tracker comparison uses a separate September 28 snapshot.

## Collection and units

The canonical JSON contains 235 records. Analysis selects 228 announcement records dated January through June 2026. Two July records and five historical/period workforce measures remain in the data but are excluded from announcement counts. Oracle's annual workforce measure is separate from its March announcement; the latter remains in the analysis.

A company can appear more than once. Company labels are not a complete legal-entity consolidation. Possible overlapping rounds remain identified; a count of records is not necessarily a count of independent events or unique people.

## Classification

Each record retains its attributed explanations, supporting sources, attribution and scope. Classification and review were assisted by AI; inter-coder agreement was not measured. Company statements, press reporting, worker accounts and explicit inferences are distinguishable. Source access is not independent corroboration.

Only an explanation connected to the staffing event is assigned as a reason. An acquisition, earlier hiring, a change in leadership or an AI product is not automatically a layoff reason. Context and scoped denials are stored separately. A missing denial does not imply acceptance of an AI explanation.

`causes` includes specific mechanisms and general explanations. `specificity` describes detail, not confidence or truth. All attributed reasons count in the analysis; generic-only records are not removed. Multiple reasons may describe the same decision.

Layoffs.fyi's event-level AI labels are the baseline. Additional evidence can add a link or document an exception, such as a different layoff round. Failure to retrieve an article alone does not justify removing a tracker label. Eleven AI links retain the tracker attribution without independent corroboration of its mechanism. [Comparison and case decisions](research/ai-tracker-comparison/README.md).

## Counts and missing data

Count each announcement once per reason or pair, regardless of the number of sources. Categories overlap. Current counts are 108 announcements with AI reasons, 98 with only other reasons and 22 without a classifiable explanation. Eighty combine AI and other reasons. Among the 228 announcements, 212 have reviewed source material, 14 partial evidence and two unavailable sources.

Headcounts belong to whole announcements, not individual reasons. Do not duplicate them after joining one-to-many reason tables or allocate all jobs to AI. Missing numbers are not zero. Plans, annual net changes, cumulative figures and unverified event sizes have different scopes. Workforce percentages may use a division rather than a whole company as denominator; exploratory comparisons preserve this limitation.

## Employment history and industry

Historical observations retain dates, sources, exclusions and documented changes in company perimeter in `research/hiring/company-history.json`. The notebooks select year-endpoint observations according to their documented rules and calculate percentage changes directly. Availability is selective; acquisitions and workforce definitions are not fully harmonized. Growth does not establish overhiring.

The industry exploration uses `research/hiring/industry-review.json`. Its broad activity groups reflect descriptions consulted in October 2026, not historical revenue-segment classifications. Alternative groupings are shown as sensitivities. Multiple comparisons were explored; these are descriptive exercises, not preregistered confirmatory tests or estimates of AI's effect.

## Reproduction and provenance

1. `scripts/validate_causes.py` checks record structure, CSV consistency and the historical audit chain in `data/audit/` and `coverage/` against the canonical JSON.
2. `scripts/build_normalized.py` generates typed CSV tables, SQLite and a manifest with hashes.
3. `scripts/build_notebooks.py` executes the two published notebooks in isolation and updates their HTML outputs.

The canonical dataset and retained research inputs carry source URLs and review decisions. Old download caches and one-time curation scripts are excluded from the current tree; historical versions remain in Git. Reproduction checks calculations. It does not retrieve new evidence or independently establish what caused any layoff.
