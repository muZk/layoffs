#!/usr/bin/env python3
"""
01_cutoff.py

Establish a principled "mega-event" cutoff for headline layoff statistics,
using an iterative dominance rule, and write the mega/population split to disk.
"""
import json
from pathlib import Path

BASE = Path("/Users/muzk/code/layoffs")
IN_PATH = BASE / "2026-categorized.json"
OUT_DIR = BASE / "analysis-twolens"
OUT_PATH = OUT_DIR / "split.json"

EXCLUDE = {
    ("Microsoft (Xbox)", "2026-07-06"),
    ("Microsoft (corporate)", "2026-07-06"),
}


def pct_fmt(x):
    return f"{x*100:.2f}%"


def main():
    data = json.loads(IN_PATH.read_text())
    print(f"Loaded {len(data)} raw events from {IN_PATH.name}")

    excluded = [r for r in data if (r["company"], r["date"]) in EXCLUDE]
    events = [r for r in data if (r["company"], r["date"]) not in EXCLUDE]

    print(f"Excluded {len(excluded)} events (Microsoft 2026-07-06 x2):")
    for r in excluded:
        print(f"  - {r['company']} | {r['date']} | laid_off={r['laid_off']}")

    print()
    print("=" * 70)
    print("STEP 1: Post-exclusion event count")
    print("=" * 70)
    print(f"Remaining events: {len(events)}  (expected 161)")

    disclosed = [r for r in events if r.get("laid_off") is not None]
    total_disclosed_heads = sum(r["laid_off"] for r in disclosed)
    print(f"Events with non-null laid_off: {len(disclosed)}")
    print(f"Events with null laid_off: {len(events) - len(disclosed)}")
    print(f"Total disclosed heads: {total_disclosed_heads:,}")

    print()
    print("=" * 70)
    print("STEP 2: Size distribution of disclosed events")
    print("=" * 70)

    disclosed_sorted = sorted(disclosed, key=lambda r: r["laid_off"], reverse=True)

    print()
    print("Top 20 events by laid_off:")
    print(f"{'#':>3} {'company':<30} {'date':<12} {'laid_off':>10} {'% of total disclosed':>22}")
    for i, r in enumerate(disclosed_sorted[:20], start=1):
        share = r["laid_off"] / total_disclosed_heads
        print(f"{i:>3} {r['company']:<30} {r['date']:<12} {r['laid_off']:>10,} {pct_fmt(share):>22}")

    # Percentiles
    def percentile(sorted_asc, p):
        # simple linear-interpolation percentile (like numpy default)
        n = len(sorted_asc)
        if n == 1:
            return sorted_asc[0]
        k = (n - 1) * p
        f = int(k)
        c = min(f + 1, n - 1)
        if f == c:
            return sorted_asc[f]
        d0 = sorted_asc[f] * (c - k)
        d1 = sorted_asc[c] * (k - f)
        return d0 + d1

    heads_asc = sorted(r["laid_off"] for r in disclosed)
    percentiles = {
        "p50": percentile(heads_asc, 0.50),
        "p75": percentile(heads_asc, 0.75),
        "p90": percentile(heads_asc, 0.90),
        "p95": percentile(heads_asc, 0.95),
        "p99": percentile(heads_asc, 0.99),
        "max": heads_asc[-1],
    }
    print()
    print("Percentiles of laid_off among disclosed events:")
    for k, v in percentiles.items():
        print(f"  {k}: {v:,.1f}")

    # Gaps: ratio between consecutive events when sorted descending
    print()
    print("Top-10 gaps (ratio of event[i] / event[i+1], sorted descending by laid_off):")
    gaps = []
    for i in range(len(disclosed_sorted) - 1):
        a = disclosed_sorted[i]["laid_off"]
        b = disclosed_sorted[i + 1]["laid_off"]
        if b == 0:
            continue
        ratio = a / b
        gaps.append((ratio, i, disclosed_sorted[i], disclosed_sorted[i + 1]))
    gaps_sorted = sorted(gaps, key=lambda x: x[0], reverse=True)
    for ratio, i, hi, lo in gaps_sorted[:10]:
        print(
            f"  rank {i+1}->{i+2}: {hi['company']} ({hi['laid_off']:,}) / "
            f"{lo['company']} ({lo['laid_off']:,}) = {ratio:.3f}x"
        )

    print()
    print("=" * 70)
    print("STEP 3: Iterative dominance rule for mega-event cutoff")
    print("=" * 70)

    def iterative_dominance(events_sorted_desc, threshold):
        """
        Sort disclosed events by laid_off descending (already done).
        Repeatedly: R = total heads of all not-yet-mega events.
        If largest remaining event's heads > threshold * (R - that event's own heads),
        mark it mega and repeat. Stop when largest remaining <= threshold * (R - its own heads).
        Returns (mega_list, log_lines).
        """
        remaining = list(events_sorted_desc)  # still sorted desc since we pop from front
        mega = []
        log = []
        while remaining:
            R = sum(r["laid_off"] for r in remaining)
            largest = remaining[0]
            rest = R - largest["laid_off"]
            if rest <= 0:
                # only one event left; can't compute a meaningful "remaining population" share
                break
            share = largest["laid_off"] / rest
            if share > threshold:
                mega.append(largest)
                log.append((largest["company"], largest["date"], largest["laid_off"], share))
                remaining.pop(0)
            else:
                break
        return mega, log, remaining

    print()
    print("--- Primary: 5% iterative threshold ---")
    mega_5, log_5, remaining_5 = iterative_dominance(disclosed_sorted, 0.05)
    for company, date, heads, share in log_5:
        print(f"  MEGA: {company:<30} {date:<12} heads={heads:>10,}  share_of_rest={pct_fmt(share)}")
    print(f"  -> {len(mega_5)} mega events under 5% rule")

    print()
    print("--- Comparison: 8% iterative threshold ---")
    mega_8, log_8, remaining_8 = iterative_dominance(disclosed_sorted, 0.08)
    for company, date, heads, share in log_8:
        print(f"  MEGA: {company:<30} {date:<12} heads={heads:>10,}  share_of_rest={pct_fmt(share)}")
    print(f"  -> {len(mega_8)} mega events under 8% rule")

    print()
    print("--- Comparison: 10% iterative threshold ---")
    mega_10, log_10, remaining_10 = iterative_dominance(disclosed_sorted, 0.10)
    for company, date, heads, share in log_10:
        print(f"  MEGA: {company:<30} {date:<12} heads={heads:>10,}  share_of_rest={pct_fmt(share)}")
    print(f"  -> {len(mega_10)} mega events under 10% rule")

    print()
    print("--- Natural gap among top ~15 events ---")
    top15_gaps = [g for g in gaps if g[1] < 15]
    top15_gaps_sorted = sorted(top15_gaps, key=lambda x: x[0], reverse=True)
    biggest = top15_gaps_sorted[0]
    ratio, i, hi, lo = biggest
    print(
        f"  Largest gap in top 15: between rank {i+1} ({hi['company']}, {hi['laid_off']:,}) "
        f"and rank {i+2} ({lo['company']}, {lo['laid_off']:,}) = {ratio:.3f}x"
    )
    print(f"  -> Natural break suggests cutoff after rank {i+1} ({len(mega_5) if False else i+1} events as mega)")

    natural_gap_mega_count = i + 1

    print()
    print("--- Agreement across approaches ---")
    print(f"  5% iterative rule:  {len(mega_5)} mega events -> {[r['company'] for r in mega_5]}")
    print(f"  8% iterative rule:  {len(mega_8)} mega events -> {[r['company'] for r in mega_8]}")
    print(f"  10% iterative rule: {len(mega_10)} mega events -> {[r['company'] for r in mega_10]}")
    print(f"  Natural gap (top15): {natural_gap_mega_count} events would be 'mega' if cut there "
          f"-> {[r['company'] for r in disclosed_sorted[:natural_gap_mega_count]]}")

    same_set = (
        {r["company"] for r in mega_5} == {r["company"] for r in mega_8} == {r["company"] for r in mega_10}
    )
    if same_set:
        print(f"  AGREEMENT: 5%, 8%, and 10% iterative rules all agree on the same {len(mega_5)}-event mega set.")
    else:
        print("  NOTE: iterative rules at different thresholds do NOT all select the identical set.")
    if {r["company"] for r in mega_5} == {r["company"] for r in disclosed_sorted[:natural_gap_mega_count]}:
        print("  The natural-gap break also lands at the same cutoff as the 5% rule.")
    else:
        print("  The natural-gap break does NOT land at exactly the same cutoff as the 5% rule.")

    print()
    print("=" * 70)
    print("STEP 4: Verify population under 5%-iterative cutoff")
    print("=" * 70)

    # Population = all events (disclosed + null) minus mega_5
    mega_keys = {(r["company"], r["date"]) for r in mega_5}
    population = [r for r in events if (r["company"], r["date"]) not in mega_keys]
    population_disclosed = [r for r in population if r.get("laid_off") is not None]
    population_total_heads = sum(r["laid_off"] for r in population_disclosed)

    max_share = 0.0
    max_share_company = None
    for r in population_disclosed:
        share = r["laid_off"] / population_total_heads
        if share > max_share:
            max_share = share
            max_share_company = r

    print(f"Population size (mega excluded): {len(population)} events "
          f"({len(population_disclosed)} disclosed, total heads={population_total_heads:,})")
    print(f"Max single-event share of population disclosed heads: "
          f"{max_share_company['company']} = {pct_fmt(max_share)}")
    if max_share <= 0.10:
        print("  CONFIRMED: no single event exceeds 10% of population's disclosed heads.")
    else:
        print("  WARNING: a single event EXCEEDS 10% of population's disclosed heads!")

    print()
    print("=" * 70)
    print("STEP 5: Write split.json")
    print("=" * 70)

    total_all_heads = total_disclosed_heads  # heads among all 161 disclosed events
    mega_total_heads = sum(r["laid_off"] for r in mega_5)
    mega_share_of_total = mega_total_heads / total_all_heads if total_all_heads else 0

    split = {
        "cutoff_rule": (
            "Iterative dominance rule (5% threshold): sort disclosed events by laid_off "
            "descending; repeatedly mark the largest remaining event as 'mega' if its heads "
            "exceed 5% of the heads of the rest of the not-yet-mega population (i.e. "
            "heads / (remaining_total - heads) > 0.05); stop when the largest remaining event "
            "no longer clears that bar. Applied to the 161 events after excluding the two "
            "Microsoft 2026-07-06 events (outside the Jan-Jun 2026 analysis window)."
        ),
        "mega_events": [
            {"company": r["company"], "date": r["date"], "laid_off": r["laid_off"]}
            for r in mega_5
        ],
        "population_keys": [[r["company"], r["date"]] for r in population],
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(split, indent=2))

    print(f"Wrote {OUT_PATH}")
    print(f"  mega_events: {len(split['mega_events'])} "
          f"(total heads={mega_total_heads:,}, {pct_fmt(mega_share_of_total)} of total disclosed heads)")
    print(f"  population_keys: {len(split['population_keys'])} "
          f"(expected {len(events)} - {len(mega_5)} = {len(events) - len(mega_5)})")

    assert len(split["population_keys"]) == len(events) - len(mega_5)
    assert len(events) == 161, f"Expected 161 events after exclusion, got {len(events)}"

    print()
    print("Done.")


if __name__ == "__main__":
    main()
