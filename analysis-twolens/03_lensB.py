#!/usr/bin/env python3
"""
Lens B: population-level analysis (148 events = 161 Jan-Jun events minus 13 mega-events),
with a distortion check against all 161 Jan-Jun events (mega included).

Reads:
  /Users/muzk/code/layoffs/2026-categorized.json      (163 records, all events)
  /Users/muzk/code/layoffs/analysis-twolens/split.json (population_keys: 148 [company,date] pairs)
"""
import json
import statistics as stats
from collections import Counter, defaultdict

DATA_PATH = "/Users/muzk/code/layoffs/2026-categorized.json"
SPLIT_PATH = "/Users/muzk/code/layoffs/analysis-twolens/split.json"

with open(DATA_PATH) as f:
    data = json.load(f)
with open(SPLIT_PATH) as f:
    split = json.load(f)

pop_keys = set(tuple(x) for x in split["population_keys"])

# Jan-Jun 2026 window excludes the two 2026-07-06 Microsoft events.
all_janjun = [d for d in data if d["date"] <= "2026-06-30"]
population = [d for d in all_janjun if (d["company"], d["date"]) in pop_keys]

assert len(all_janjun) == 161, f"expected 161 Jan-Jun events, got {len(all_janjun)}"
assert len(population) == 148, f"expected 148 population events, got {len(population)}"


def fmt_pct(x):
    return f"{x*100:.1f}%"


def hr(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


# ---------------------------------------------------------------------------
# 1. SANITY
# ---------------------------------------------------------------------------
hr("1. SANITY CHECK (148-event population)")

n_events = len(population)
disclosed = [d for d in population if d.get("laid_off") is not None]
n_disclosed = len(disclosed)
total_heads = sum(d["laid_off"] for d in disclosed)

max_event = max(disclosed, key=lambda d: d["laid_off"])
max_share = max_event["laid_off"] / total_heads

print(f"n events (population)            : {n_events}")
print(f"n events with disclosed laid_off  : {n_disclosed}")
print(f"total disclosed heads             : {total_heads:,}")
print(f"max single-event heads            : {max_event['company']} ({max_event['date']}) = "
      f"{max_event['laid_off']:,} heads = {fmt_pct(max_share)} of population disclosed heads")

assert n_disclosed == 103, f"expected 103 disclosed, got {n_disclosed}"
assert total_heads == 27929, f"expected 27929 total heads, got {total_heads}"


# ---------------------------------------------------------------------------
# Tiering logic (shared between population and all-events distortion check)
# ---------------------------------------------------------------------------
def classify_tier(d):
    link = d.get("ai_link")
    basis = d.get("ai_link_basis")
    if link == "direct_substitution" and basis == "company_stated":
        return "a_substitution_company_stated"
    if link == "capex_funding" and basis == "company_stated":
        return "b_capex_company_stated"
    if link in ("direct_substitution", "capex_funding") and basis != "company_stated":
        return f"c_ai_mechanism_press_inferred__basis={basis}"
    if link == "ai_narrative_only":
        if basis == "company_denied":
            return "d2_ai_narrative_only__company_denied"
        return "d1_ai_narrative_only__other_basis"
    if link == "unrelated":
        return "e_unrelated"
    return "f_other_unknown"


def tier_table(events, heads_denom, events_denom, label):
    """Return dict: tier -> (n_events, heads, event_pct, heads_pct)"""
    by_tier_events = Counter()
    by_tier_heads = Counter()
    for d in events:
        t = classify_tier(d)
        by_tier_events[t] += 1
        if d.get("laid_off") is not None:
            by_tier_heads[t] += d["laid_off"]

    print(f"\n--- {label} ---")
    print(f"{'tier':55s} {'n_ev':>6s} {'ev%':>7s} {'heads':>9s} {'heads%':>8s}")
    all_tiers = sorted(set(by_tier_events) | set(by_tier_heads))
    rows = {}
    for t in all_tiers:
        ne = by_tier_events[t]
        nh = by_tier_heads[t]
        ev_pct = ne / events_denom
        heads_pct = nh / heads_denom if heads_denom else 0.0
        rows[t] = (ne, nh, ev_pct, heads_pct)
        print(f"{t:55s} {ne:6d} {fmt_pct(ev_pct):>7s} {nh:9,d} {fmt_pct(heads_pct):>8s}")

    # combined company-stated AI mechanism (a+b)
    comb_ev = by_tier_events["a_substitution_company_stated"] + by_tier_events["b_capex_company_stated"]
    comb_heads = by_tier_heads["a_substitution_company_stated"] + by_tier_heads["b_capex_company_stated"]
    comb_ev_pct = comb_ev / events_denom
    comb_heads_pct = comb_heads / heads_denom if heads_denom else 0.0
    print(f"{'>>> COMBINED company-stated AI mechanism (a+b)':55s} {comb_ev:6d} "
          f"{fmt_pct(comb_ev_pct):>7s} {comb_heads:9,d} {fmt_pct(comb_heads_pct):>8s}")
    rows["COMBINED_company_stated_ai_mechanism"] = (comb_ev, comb_heads, comb_ev_pct, comb_heads_pct)

    # substitution-only and capex-only (company-stated) individually already in rows a/b
    return rows


# ---------------------------------------------------------------------------
# 2. AI-ATTRIBUTION TIERS (population)
# ---------------------------------------------------------------------------
hr("2. AI-ATTRIBUTION TIERS (148-event population; heads denom=27,929, events denom=148)")
pop_tiers = tier_table(population, heads_denom=total_heads, events_denom=n_events,
                        label="POPULATION (148 events)")


# ---------------------------------------------------------------------------
# 3. SIZE CLUSTERS
# ---------------------------------------------------------------------------
hr("3. SIZE CLUSTERS (implied company size = laid_off / pct, both non-null, pct>0)")

with_size = []
for d in population:
    lo = d.get("laid_off")
    pct = d.get("pct")
    if lo is not None and pct is not None and pct > 0:
        d = dict(d)
        d["_implied_size"] = lo / pct
        with_size.append(d)

n_disclosed_no_pct = sum(1 for d in population
                          if d.get("laid_off") is not None and
                          (d.get("pct") is None or d.get("pct") == 0))

print(f"n of 148 with both laid_off & pct (pct>0) : {len(with_size)}")
print(f"n disclosed-heads events lacking usable pct: {n_disclosed_no_pct}")

def cluster_of(size):
    if size < 500:
        return "<500"
    if size < 2000:
        return "500-2,000"
    if size < 10000:
        return "2,000-10,000"
    return ">10,000"

clusters = defaultdict(list)
for d in with_size:
    clusters[cluster_of(d["_implied_size"])].append(d)

cluster_order = ["<500", "500-2,000", "2,000-10,000", ">10,000"]

for c in cluster_order:
    members = clusters.get(c, [])
    if not members:
        print(f"\n--- cluster {c}: 0 events ---")
        continue
    n_ev = len(members)
    heads_list = [m["laid_off"] for m in members]
    total_c_heads = sum(heads_list)
    pcts = [m["pct"] for m in members]
    median_pct = stats.median(pcts)
    mean_pct = stats.mean(pcts)

    stated_ev = sum(1 for m in members if classify_tier(m) in
                     ("a_substitution_company_stated", "b_capex_company_stated"))
    stated_heads = sum(m["laid_off"] for m in members if classify_tier(m) in
                        ("a_substitution_company_stated", "b_capex_company_stated"))
    stated_ev_rate = stated_ev / n_ev
    stated_heads_rate = stated_heads / total_c_heads if total_c_heads else 0.0

    link_mix = Counter(m.get("ai_link") for m in members)
    basis_mix = Counter(m.get("ai_link_basis") for m in members)
    hire_mix = Counter(m.get("hire_overcorrection") for m in members)
    reason_mix = Counter(m.get("reason_primary") for m in members)
    top3_reasons = reason_mix.most_common(3)

    names = sorted(set(m["company"] for m in members))

    print(f"\n--- cluster {c}: n={n_ev} events, total heads={total_c_heads:,} ---")
    print(f"  median pct cut          : {fmt_pct(median_pct)}")
    print(f"  mean pct cut            : {fmt_pct(mean_pct)}")
    print(f"  company-stated-AI rate (events) : {stated_ev}/{n_ev} = {fmt_pct(stated_ev_rate)}")
    print(f"  company-stated-AI rate (heads)  : {stated_heads:,}/{total_c_heads:,} = {fmt_pct(stated_heads_rate)}")
    print(f"  ai_link mix             : {dict(link_mix)}")
    print(f"  ai_link_basis mix       : {dict(basis_mix)}")
    print(f"  hire_overcorrection mix : True={hire_mix.get(True,0)} False={hire_mix.get(False,0)} "
          f"None={hire_mix.get(None,0)}")
    print(f"  top-3 reason_primary    : {top3_reasons}")
    print(f"  companies (up to 8)     : {names[:8]}")


# ---------------------------------------------------------------------------
# 4. CUT-DEPTH BY MECHANISM (population only)
# ---------------------------------------------------------------------------
hr("4. CUT-DEPTH BY MECHANISM (population, pct available; n=148 events, subset with pct non-null)")

def cut_depth_by_group(events, group_key, min_n=1):
    groups = defaultdict(list)
    for d in events:
        pct = d.get("pct")
        if pct is None:
            continue
        groups[d.get(group_key)].append(pct)
    rows = {}
    for g, vals in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        if len(vals) < min_n:
            continue
        rows[g] = (len(vals), stats.median(vals), stats.mean(vals))
    return rows

print("\nBy ai_link:")
print(f"{'ai_link':22s} {'n(pct)':>7s} {'median pct':>12s} {'mean pct':>10s}")
by_link = cut_depth_by_group(population, "ai_link")
for g, (n, med, mean) in by_link.items():
    print(f"{str(g):22s} {n:7d} {fmt_pct(med):>12s} {fmt_pct(mean):>10s}")

print("\nBy reason_primary (n>=5 with pct available):")
print(f"{'reason_primary':28s} {'n(pct)':>7s} {'median pct':>12s} {'mean pct':>10s}")
by_reason = cut_depth_by_group(population, "reason_primary", min_n=5)
for g, (n, med, mean) in by_reason.items():
    print(f"{str(g):28s} {n:7d} {fmt_pct(med):>12s} {fmt_pct(mean):>10s}")


# ---------------------------------------------------------------------------
# 5. DISTORTION CHECK vs all 161 Jan-Jun events
# ---------------------------------------------------------------------------
hr("5. DISTORTION CHECK: 148-population vs 161 all-Jan-Jun-events (mega included)")

all_disclosed = [d for d in all_janjun if d.get("laid_off") is not None]
all_total_heads = sum(d["laid_off"] for d in all_disclosed)
print(f"all-events n={len(all_janjun)}, n disclosed={len(all_disclosed)}, total heads={all_total_heads:,}")
assert all_total_heads == 108089, f"expected 108,089 total heads for all events, got {all_total_heads}"

all_tiers = tier_table(all_janjun, heads_denom=all_total_heads, events_denom=len(all_janjun),
                        label="ALL 161 JAN-JUN EVENTS")

print("\nCut-depth by ai_link (ALL 161 events):")
print(f"{'ai_link':22s} {'n(pct)':>7s} {'median pct':>12s} {'mean pct':>10s}")
all_by_link = cut_depth_by_group(all_janjun, "ai_link")
for g, (n, med, mean) in all_by_link.items():
    print(f"{str(g):22s} {n:7d} {fmt_pct(med):>12s} {fmt_pct(mean):>10s}")

print("\nCut-depth by reason_primary (ALL 161 events, n>=5):")
print(f"{'reason_primary':28s} {'n(pct)':>7s} {'median pct':>12s} {'mean pct':>10s}")
all_by_reason = cut_depth_by_group(all_janjun, "reason_primary", min_n=5)
for g, (n, med, mean) in all_by_reason.items():
    print(f"{str(g):28s} {n:7d} {fmt_pct(med):>12s} {fmt_pct(mean):>10s}")

# ---- Build unified metric comparison table ----
hr("5b. METRICS THAT MOVE >5pp BETWEEN ALL-EVENTS AND POPULATION")

moved = []

def add_move(name, pop_val, all_val, unit="pp"):
    """pop_val, all_val are fractions (0-1). Records if |diff| > 0.05."""
    if pop_val is None or all_val is None:
        return
    diff = (all_val - pop_val) * 100
    moved.append((name, pop_val, all_val, diff))

# tier events% and heads% comparisons
tier_names = sorted(set(pop_tiers) | set(all_tiers))
for t in tier_names:
    pe = pop_tiers.get(t, (0, 0, 0.0, 0.0))
    ae = all_tiers.get(t, (0, 0, 0.0, 0.0))
    add_move(f"[events%] tier={t}", pe[2], ae[2])
    add_move(f"[heads%]  tier={t}", pe[3], ae[3])

# explicit headline numbers (always print regardless of threshold)
headline_pop = pop_tiers["COMBINED_company_stated_ai_mechanism"]
headline_all = all_tiers["COMBINED_company_stated_ai_mechanism"]
sub_pop = pop_tiers["a_substitution_company_stated"]
sub_all = all_tiers["a_substitution_company_stated"]
capex_pop = pop_tiers["b_capex_company_stated"]
capex_all = all_tiers["b_capex_company_stated"]

print("\nHEADLINE — company-stated AI mechanism (a+b), % of HEADS:")
print(f"  population : {fmt_pct(headline_pop[3])}  ({headline_pop[1]:,} / {total_heads:,})")
print(f"  all-events : {fmt_pct(headline_all[3])}  ({headline_all[1]:,} / {all_total_heads:,})")
print(f"  delta      : {(headline_all[3]-headline_pop[3])*100:+.1f} pp")

print("\nHEADLINE — company-stated AI mechanism (a+b), % of EVENTS:")
print(f"  population : {fmt_pct(headline_pop[2])}  ({headline_pop[0]} / {n_events})")
print(f"  all-events : {fmt_pct(headline_all[2])}  ({headline_all[0]} / {len(all_janjun)})")
print(f"  delta      : {(headline_all[2]-headline_pop[2])*100:+.1f} pp")

print("\nSUBSTITUTION-ONLY (company-stated direct_substitution), % of HEADS:")
print(f"  population : {fmt_pct(sub_pop[3])}   all-events : {fmt_pct(sub_all[3])}   "
      f"delta: {(sub_all[3]-sub_pop[3])*100:+.1f} pp")
print("SUBSTITUTION-ONLY, % of EVENTS:")
print(f"  population : {fmt_pct(sub_pop[2])}   all-events : {fmt_pct(sub_all[2])}   "
      f"delta: {(sub_all[2]-sub_pop[2])*100:+.1f} pp")

print("\nCAPEX-ONLY (company-stated capex_funding), % of HEADS:")
print(f"  population : {fmt_pct(capex_pop[3])}   all-events : {fmt_pct(capex_all[3])}   "
      f"delta: {(capex_all[3]-capex_pop[3])*100:+.1f} pp")
print("CAPEX-ONLY, % of EVENTS:")
print(f"  population : {fmt_pct(capex_pop[2])}   all-events : {fmt_pct(capex_all[2])}   "
      f"delta: {(capex_all[2]-capex_pop[2])*100:+.1f} pp")

# cut-depth by mechanism medians comparison
for g in sorted(set(by_link) | set(all_by_link)):
    p = by_link.get(g)
    a = all_by_link.get(g)
    if p and a:
        add_move(f"[median pct] ai_link={g}", p[1], a[1])
    if p and a:
        add_move(f"[mean pct]   ai_link={g}", p[2], a[2])

for g in sorted(set(by_reason) | set(all_by_reason)):
    p = by_reason.get(g)
    a = all_by_reason.get(g)
    if p and a:
        add_move(f"[median pct] reason_primary={g}", p[1], a[1])
        add_move(f"[mean pct]   reason_primary={g}", p[2], a[2])

print("\n\nALL METRICS moving by >5.0 percentage points (population -> all-events):")
print(f"{'metric':55s} {'pop':>8s} {'all':>8s} {'delta(pp)':>10s}")
big_moves = [m for m in moved if round(abs(m[3]), 6) > 5.0]
big_moves.sort(key=lambda m: -abs(m[3]))
if not big_moves:
    print("  (none found beyond the headline metrics explicitly listed above)")
for name, pv, av, diff in big_moves:
    print(f"{name:55s} {fmt_pct(pv):>8s} {fmt_pct(av):>8s} {diff:>+9.1f}pp")

hr("DONE")
