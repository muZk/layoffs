import json

DATA_PATH = "/Users/muzk/code/layoffs/2026-categorized.json"
SPLIT_PATH = "/Users/muzk/code/layoffs/analysis-twolens/split.json"
TOTAL_DISCLOSED = 108089

data = json.load(open(DATA_PATH))
split = json.load(open(SPLIT_PATH))
mega_events = split["mega_events"]

# index main dataset by (company, date)
by_key = {(r["company"], r["date"]): r for r in data}

print("=" * 100)
print("ALL KEYS PRESENT ON THE 13 MEGA-EVENT RECORDS")
print("=" * 100)
keyset = set()
for e in mega_events:
    key = (e["company"], e["date"])
    r = by_key.get(key)
    if r is None:
        print(f"!!! NOT FOUND: {key}")
        continue
    keyset.update(r.keys())
print(sorted(keyset))
print()

records = []
for e in mega_events:
    key = (e["company"], e["date"])
    r = by_key.get(key)
    if r is None:
        continue
    records.append(r)

# sort by laid_off descending
records.sort(key=lambda r: r["laid_off"], reverse=True)

print("=" * 100)
print("PER-EVENT DOSSIER (13 mega events, ordered by laid_off descending)")
print("=" * 100)

for r in records:
    laid_off = r["laid_off"]
    pct_of_total = laid_off / TOTAL_DISCLOSED * 100
    pct_workforce = r.get("pct")
    pct_workforce_str = f"{pct_workforce*100:.1f}%" if isinstance(pct_workforce, (int, float)) else str(pct_workforce)

    print("-" * 100)
    print(f"COMPANY: {r['company']}   DATE: {r['date']}")
    print(f"  laid_off: {laid_off}   ({pct_of_total:.2f}% of {TOTAL_DISCLOSED} total disclosed Jan-Jun heads)")
    print(f"  pct (workforce share): {pct_workforce_str}")
    print(f"  reason_primary: {r.get('reason_primary')}")
    print(f"  ai_link: {r.get('ai_link')}   ai_link_basis: {r.get('ai_link_basis')}")
    print(f"  narrative_source: {r.get('narrative_source')}")
    print(f"  story_integrity: {r.get('story_integrity')}")
    print(f"  revenue_health: {r.get('revenue_health')}")
    print(f"  backfill_verdict: {r.get('backfill_verdict')}")
    print(f"  hire_overcorrection: {r.get('hire_overcorrection')}")
    print(f"  reassignment_observed: {r.get('reassignment_observed')}")
    print(f"  ai_position: {r.get('ai_position')}")
    print(f"  industry: {r.get('industry')}   country: {r.get('country')}   stage: {r.get('stage')}")
    print(f"  location_hq: {r.get('location_hq')}")
    print(f"  raised_mm: {r.get('raised_mm')}")
    print(f"  theme_original: {r.get('theme_original')}")
    print(f"  source_used: {r.get('source_used')}")
    print(f"  source_url: {r.get('source_url')}")
    print(f"  profiles_cut: {r.get('profiles_cut')}")
    print(f"  profiles_hired: {r.get('profiles_hired')}")
    print(f"  reason (full text): {r.get('reason')}")
    print()

print("=" * 100)
print("SUMMARY COUNTS")
print("=" * 100)

n_ai_company_stated = sum(
    1 for r in records
    if r.get("ai_link") in ("direct_substitution", "capex_funding")
    and r.get("ai_link_basis") == "company_stated"
)
print(f"ai_link in (direct_substitution, capex_funding) AND ai_link_basis == company_stated: {n_ai_company_stated} / 13")

from collections import Counter
si_counts = Counter(r.get("story_integrity") for r in records)
print("story_integrity breakdown:")
for k in ["holds", "cracked", "busted", None]:
    print(f"  {k}: {si_counts.get(k, 0)}")
# catch any unexpected values
for k, v in si_counts.items():
    if k not in ["holds", "cracked", "busted", None]:
        print(f"  UNEXPECTED value {k}: {v}")

ho_counts = Counter(r.get("hire_overcorrection") for r in records)
print("hire_overcorrection breakdown:")
for k in [True, False, None]:
    print(f"  {k}: {ho_counts.get(k, 0)}")
for k, v in ho_counts.items():
    if k not in [True, False, None]:
        print(f"  UNEXPECTED value {k}: {v}")
