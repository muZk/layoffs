# Layoff evidence report

Open `index.html` for the illustrated report and interactive source register. Read or edit
`draft.md` for the prose. `assets/` contains five figures in SVG and PNG formats, with data
provenance. Only the 228 January–June announcement records are included in the HTML and downloadable JSON/CSV.

Rebuild after editing the prose or data:

```sh
python3 report/build.py
```

Requires Python packages `markdown` and `matplotlib`. The web edition is static HTML/CSS/JS;
no backend, tracking or API calls. It can be opened directly from disk or served locally.
Jost is bundled under its included open-font license. Fonts, figures and data are local. No publication or deployment has been performed.

Source of truth: `../2026-categorized.json`. Denominator: 228 retained H1 announcement
records. Possible overlaps, plan scopes and evidence limitations remain explicit.

The chart generator creates figures from the data; prose figures should be checked again
if the reviewed source dataset changes. `draft.md` is the editable manuscript; `index.html`
is generated. `template.html`, `report.css` and `report.js` define its presentation.

Spanish edition: `index-es.html`; editable Spanish manuscript: `informe.md`.
The main build generates both editions. Figures and evidence records remain in English.

Data exploration companions: `explorar.html` (Spanish) and `explore.html` (English). Their editable text is `explorar.md` / `explore.md`. The main build generates all four editions.

The additional 20-case explanation review is reproduced with `python3 research/explanations/recheck.py` (after `curate.py`, before building). `explanation-recheck.json` records findings and remaining limits for all 20; `explanation-review.json` contains the current 65-case classifications.

Run `python3 research/generic-review/curate.py` after the explanation recheck and before building to reproduce the 46-case follow-up. `generic-review.json` and `revision-explicaciones.md` document all cases; the Spanish explorer provides an expandable source-linked review.
