# Explore the explanations behind the cuts

*Evidence and coverage reviewed 17 September 2026*

228 announcement records. One question at a time, with every count connected to its evidence.

Start with a mechanism, inspect how it combines with others, and open the underlying records. Counts describe explanations attributed in the sources. They do not allocate jobs to a cause or establish causal effects.

[Read the findings article](index.html) · [Download the data](records.csv)

## What is in the collection?

We analyze **228 layoff announcement records from January–June 2026**. The article, explorer and downloadable files use this same collection.

We started with the public layoff list at [Layoffs.fyi](https://layoffs.fyi/2026-layoffs/) and supplemented it with other sources. Records with incomplete evidence are marked. Possible overlapping rounds remain flagged for Expedia, Meta and Vimeo, plus Credit Karma within Intuit’s plan; some plans extend beyond June. The collection is not a census of layoffs or a uniformly sampled monthly series.

## What reasons are attributed to the cuts?

We count the reasons sources attribute to each reduction: savings, reorganization, investment, AI transition and others. A company can give several reasons for one announcement. Select a count to inspect its records and sources.

<!--REASONS-->

**Cost cutting appears in 45 announcements, organizational consolidation in 43, and product or business pivots in 29.** Meanwhile, AI transition appears in 13; organizational realignment, strategic priorities and efficiency each appear in 11.

These bars contain explanations from **201 of 228 announcements**. The other **27** have no classifiable explanation: 13 have no reason identified, 12 have insufficient evidence and 2 have no causal source recovered. An announcement can appear in several bars; adding them does not produce a total of unique announcements.

## How many announcements link cuts to AI?

**In 72 announcements, a source links the cuts to AI.** Reasons include productivity (24), investment reallocation (14), AI transition without further detail (13), work redesign (10), task substitution (8) and AI market disruption (7). An announcement can appear in several categories.

These describe different relationships: funding AI products is not the same as replacing tasks with AI. “AI transition, without further detail” preserves the connection expressed by the source without assuming one of those decisions. The 72 are announcements with an attributed connection, not demonstrated replacements.

## What appears together?

These are the most frequent pairs of **an AI explanation and another reason**. We show the first five positions, including every tie at the fifth. Each count opens its announcements. Pairs overlap: one announcement can contribute to several.

<!--AI-PAIRS-->

**AI productivity and cost cutting appear together in 12 of the 24 announcements with an attributed AI productivity mechanism.** That is half of this group. The sources combine a spending objective with the expectation of producing with fewer people; these data do not measure whether that productivity was achieved.

<!--GROUPS-->

The matrix crosses non-AI reasons with AI explanations. The final row and column include records without a specified mechanism on that side. Select a nonzero count to inspect its records. Rows and columns overlap; do not add cells to calculate unique announcements.


![Matrix of attributed mechanisms.](assets/matrix.svg)

<!--FUNCTIONS-->

Engineering and R&D appears in **31 records**; 8 include an AI explanation. This does not establish that these jobs were replaced by AI. **57 of the 72 announcements with AI explanations** have no specific affected function identified.

Three examples show why the questions are separate: **Breadfast** identifies engineering, product and data, but no specific cause; **Atlassian** identifies R&D and investment reallocation toward AI; **Zap Africa** includes customer support and a worker's substitution claim alongside the company's productivity explanation. Each record preserves the attribution.

## What information is still missing?

**Evidence limited** describes a review limitation: for Xero (February), a BusinessDesk preview describes proposed restructuring, but the full article and a sufficient alternative explanation were not recovered. [Source](https://businessdesk.co.nz/article/markets/xero-restructures-with-250-jobs-on-the-line).

**No causal source recovered** applies to Dayforce, for example: the listing points to an internal memo unavailable for review.

**“No explanation identified” describes our search result.** For those 13 records, we did not recover a reason attributable to the announcement; that does not establish that none exists. [Inspect the individual review and its limits](explanation-recheck.json).

The incomplete-source review recovered sufficient material in **21 of 37 cases**. Fourteen remain partial and two unavailable. Four of the 60 records with identified functions rely on partial extracts; another seven retain evidence from the prior review, marked in each record. [Inspect all 37 reviewed cases](source-recovery.json).

<!--EVIDENCE-->

## How can a company invest in AI and deny a connection?

**AI investment can coexist with denying a different type of connection.** Autodesk, Atlassian and GitLab have both an AI investment explanation and a company-attributed denial. Autodesk and Atlassian deny direct replacement; GitLab denies that the goal is AI optimization or cost reduction. The object of each denial matters: none amounts to denying every possible AI connection. [Read the statements and their differences](index.html#what-does-an-ai-denial-actually-deny).

## Who attributes the explanation to the cut?

Counts include company statements, press attributions and external inferences. Each record identifies who makes the connection, so the classification can be read alongside its basis.

**Attribution matters too:** for Salesforce’s February round, a Forrester analyst interprets the cuts as AI substitution. That record counts as an external inference, not a Salesforce statement or demonstrated replacement. Zencity’s efficiency explanation comes from CTech’s headline, without a company statement.

## Had companies linking cuts to AI grown faster?

We linked announcements to workforce histories: 71 companies have usable 2022–2025 observations and 35 have 2019–2022 observations. In the earlier window, median workforce growth was +80% among companies with attributed AI explanations versus +51% among those with only other mechanisms. In 2022–2025, the medians are +3.7% and +4.7% respectively: the ordering reverses.

The study provides distributions, coverage, sensitivity checks and business-growth case studies. It uses a secondary compilation with partial checks against original filings; it does not measure excess hiring.

[Read the research, in Spanish](contratacion.html) · [Download the data](hiring-research.csv)
