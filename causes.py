#!/usr/bin/env python3
"""
causes.py — multi-causal tagging layer (added 2026-09, additive).

Reframe: whether a company *uses* AI is irrelevant. The thing in dispute is
the CLAIM "we replaced X jobs with AI". Layoffs are multi-causal, so every
event carries a LIST of cause tags instead of one bucket, plus a verdict that
grades ONLY the AI-substitution claim when one was made.

Three new keys per event (written by categorize.py into 2026-categorized.json;
no existing column is touched):

  causes            list[str]  — cause tags from CAUSE_VOCAB (>=1, orthogonal
                                 within the AI cluster: at most one ai_* tag)
  cause_evidence    dict       — tag -> short note saying what the tag rests on
  ai_claim_verdict  str        — grades the AI-substitution claim only

Derivation is mechanical from the existing axes (reason_primary, ai_link,
ai_link_basis, hire_overcorrection, story_integrity, backfill_verdict,
revenue_health) plus a small per-event override dict (CAUSE_OVERRIDES) for
facts already documented in the reason text / CROSS_CHECK notes that the
single-value axes could not carry (e.g. WiseTech's e2open merger, Vimeo's
Bending Spoons pattern, Block's named rehires).

Run standalone for the tag cross-tabs:  python3 causes.py
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

CAUSE_VOCAB = {
    # --- the AI cluster: mutually exclusive, exactly what the company (or press) said ---
    "ai_substitution_claim":   "THE DISPUTED CLAIM: the company itself says AI does/reduces the cut work (ai_link=direct_substitution, basis company_stated/company_informal)",
    "ai_capex_reallocation":   "company says payroll is cut to fund AI investment/infra (real, but not substitution)",
    "ai_framing_vague":        "company invoked AI ('AI era', 'AI-first') without stating a mechanism",
    "ai_press_narrative":      "AI angle added by press/analysts only; company gave a non-AI reason or none",
    "ai_denied":               "company explicitly denied AI as the cause (verified denial language)",
    # --- financial / structural causes (co-occur freely) ---
    "over_hiring":             "SEC/Workforce.ai-verified prior headcount spike (2-yr growth >= ~15% organic) being unwound",
    "cost_cutting":            "explicit margin / savings / profitability target or cost-discipline language",
    "restructuring_unspecified": "'aligning with priorities' / 'reducing layers' — no concrete mechanism stated",
    "financial_distress":      "revenue/profit weakness on the record (revenue_health=weakness, same-day guidance cut, losses)",
    "demand_collapse":         "sector or market downturn (5G capex, crypto cycle, engagement decline)",
    "new_ceo_turnaround":      "new/incoming CEO uses the cut as a signaling event",
    "m_and_a":                 "post-acquisition overlap, merger integration, or acquirer's cost pattern",
    "strategic_pivot":         "company changes product/market (incl. pivot into AI as a market)",
    "shutdown":                "company closes (100% layoff / bankruptcy)",
    "market_exit":             "specific contract lost or country/market exited",
    "offshoring":              "roles moved to cheaper geographies (labor arbitrage, not AI)",
    "rehiring_same_roles":     "re-posted the roles it cut (documented same-role reqs post-cut)",
    "performance_cull":        "framed as a performance-review separation",
    "ipo_prep":                "streamlining ahead of a stated IPO",
    "regulatory":              "regulatory change forced the cut",
    "unknown":                 "public source not accessible; no cause recoverable",
}

AI_CLAIM_VERDICTS = {
    "plausible":              "substitution claimed AND external evidence does not contradict it (story_integrity=holds). Means 'not contradicted', NOT 'proven' — the cut can still be multi-causal (e.g. also over_hiring). MercadoLibre is the only one with no competing cause.",
    "thin_evidence":          "substitution claimed but not externally testable (informal channel, no cross-check, or event unverifiable)",
    "contradicted_soft":      "substitution claimed but >=1 material fact cuts against it (same-day guidance cut, M&A synergy in AI clothing, inflated headline, backfill reqs)",
    "contradicted_hard":      "substitution claimed but rehiring of the same roles, offshoring, or self-contradiction is documented",
    "capex_not_substitution": "company's own framing is capex reallocation, not replacement — no substitution claim to grade",
    "not_claimed":            "no company substitution claim (unrelated, press-only, vague framing, or denied)",
}

# Per-event refinements. "add"/"remove" edit the derived tag list; "evidence"
# attaches notes; "verdict" forces ai_claim_verdict. Every fact below is
# already in the event's `reason` text or in categorize.py's CROSS_CHECK notes.
CAUSE_OVERRIDES = {
    ("Oracle", "2026-03-31"): {
        "add": ["m_and_a", "cost_cutting"],
        "evidence": {
            "ai_substitution_claim": "FY26 10-K Item 1A RISK FACTORS (verified 2026-09-02): AI deployment 'have resulted, and may continue to result, in reductions to our workforce' — one hedged sentence bundled with management/product/performance/acquisition drivers; Note 7: restructuring 'including through the adoption and integration of AI technologies across certain functions'. No AI-attributable headcount; filed ~3 months after a cut explained in March only as 'a broader organizational change'",
            "m_and_a": "the only headcount Oracle added FY22->FY23 came from Cerner (~25k); Oracle Health/Cerner cut every year since; the 539-person KC WARN is the only company-confirmed unit figure (the 8-10k Health number is a TD Cowen estimate)",
            "cost_cutting": "Note 7: 2026 Restructuring Plan 'to further improve operational efficiencies', $1.78B FY26 expense, up to $2.1B; press framed the cut as funding the ~$50B AI capex push (the viral Catz/Ellison capex quotes are untraceable)",
        },
        # thin, not contradicted: the claim itself is unquantified risk-factor
        # language; the 30k-vs-21k crack is a press-headline problem, and the net
        # 141k figure absorbs OCI/AI hiring so backfill cannot be tested.
        "verdict": "thin_evidence",
    },
    ("Block", "2026-02-26"): {
        "add": ["rehiring_same_roles"],
        "evidence": {
            "rehiring_same_roles": "Business Insider (2026-03): at least 4 named laid-off employees rehired into the same roles within weeks (backfill_verdict left at ai_only by the July pass; the named rehires are the harder fact)",
            "ai_substitution_claim": "Dorsey 8-K shareholder letter: teams 'using AI to automate more work'; +127% 2-yr headcount before the cut",
        },
        "verdict": "contradicted_hard",
    },
    ("Snap", "2026-04-15"): {
        "add": ["cost_cutting"],
        "evidence": {
            "cost_cutting": "$500M+ annualized savings target; stock jumped on the news",
            "ai_substitution_claim": "Spiegel: AI reduces 'repetitive work' enabling smaller teams; 250+ broad open reqs post-cut (backfill_verdict=mixed) — partial backfill, not documented same-role rehiring",
        },
    },
    ("PayPal", "2026-05-05"): {
        "add": ["cost_cutting", "financial_distress"],
        "evidence": {
            "new_ceo_turnaround": "Lores took over March 1, 2026; cut announced 9 weeks in",
            "cost_cutting": ">= $1.5B annualized run-rate savings target, 2-3 year program",
            "financial_distress": "announced alongside weaker-than-expected Q1 profit; EPS guided down same day",
            "ai_substitution_claim": "'AI-native operating model' framing; cuts phased to 2028 so no backfill test yet",
        },
    },
    ("WiseTech", "2026-02-24"): {
        "add": ["m_and_a"],
        "evidence": {
            "m_and_a": "~$2.1B e2open acquisition doubled headcount to ~7,000; up to ~half the 2,000 cuts land on e2open (merger integration in AI clothing)",
            "ai_substitution_claim": "ASX release + CEO Appoo: 'the era of manually writing code... is over'; only ~500 of 2,000 executed in H1 FY26",
        },
    },
    ("Livspace", "2026-02-20"): {
        "evidence": {"rehiring_same_roles": "138 live listings in the exact cut role families within weeks of the cut"},
    },
    ("Freshworks", "2026-05-05"): {
        "evidence": {"rehiring_same_roles": "Chennai support trainee req on Freshworks' own ATS ~7 weeks post-cut"},
    },
    ("ZoomInfo", "2026-05-11"): {
        "add": ["cost_cutting"],
        "evidence": {
            "offshoring": "own 8-K: Israel R&D closed, roles reallocated incl. to India",
            "cost_cutting": "~$60M annual savings target",
            "financial_distress": "guidance cut to ~1% growth",
        },
    },
    ("Cloudflare", "2026-05-07"): {
        "evidence": {
            "rehiring_same_roles": "CEO vowed to exceed 2026 headcount by 2027; sales spared; rehiring in cut functions (CROSS_CHECK)",
            "ai_framing_vague": "'agentic AI era' reorg; internal AI usage +600% cited, no substitution mechanism stated",
        },
    },
    ("Robinhood", "2026-06-16"): {
        "evidence": {
            "rehiring_same_roles": "CX reqs posted in layoff-hit hub cities, one on layoff day",
            "ai_press_narrative": "Tenev memo said 'frontier technologies', never 'AI'; the AI angle is TechCrunch et al.",
        },
    },
    ("Playtika", "2026-01-14"): {
        "add": ["demand_collapse"],
        "evidence": {"demand_collapse": "6th round of secular decline; focus on fewer games", "offshoring": "Israel -> Bucharest (thin)"},
    },
    ("UKG", "2026-04-15"): {
        "evidence": {"offshoring": "CROSS_CHECK offshore_swap; +3,100 cut since 2024 under PE owner Hellman & Friedman"},
    },
    ("Coinbase", "2026-05-05"): {
        "add": ["demand_collapse"],
        "evidence": {"demand_collapse": "company-stated crypto market downturn as co-driver"},
    },
    ("Kraken", "2026-05-15"): {
        "add": ["demand_collapse", "financial_distress"],
        "evidence": {"demand_collapse": "crypto market decline; IPO filing paused", "financial_distress": "Q1 EBITDA -90% disclosed 3 days post-layoff"},
    },
    ("Crypto.com", "2026-03-19"): {
        "add": ["demand_collapse"],
        "evidence": {"demand_collapse": "3rd round since 2022, crypto-cycle downturn"},
    },
    ("C3.ai", "2026-02-25"): {
        "add": ["cost_cutting", "over_hiring"],
        "evidence": {"financial_distress": "wider loss, stock drop; CEO: cost structure 'simply too high'", "over_hiring": "company-admitted: CEO said aggressive 2024-25 hiring outpaced enterprise AI adoption (his own words)"},
    },
    ("Upwork", "2026-05-07"): {
        "add": ["financial_distress", "cost_cutting"],
        "evidence": {"financial_distress": "same-day ~9% guidance cut on +1% growth", "cost_cutting": "profitability goals cited"},
    },
    ("Wix", "2026-05-25"): {
        "add": ["financial_distress", "cost_cutting"],
        "evidence": {"financial_distress": "weak earnings, ~50% stock decline", "cost_cutting": "rising AI compute costs from Base44 acquisition"},
    },
    ("GitLab", "2026-06-03"): {
        "add": ["market_exit"],
        "evidence": {"market_exit": "exit from 22 countries", "ai_capex_reallocation": "narrative flip: May 11 'not an AI optimization or cost cutting exercise' -> June 3 'fund AI infrastructure buildout'"},
    },
    ("Atlassian", "2026-03-11"): {
        "evidence": {"ai_capex_reallocation": "Cannon-Brookes: 'self-fund further investment in AI and enterprise sales'; no verifiable capex commitment; chronic GAAP losses"},
    },
    ("Meta", "2026-05-20"): {
        "evidence": {"ai_capex_reallocation": "~7,000 redeployed into AI orgs; capex raised — money goes where the story says"},
    },
    ("Vimeo", "2026-01-21"): {"add": ["m_and_a"], "evidence": {"m_and_a": "two months after Bending Spoons' $1.38B acquisition; matches WeTransfer/Filmic post-acquisition pattern"}},
    ("Vimeo", "2026-04-03"): {"add": ["m_and_a"], "evidence": {"m_and_a": "second reduction since the Bending Spoons acquisition"}},
    ("eBay", "2026-02-26"): {"add": ["m_and_a"], "evidence": {"m_and_a": "followed $1.2B Depop acquisition; 'areas of duplication'"}},
    ("Staffbase", "2026-05-08"): {"add": ["m_and_a"], "evidence": {"m_and_a": "'reducing complexity after three acquisitions'; sites consolidated to Berlin/Saxony"}},
    ("Intuit", "2026-05-20"): {"evidence": {"ai_denied": "Goodarzi on CNBC: 'None of it had to do with AI'", "restructuring_unspecified": "hub consolidation (Reno, Woodland Hills wound down)"}},
    ("Amazon", "2026-01-28"): {"evidence": {"ai_denied": "spokesperson to AP: AI 'not the reason behind the vast majority of these reductions'"}},
    ("GoPro", "2026-04-07"): {"add": ["financial_distress"], "evidence": {"financial_distress": "2025 revenue decline, $9M Q4 loss; weighing a sale"}},
    ("Zendesk", "2026-03-24"): {"add": ["ai_framing_vague"], "evidence": {"ai_framing_vague": "internal memo only, no external footprint (Forethought AI agents cited); excluded from the substitution-claim count for lack of a public source"}},
    ("Parker", "2026-05-09"): {"add": ["over_hiring"], "evidence": {"over_hiring": "company-admitted: CEO hinted at over-hiring and reactive decisions"}},
    ("Expedia", "2026-01-26"): {"evidence": {"ai_press_narrative": "statement cites layers/skills; AI appears as 'enhance AI-driven experiences' — press inferred substitution"}},
    ("Digg", "2026-03-13"): {"evidence": {"ai_framing_vague": "'AI broke the product' (bot spam), not labor substitution"}},
    ("Epidemic Sound", "2026-04-21"): {"evidence": {"financial_distress": "2025 growth 29% -> 3%, negative EBITDA, despite 'not financially driven' line"}},
    ("MercadoLibre", "2026-01-12"): {"evidence": {"ai_substitution_claim": "narrow claim (UX writers) while net-adding ~42k jobs; affected workers trained the replacing AI"}},
    ("Multiverse", "2026-01-05"): {"add": ["cost_cutting"], "evidence": {"cost_cutting": "'revenue per employee' target, rising staff costs"}},
    ("Pocket FM", "2026-05-06"): {"add": ["performance_cull"], "evidence": {"performance_cull": "framed as regular performance-based reviews"}},
}

_COST_RE = re.compile(
    r"\$[\d.,]+ ?[MBmb]\b.{0,40}(saving|cost)|savings|margin|profitab|cost structure|cost base|"
    r"reduce costs|lower costs|cut costs|cost[- ]cutting|staff costs|revenue per employee|operating costs",
    re.I,
)
_PERF_RE = re.compile(r"performance[- ]based|performance review", re.I)
_DEMAND_RE = re.compile(r"downturn|market decline|crypto market|slowdown|engagement decline|demand (decline|slump|drop)", re.I)


def derive_causes(e):
    """Return {"causes": [...], "cause_evidence": {...}, "ai_claim_verdict": str} for one event."""
    rp = e.get("reason_primary")
    link = e.get("ai_link")
    basis = e.get("ai_link_basis")
    si = e.get("story_integrity")
    bf = e.get("backfill_verdict")
    rh = e.get("revenue_health")
    reason = e.get("reason") or ""
    tags, ev = [], {}

    def add(tag, note=None):
        if tag not in tags:
            tags.append(tag)
        if note and tag not in ev:
            ev[tag] = note

    # --- AI cluster (one tag max) ---
    company_said = basis in ("company_stated", "company_informal")
    if basis == "company_denied":
        add("ai_denied", f"ai_link_basis=company_denied")
    # only an on-record company claim counts. unknown-basis (e.g. Zendesk, internal
    # memo with no external footprint) and press/analyst inference never count as a
    # company claim of substitution.
    elif link == "direct_substitution" and company_said:
        add("ai_substitution_claim", f"ai_link=direct_substitution, basis={basis}" + (" (informal channel: tweet/LinkedIn/spokesperson)" if basis == "company_informal" else ""))
    elif link == "capex_funding" and company_said:
        add("ai_capex_reallocation", f"ai_link=capex_funding, basis={basis}")
    elif link == "ai_narrative_only" and company_said:
        add("ai_framing_vague", f"ai_link=ai_narrative_only, basis={basis}")
    elif link in ("direct_substitution", "capex_funding", "ai_narrative_only") and basis in ("press_inferred", "analyst_inferred"):
        add("ai_press_narrative", f"ai_link={link}, basis={basis} — not a company claim")

    # --- structural causes from reason_primary ---
    rp_map = {
        "cost_cutting": "cost_cutting", "path_to_profitability": "cost_cutting",
        "restructuring_vague": "restructuring_unspecified",
        "demand_collapse": "demand_collapse",
        "new_ceo_turnaround": "new_ceo_turnaround",
        "m_and_a_consolidation": "m_and_a",
        "strategic_pivot": "strategic_pivot",
        "shutdown_bankruptcy": "shutdown",
        "lost_contract_market_exit": "market_exit",
        "geographic_relocation": "offshoring",
        "ipo_prep": "ipo_prep", "regulatory": "regulatory",
        "unknown": "unknown",
    }
    if rp in rp_map:
        add(rp_map[rp], f"reason_primary={rp}")

    # --- verified facts from the audit axes ---
    # over_hiring is NOT read from the headcount flag (window-dependent + audit-biased);
    # the trajectory lives on the `headcount_path` axis, and over_hiring enters `causes`
    # only when the company itself admitted it (via CAUSE_OVERRIDES: C3.ai, Parker).
    # rehiring_same_roles enters only via CAUSE_OVERRIDES with a citable source (Block);
    # the raw backfill flag is not publishable (dynamic job boards, unarchived).
    if bf == "offshore_swap":
        add("offshoring", "backfill_verdict=offshore_swap")
    if rh == "weakness":
        add("financial_distress", "revenue_health=weakness (last quarter before the cut)")

    # --- text signals (conservative) ---
    if _COST_RE.search(reason):
        add("cost_cutting", "explicit savings/margin/profitability language in the public reason")
    if _PERF_RE.search(reason):
        add("performance_cull", "performance-review framing in the public reason")
    if _DEMAND_RE.search(reason):
        add("demand_collapse", "downturn/decline language in the public reason")

    # --- per-event refinements ---
    ov = CAUSE_OVERRIDES.get((e["company"], e["date"]), {})
    for t in ov.get("add", []):
        add(t)
    for t in ov.get("remove", []):
        if t in tags:
            tags.remove(t)
            ev.pop(t, None)
    ev.update(ov.get("evidence", {}))

    if not tags:
        add("unknown", "no cause recoverable from the axes")
    # `unknown` only stands alone
    if "unknown" in tags and len(tags) > 1:
        tags.remove("unknown"); ev.pop("unknown", None)

    # --- verdict on the substitution claim only ---
    if "ai_substitution_claim" in tags:
        if si == "busted" or "rehiring_same_roles" in tags or "offshoring" in tags:
            verdict = "contradicted_hard"
        elif si == "cracked":
            verdict = "contradicted_soft"
        elif si == "holds":
            verdict = "plausible"
        else:
            verdict = "thin_evidence"
    elif "ai_capex_reallocation" in tags:
        verdict = "capex_not_substitution"
    else:
        verdict = "not_claimed"
    if "verdict" in ov:
        verdict = ov["verdict"]

    unknown_tags = set(tags) - set(CAUSE_VOCAB)
    if unknown_tags:
        raise SystemExit(f"{e['company']} {e['date']}: tags outside CAUSE_VOCAB: {sorted(unknown_tags)}")
    return {"causes": tags, "cause_evidence": {t: ev[t] for t in tags if t in ev}, "ai_claim_verdict": verdict}


def summarize(events, window_end="2026-07-01"):
    ev = [e for e in events if e["date"] < window_end]
    print(f"\n=== causes summary: {len(ev)} events (date < {window_end}) ===")
    freq = Counter(t for e in ev for t in e["causes"])
    heads = Counter()
    for e in ev:
        for t in e["causes"]:
            heads[t] += e.get("laid_off") or 0
    print("\ntag                         events   heads")
    for t, n in freq.most_common():
        print(f"  {t:26} {n:5}   {heads[t]:7,}")
    print(f"\ntags per event: mean {sum(len(e['causes']) for e in ev)/len(ev):.2f}, "
          f"multi-tagged: {sum(len(e['causes'])>1 for e in ev)}/{len(ev)}")
    print("\nai_claim_verdict:")
    for v, n in Counter(e["ai_claim_verdict"] for e in ev).most_common():
        h = sum(e.get("laid_off") or 0 for e in ev if e["ai_claim_verdict"] == v)
        print(f"  {v:24} {n:4}  {h:8,} heads")
    sub = [e for e in ev if "ai_substitution_claim" in e["causes"]]
    print(f"\nco-occurrence with ai_substitution_claim ({len(sub)} events, {sum(e.get('laid_off') or 0 for e in sub):,} heads):")
    for t, n in Counter(t for e in sub for t in e["causes"] if t != "ai_substitution_claim").most_common():
        print(f"  + {t:26} {n:3}  ({', '.join(e['company'] for e in sub if t in e['causes'])})")
    print("\nsubstitution claims by verdict:")
    for v in ("plausible", "thin_evidence", "contradicted_soft", "contradicted_hard"):
        names = [f"{e['company']} {e.get('laid_off') or '?'}" for e in sub if e["ai_claim_verdict"] == v]
        print(f"  {v:18} {len(names):3}: {', '.join(names)}")


if __name__ == "__main__":
    events = json.load(open(ROOT / "2026-categorized.json"))
    if "causes" not in events[0]:
        for e in events:
            e.update(derive_causes(e))
    summarize(events)
