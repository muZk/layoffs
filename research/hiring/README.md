# Workforce growth and attributed layoff mechanisms

Read the delivered study at `../../report/contratacion.html` (Spanish).

This is an exploratory availability sample, not a complete primary-document audit or an estimate of excess hiring. It preserves all 217 company labels and explicitly records missing coverage. No layoff causes are inferred from workforce growth.

Reproduce, in order:

1. `python3 research/hiring/collect.py` — identify company histories and collect visible dated numeric workforce observations from Stock Analysis. Cached extracted facts are under `sources/`; restricted observations are not recovered. Mapping includes historical listings and is not a claim of present public-company status. No parent substitutions.
2. `python3 research/hiring/analyze.py` — use current announcement causes, apply primary additions/corrections and quality exclusions, derive dated endpoints, group counts and sensitivity results.
3. `python3 research/hiring/build_report.py` — produce figures, Spanish report and JSON/CSV covering all companies. Also invoked by `report/build.py` after analyses exist.

`primary-checks.json` contains selected facts checked against original statements/filings. Those checks are not a representative validation sample. Four otherwise missing 2019 baselines were recovered for Block, Angi, Atlassian and Upwork; availability still determines membership. All other unverified observations are explicitly secondary compilations. Never interpret `no_series_recovered` or `not_mapped_to_standalone_public_history` as proof that public information does not exist.

`quality-issues.json` documents known date, metric and population issues. `perimeter-events.json` is a nonexhaustive set of documented corporate transactions: null headcount adjustments mean unadjusted, not zero. Sensitivity excludes affected companies only when a documented transaction falls between the actual observation dates. `business-cases.json` and `historical-statements.json` are illustrative case studies, not exhaustive extraction.

The main study uses the latest numeric observation inside each calendar year. This is a reported-workforce comparison: some measures include contractors or annual averages. Fiscal dates, unreviewed definitions and acquisitions constrain interpretation. Medians and counts describe observed companies only. No hypothesis-test or causal-population inference is presented.

The source extracts are numerical facts and metadata; source prose is not republished. All files contain review/source dates and source URLs. The downloadable research JSON includes the hash of the announcement dataset used.
