"""
Categorize the 160 2026 layoff entries across 3 axes:
  - reason_primary: financial/strategic root cause (15 values)
  - ai_link: relationship to the AI cycle (6 values)
  - narrative_source: evidence quality (6 values)

Plus optional enrichment columns where data exists:
  - profiles_cut, profiles_hired (from deep-research)
  - hire_overcorrection (from Pragmatic Engineer + Workforce.ai data)
  - reassignment_observed (Meta-style redeployment vs layoff)

Outputs:
  - 2026-categorized.json (full structured records)
  - 2026-categorized.csv (flat tabular view)
"""

import json
import csv
import re
from pathlib import Path

ROOT = Path("/Users/muzk/code/layoffs")

# ---------------------------------------------------------------------------
# Manual ai_position: company's business-model relationship to the AI economy
# ---------------------------------------------------------------------------
# compute_seller   = sells compute/AI capacity to third parties (cloud AI providers,
#                    AI model APIs). Wins when AI usage ↑.
# infra_seller     = sells hardware/silicon/networking that enables AI. Wins when
#                    AI capex spend ↑.
# vertical_builder = builds own AI stack (models, silicon, datacenters) end-to-end
#                    for own products. Doesn't sell AI to third parties. Bets value
#                    flows through downstream products (ads, devices, agents).
# token_buyer      = pays third-party providers (Anthropic, OpenAI, Microsoft) for
#                    AI capability through APIs / partnerships. Margin squeezed
#                    when token prices ↑.
# hybrid           = combines two or more (Amazon AWS+Trainium+Bedrock+Nova, etc.)
# n/a              = AI is not material to the business model (telecom 5G,
#                    regulatory shutdowns, M&A overlap unrelated to AI, etc.)
#
# Keyed by company name (not date) since position is structural per-company.
AI_POSITION = {  # deduped + guarded 2026-08 (was 201 entries w/ 39 dup keys; recovered 3 miscased, dropped 6 dead)
    "0G": "n/a",
    "AI21 Labs": "compute_seller",
    "ASML": "infra_seller",
    "Acko": "token_buyer",
    "Adda247": "token_buyer",
    "Aleph Alpha": "compute_seller",
    "Amazon": "hybrid",
    "Angi": "token_buyer",
    "ApnaMart": "token_buyer",
    "Arctic Wolf": "token_buyer",
    "At-Bay": "n/a",
    "Atlassian": "token_buyer",
    "Autodesk": "token_buyer",
    "Axonius": "token_buyer",
    "Bill.com": "token_buyer",
    "Block": "token_buyer",
    "Bolt": "token_buyer",
    "Breadfast": "n/a",
    "Bungie": "n/a",
    "C3.ai": "compute_seller",
    "Careem": "n/a",
    "Cars.com": "token_buyer",
    "Cisco": "infra_seller",
    "Clari": "token_buyer",
    "Cloudflare": "hybrid",
    "Codecademy": "n/a",
    "Coinbase": "token_buyer",
    "Covrzy": "n/a",
    "Crypto.com": "token_buyer",
    "Cyberark": "token_buyer",
    "Dayforce": "n/a",
    "DeepL": "compute_seller",
    "Deliveroo": "n/a",
    "Dell": "infra_seller",
    "Digg": "token_buyer",
    "DraftKings": "token_buyer",
    "Dune": "token_buyer",
    "Enpal": "n/a",
    "Entropy": "n/a",
    "Envato": "token_buyer",
    "Epic Games": "n/a",
    "Epidemic Sound": "token_buyer",
    "Ericsson": "n/a",
    "Esh Group": "n/a",
    "Eventbrite": "token_buyer",
    "Expedia": "token_buyer",
    "Fi.Money": "n/a",
    "Firebolt": "compute_seller",
    "Flipkart": "token_buyer",
    "Foretellix": "infra_seller",
    "FormFactor": "n/a",
    "FranShares": "n/a",
    "Freshworks": "hybrid",
    "Gambling.com Group": "n/a",
    "Gemini": "token_buyer",
    "GeoComply": "token_buyer",
    "GitLab": "token_buyer",
    "Glossier": "n/a",
    "GoCardless": "n/a",
    "GoPro": "n/a",
    "Guesty": "n/a",
    "Hailo": "infra_seller",
    "Huawei": "hybrid",
    "IAC": "n/a",
    "Innovaccer": "token_buyer",
    "Intuit": "token_buyer",
    "InvestCloud": "n/a",
    "Jumia": "token_buyer",
    "Kaseya": "n/a",
    "Kiwi.com": "n/a",
    "Kraken": "token_buyer",
    "LSports": "token_buyer",
    "Life360": "token_buyer",
    "LinkedIn": "token_buyer",
    "Livspace": "token_buyer",
    "Loopio": "n/a",
    "Lucid Motors": "n/a",
    "MARA": "n/a",
    "MRI Software": "token_buyer",
    "MercadoLibre": "token_buyer",
    "MessageBird": "token_buyer",
    "Meta": "vertical_builder",
    "MicroVision": "n/a",
    "Microsoft (Xbox)": "n/a",
    "Microsoft (corporate)": "hybrid",
    "Monte Carlo": "token_buyer",
    "Moon Active": "n/a",
    "Multiverse": "n/a",
    "NeuroPixel.AI": "compute_seller",
    "Ocado": "n/a",
    "One Identity": "n/a",
    "OpenText": "hybrid",
    "Oracle": "compute_seller",
    "Parker": "n/a",
    "PayPal": "token_buyer",
    "Peloton": "n/a",
    "Pendo": "token_buyer",
    "Pentera": "token_buyer",
    "Pepper Pay": "n/a",
    "Pinterest": "token_buyer",
    "Playtika": "token_buyer",
    "Pocket FM": "token_buyer",
    "Polygon": "n/a",
    "Productboard": "token_buyer",
    "Quandoo": "n/a",
    "Quora": "hybrid",
    "Rec Room": "n/a",
    "Remarkable": "n/a",
    "Rewire": "n/a",
    "Robinhood": "token_buyer",
    "Roof Stacks": "n/a",
    "SSense": "n/a",
    "Salesforce": "hybrid",
    "Sama": "infra_seller",
    "Shopify": "token_buyer",
    "Smartsheet": "token_buyer",
    "Snap": "token_buyer",
    "Snowflake": "compute_seller",
    "Sonos": "n/a",
    "Spotify": "hybrid",
    "Staffbase": "token_buyer",
    "StarkWare": "n/a",
    "Stone": "token_buyer",
    "StoreDot": "n/a",
    "SuperOps": "hybrid",
    "Supernal": "n/a",
    "Swyftx": "n/a",
    "Tailwind Labs": "token_buyer",
    "Ticketmaster": "token_buyer",
    "Tipalti": "n/a",
    "TrueCar": "n/a",
    "Truecaller": "token_buyer",
    "UKG": "token_buyer",
    "Upwork": "token_buyer",
    "Verint Systems": "token_buyer",
    "Vimeo": "n/a",
    "Welltech": "n/a",
    "WiseTech": "token_buyer",
    "Wix": "token_buyer",
    "Workday": "token_buyer",
    "Yupp": "token_buyer",
    "Zap Africa": "token_buyer",
    "Zendesk": "token_buyer",
    "Zillow": "n/a",
    "Zipcar": "n/a",
    "ZoomInfo": "token_buyer",
    "Zupee": "n/a",
    "eBay": "token_buyer",
    "eToro": "n/a",
    "reAlpha": "token_buyer",
}


# ---------------------------------------------------------------------------
# Manual overrides: companies + dates where we have deep research data
# ---------------------------------------------------------------------------
# Keys are (company, date) -> dict of fields to override the rule-based output
MANUAL = {
    # ---------------------- Meta (4 rounds) ----------------------
    ("Meta", "2026-01-13"): {
        "reason_primary": "strategic_pivot",
        "ai_link": "ai_pivot_market",
        "narrative_source": "ceo_memo",
        "profiles_cut": ["VR_game_studios_shutdown", "VR_engine_engineers", "game_producers", "Twisted_Pixel", "Sanzaru", "Armature", "Oculus_Studios_Central_Technology"],
        "profiles_hired": ["AR_hardware_engineers", "smart_glasses", "CV_optics"],
        "hire_overcorrection": True,
        "reassignment_observed": False,
    },
    ("Meta", "2026-03-25"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding",
        "narrative_source": "news_with_quote",
        "profiles_cut": ["Reality_Labs", "Facebook_social", "recruiting_TA", "ad_sales", "global_operations"],
        "profiles_hired": ["AI_infra", "AI_monetization"],
        "hire_overcorrection": True,
        "reassignment_observed": False,
    },
    ("Meta", "2026-04-02"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding",
        "narrative_source": "press_release_sec",  # CA EDD WARN filings (Burlingame 124 / Sunnyvale 74) — see meta-profile-breakdown.md Round 3
        "profiles_cut": ["Bay_Area_ICs_RL_AR_infra"],
        "profiles_hired": [],
        "hire_overcorrection": True,
        "reassignment_observed": False,
    },
    ("Meta", "2026-05-20"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding",
        "narrative_source": "ceo_memo",
        "profiles_cut": ["middle_management", "core_engineering_non_AI", "product_design", "cybersecurity", "content_moderation", "Reality_Labs", "Facebook_social", "recruiting", "FAIR_researchers"],
        "profiles_hired": ["AI_researchers_foundation_models", "ML_engineers", "AI_infra", "AI_monetization", "AR_hardware", "Superintelligence_Labs", "TBD_Lab"],
        "hire_overcorrection": True,
        "reassignment_observed": True,  # ~7,000 redeployed to 4 new AI orgs
    },
    # ---------------------- Oracle ----------------------
    ("Oracle", "2026-03-31"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding",
        "narrative_source": "news_with_quote",
        "profiles_cut": ["Oracle_Health_Cerner", "SVOS_support", "NetSuite_devs", "OCI_legacy_sales", "customer_support", "QA_testers", "documentation", "middle_management", "India_dev_centers"],
        "profiles_hired": ["data_center_technicians_no_degree", "AI_infra_engineers", "MLOps", "OCI_AI_sales", "Stargate_buildout"],
        "hire_overcorrection": False,
        "reassignment_observed": False,
    },
    # ---------------------- PayPal ----------------------
    ("PayPal", "2026-05-05"): {
        "reason_primary": "new_ceo_turnaround",
        "ai_link": "ai_denied_but_adjacent",  # framed as cost + AI-native; some functions explicitly AI
        "narrative_source": "ceo_memo",
        "profiles_cut": ["engineering", "support_ops", "customer_service", "risk_management", "middle_management"],
        "profiles_hired": ["AI_Transformation_team", "digital_banking_exec", "AI_fluent_engineers"],
        "hire_overcorrection": False,
        "reassignment_observed": False,
    },
    # ---------------------- Amazon ----------------------
    ("Amazon", "2026-01-28"): {
        "reason_primary": "restructuring_vague",
        # NOTE (2026-07-10 adjudication): the earlier "Claude Sonnet replacing dozens of
        # mid-engineers cited" note was traced to a satirical blog post + an unrelated Reddit
        # anecdote — no first-party Amazon origin. Galetti memo is AI-silent; Amazon spokesperson
        # to AP (~Feb 1): AI was "not the reason behind the vast majority of these reductions".
        # ai_link is therefore set by the ADJUDICATION layer below (ai_narrative_only/company_denied).
        "narrative_source": "ceo_memo",
        "profiles_cut": ["SDE_II", "middle_management_L6_L7", "PXT_HR_recruiting", "AWS_TAM_solutions_architects", "Alexa_AI_legacy", "Prime_Video_platform_eng", "Amazon_Pharmacy", "TPMs"],
        "profiles_hired": ["AGI_team_Nova", "Trainium_chip_team", "Bedrock_agents", "Frontier_AI_Robotics", "Project_Rainier_data_center"],
        "hire_overcorrection": True,  # SEC audit 2026-06-18: TRUE for corporate/tech segment (see audit notes below). The Workforce.ai -1.3% SWE figure was the blended view.
        "reassignment_observed": False,
    },
    # ---------------------- Intuit ----------------------
    ("Intuit", "2026-05-20"): {
        "reason_primary": "restructuring_vague",
        "ai_link": "ai_denied_but_adjacent",  # CEO explicitly denied AI
        "narrative_source": "ceo_memo",
        "profiles_cut": ["engineering_CA", "customer_support", "marketing", "admin", "satellite_offices_Reno_WoodlandHills", "middle_management"],
        "profiles_hired": ["AI_ML_engineers_Mountain_View", "Anthropic_OpenAI_integration_roles"],
        "hire_overcorrection": True,  # SEC audit 2026-06-18: FY20→FY22 +51.9% organic ex-Mailchimp (see audit notes below)
        "reassignment_observed": False,
    },
    # ---------------------- Snap ----------------------
    ("Snap", "2026-04-15"): {
        "reason_primary": "ai_substitution_claim",
        "ai_link": "direct_substitution",  # 65% of code AI-generated cited
        "narrative_source": "ceo_memo",
        "profiles_cut": ["Snapchat_core_engineering", "product", "operations", "ad_partnerships", "trust_safety"],
        "profiles_hired": ["Specs_Inc_AR_engineers", "Lens_Studio", "Qualcomm_collab_SoC", "camera_AI_ranking_ML"],
        "hire_overcorrection": True,  # Snap was +15% then 16% cut
        "reassignment_observed": False,
    },
    # ------------- hire_overcorrection signals from Pragmatic Engineer / Workforce.ai -------------
    # 2-yr SWE headcount growth before the cut: Atlassian +23%, Shopify +36%, Stripe +29%, Spotify +6%
    ("Atlassian", "2026-03-11"): {
        "reason_primary": "strategic_pivot",  # CEO "pivoting toward AI and reorganizing for the AI era"
        "ai_link": "ai_pivot_market",
        "narrative_source": "news_with_quote",
        "hire_overcorrection": True,
    },
    ("Shopify", "2026-05-04"): {
        "hire_overcorrection": True,
    },
    # Cloudflare: from "internal AI usage grew 600%" - clearer substitution than capex
    ("Cloudflare", "2026-05-07"): {
        "reason_primary": "ai_substitution_claim",
        "ai_link": "direct_substitution",
        "narrative_source": "ceo_memo",
        "hire_overcorrection": True,  # see SEC audit pass below
    },
    # Wix: "rising AI compute costs... roles becoming redundant in the AI era"
    ("Wix", "2026-05-25"): {
        "reason_primary": "cost_cutting",
        "ai_link": "ai_denied_but_adjacent",
        "narrative_source": "news_with_quote",
        "hire_overcorrection": True,  # see SEC audit pass below
    },
    # ------------------------------------------------------------------
    # SEC 10-K audit pass (2026-06-18): expanded hire_overcorrection coverage
    # ------------------------------------------------------------------
    # Original `hire_overcorrection` flag relied on Workforce.ai data (11 companies).
    # Audited 8 large 2026 cuts (>=500 people OR >=10% pct, SaaS/digital) via SEC
    # 10-K / 20-F headcount disclosures. Threshold: >=15% growth in any 2-yr window.
    # Verdicts: 7/8 TRUE (Block, Cloudflare, Wix, Coinbase, Bill.com, Pinterest, ZoomInfo).
    # WiseTech is FALSE — its growth was M&A-driven (E2open acquisition).
    # Sources: SEC EDGAR filings of each company. See methodology.md §1 Phase 8.
    ("Block", "2026-02-26"): {
        # FY20: 5,477 → FY22: 12,428 (+127%); +101% organic ex Afterpay (~1,400 hc)
        # FY24-25 already cutting 21% before 4k cut. Returns to ~FY20+13%.
        "hire_overcorrection": True,
    },
    ("Pinterest", "2026-01-27"): {
        # FY20: 2,545 → FY22: 3,987 (+57%) AND FY23: 4,014 → FY25: 5,265 (+31%).
        # Cut corrects the FY24-25 AI-ads/GenAI rebuild wave, not original COVID bulge.
        "hire_overcorrection": True,
    },
    ("Coinbase", "2026-05-05"): {
        # Pandemic 2021 already corrected (Jun-22 -18%, Jan-23 -25%). 2026 cut
        # corrects fresh FY23→FY25 rebuild: 3,416 → 4,951 (+45% in 2yr).
        "hire_overcorrection": True,
    },
    ("Bill.com", "2026-05-07"): {
        # FY20: 618 → FY22 organic: ~1,549 (+151% organic ex Divvy/Invoice2go).
        # 30% cut returns to ~pre-acquisition organic levels.
        "hire_overcorrection": True,
    },
    ("ZoomInfo", "2026-05-11"): {  # date corrected 2026-07-10 per the 8-K (was 05-10)
        # IPO 2020 with 1,747 FTEs → FY22 peak 3,540 (+102% raw, +85% organic
        # ex Chorus.ai + RingLead). 600 cut on top of -332 in FY24-25.
        "hire_overcorrection": True,
    },
    # WiseTech (2026-02-24): FALSE — growth M&A-driven (Envase/Blume/Trinium/E2open).
    # FY21 was -12% organic. No flag.
    #
    # ------------------------------------------------------------------
    # Second SEC audit pass (2026-06-18): "the big 4" Oracle/Amazon/PayPal/Intuit
    # ------------------------------------------------------------------
    # Audited the four big cuts originally framed in the newsletter as
    # "strategic reset, NOT overhired organically". Verdicts:
    #
    # ORACLE (2026-03-31): FALSE. Best 2-yr organic window FY20→FY22 = +5.9%.
    # The +21k FY22→FY23 jump was entirely Cerner M&A ($28.3B, ~25k hc).
    # Ex-Cerner organic flat-to-down. Cut is Cerner unwind + OCI/AI margin reset.
    # Source: Oracle 10-K FY25 (Human Capital, ~162k FTE May 31, 2025).
    #
    # PAYPAL (2026-05-05): FALSE. FY21 peak 30.9k → FY25 23.8k (-23% absorbed
    # via Feb-2023 + Jan-2024 cuts). FY25 sits 10% BELOW FY20 pre-COVID baseline.
    # The COVID overhang was already cleared pre-2026.
    # Source: PayPal 10-K FY25.
    #
    # AMAZON (2026-01-28): TRUE for corporate/tech segment.
    # Corporate ~150-180k (FY19) → ~415k peak (FY22) ≈ +130-175%. Jassy's own
    # Q3 2021 disclosure: 55k new tech/corporate hires in a single batch.
    # Cumulative ~60k+ corporate eliminations against ~415k peak = ~15% unwound.
    # CAVEAT: Amazon does NOT disclose corporate-vs-fulfillment split in 10-Ks.
    # ~415k peak comes from press leaks (The Information, Reuters via earnings
    # calls), not audited disclosure. Direction high confidence, magnitude medium.
    # Newsletter previously said "Amazon not organically overhired" — that was
    # wrong for the corporate segment. Defensible only if you blend in warehouse.
    # (Flag merged into the main ("Amazon", "2026-01-28") entry above — the
    # duplicate dict key that used to sit here silently clobbered that entry's
    # full override, wiping its ai_link/narrative_source/profiles.)
    # INTUIT (2026-05-20): TRUE. FY20 10.6k → FY22 organic ex-Mailchimp 16.1k
    # = +51.9% organic in 2 yrs. Pre-Mailchimp pure organic FY20→FY21 = +27.4%
    # in a single year. Plateau FY23-FY25 (+5.6%, +3.5%, -3.4%) — classic
    # overhiring → plateau → correction pattern. Cut returns to ~FY22 organic.
    # Source: Intuit 10-K FY20 + FY22 (Mailchimp ~1,200 hc, closed Nov 2021).
    # (Flag merged into the main ("Intuit", "2026-05-20") entry above — the
    # duplicate dict key that used to sit here silently clobbered that entry's
    # full override, mislabeling Intuit as shutdown_bankruptcy/unrelated.)
    # ------------------------------------------------------------------
    # Third SEC audit pass (2026-06-18): Tier 1 (8 remaining large cuts)
    # ------------------------------------------------------------------
    # Audited Dell, Cisco, ASML, Autodesk, Stone, Workday, Freshworks, C3.ai.
    # TRUE (3): Workday, Freshworks, C3.ai. FALSE (5): Dell, Cisco, ASML,
    # Autodesk, Stone — all mature businesses or pre-absorbed overhire.
    # Methodological note: the +15% / 2-yr threshold was designed for SaaS
    # startups; mature hardware (Dell, Cisco, ASML) and disciplined LATAM
    # fintech (Stone) require qualitative judgment, not raw math.
    #
    # WORKDAY (2026-02-04): TRUE (qualified). FY21 12.5k → FY25 organic
    # 20.1k = +61% in 4 yrs. Post Feb-2025 cut (-1,750), still +50% above
    # FY21 baseline. Feb 2026 cut (-400) is follow-on right-sizing.
    # Caveat: revenue grew +95% same window, so headcount lagged revenue —
    # not pure overhire, but still elevated vs SaaS maturity benchmarks.
    ("Workday", "2026-02-04"): {
        "hire_overcorrection": True,
    },
    # FRESHWORKS (2026-05-05): TRUE. Textbook pandemic-IPO pattern.
    # FY20 3,585 → FY22 5,400 = +50% in 2 yrs. Three cuts (2023 attrition,
    # Nov 2024 -660, May 2026 -500) now at ~3,900 — BELOW the IPO baseline
    # ex-Device42. AI-productivity framing is post-hoc rationalization.
    # (Flag lives in the ("Freshworks", "2026-05-05") entry further below,
    # together with its ai_link override — avoid duplicate dict keys.)
    # C3.AI (2026-02-25): TRUE — but it's an AI-hype overhire, not COVID.
    # FY21 baseline 574 → FY25 peak 1,181 = +106% in 4 yrs. FY24 was flat
    # then FY25 re-accelerated +32.6% chasing GenAI demand. Q3 FY26 revenue
    # collapsed ($53M vs $76M consensus). New CEO: "cost structure was
    # simply too high." Feb 2026 cut (-312) ~equals FY25 net adds (+290) —
    # they literally fired everyone hired in their last growth year.
    ("C3.ai", "2026-02-25"): {
        "hire_overcorrection": True,
    },
    # FALSE verdicts kept here for documentation (no override needed):
    # - Dell (2026-03-16): FY20 organic 134k → FY22 organic 133k = -0.7%.
    #   Dell actually CONTRACTED during COVID (FY21 124k). Mature hardware.
    # - Cisco (2026-05-13): FY20 → FY22 organic +7.5%. Mature networking.
    # - ASML (2026-01-28): FY20 → FY22 payroll +35.7% but semi-cycle, not
    #   SaaS. FY24 → FY25 already +1.7% (self-decelerated). 1,700 cut = 3.9%.
    # - Autodesk (2026-01-22): FY21 → FY25 organic +28% (linear ~7% CAGR).
    #   Revenue grew faster (+62%) than headcount.
    # - Stone (2026-03-13): organic ex-Linx -11% vs peak. Already absorbed.
    # Sama: lost Meta contract (data labeling). The driver is contractual, not AI-denial.
    # Meta brought labeling in-house; Sama is the supply side that got disrupted.
    # Was wrongly flagged ai_denied_but_adjacent because the reason text mentions AI work.
    ("Sama", "2026-04-16"): {
        "ai_link": "unrelated",
    },
    # ---- Audit pass (2026-06-04): rule-based `if "ai" in r` fallthrough caught
    # many false positives via substrings (asml, det**ai**l, etc.). Fix below by
    # case. See bucket review notes in conversation.
    # 22 cases that have no real AI framing in the reason → unrelated:
    ("ASML",         "2026-01-28"): {"ai_link": "unrelated"},  # "ml " in "asml " — substring bug
    ("Flipkart",     "2026-03-06"): {"ai_link": "unrelated"},  # "regular annual performance review"
    ("Supernal",     "2026-03-04"): {"ai_link": "unrelated"},  # eVTOL strategic pivot, no AI
    ("Pocket FM",    "2026-05-06"): {"ai_link": "unrelated"},  # performance reviews
    ("Enpal",        "2026-03-27"): {"ai_link": "unrelated"},  # CS dept dissolved, no AI cited
    ("TrueCar",      "2026-02-24"): {"ai_link": "unrelated"},  # took private, refocus on profitability
    ("Expedia",      "2026-02-01"): {"ai_link": "unrelated"},  # "reducing organizational layers"
    ("Huawei",       "2026-02-15"): {"ai_link": "unrelated"},  # generic org restructure
    ("Glossier",     "2026-02-11"): {"ai_link": "unrelated"},  # new CEO reshape, brand
    ("MicroVision",  "2026-03-03"): {"ai_link": "unrelated"},  # Redmond→Orlando consolidation
    ("One Identity", "2026-05-11"): {"ai_link": "unrelated"},  # closing German office (geographic)
    ("Axonius",      "2026-02-15"): {"ai_link": "unrelated"},  # IPO prep, no AI
    ("Loopio",       "2026-03-13"): {"ai_link": "unrelated"},  # market conditions, no AI
    ("At-Bay",       "2026-03-04"): {"ai_link": "unrelated"},  # path to profit, no AI
    ("Spotify",      "2026-03-23"): {"ai_link": "unrelated"},  # podcast group reorg
    ("Careem",       "2026-05-05"): {"ai_link": "unrelated"},  # inflation, demand decline, Pakistan exit
    ("Quora",        "2026-04-16"): {"ai_link": "unrelated"},  # Poe separating from Quora financially
    ("OpenText",     "2026-03-24"): {"ai_link": "unrelated"},  # "regular evaluation"
    ("Lucid Motors", "2026-02-20"): {"ai_link": "unrelated"},  # EV profitability push
    ("Codecademy",   "2026-02-19"): {"ai_link": "unrelated"},  # no rationale given
    # Salesforce recode (2026-07-10): vague unannounced restructuring where AI surfaces
    # in the coverage framing — Benioff's own "support ~9,000 → ~5,000 via AI tools"
    # claim is cited, and the cut hit Agentforce/Heroku while Salesforce sells Agentforce.
    # Fits ai_denied_but_adjacent's second clause; was over-corrected to unrelated in the
    # substring-bug audit.
    ("Salesforce",   "2026-02-09"): {"ai_link": "ai_denied_but_adjacent"},
    ("Peloton",      "2026-01-30"): {"ai_link": "unrelated"},  # fitness hardware cost cuts
    ("Vimeo",        "2026-01-21"): {"ai_link": "unrelated"},  # Bending Spoons PE playbook
    ("StoreDot",     "2026-01-13"): {"ai_link": "unrelated"},  # SPAC merger prep, batteries

    # 4 cases that are direct_substitution (CEO openly said AI does the work):
    ("Freshworks",   "2026-05-05"): {"ai_link": "direct_substitution", "hire_overcorrection": True},  # see SEC audit pass + "over half of our code is written by AI"
    ("Upwork",       "2026-05-07"): {"ai_link": "direct_substitution", "hire_overcorrection": True},   # "AI means smaller, differently resourced teams"; 10-K: +57.4% headcount 2020→22
    ("Kraken",       "2026-05-15"): {"ai_link": "direct_substitution", "hire_overcorrection": True},   # AI chatbot handles 80% of customer inquiries; +36.4% Oct'24→May'26 (press-sourced)
    ("Crypto.com",   "2026-03-19"): {"ai_link": "direct_substitution"},  # "roles that do not adapt to AI"

    # 2 cases that are ai_pivot_market (product/market pivot to AI):
    ("Epidemic Sound","2026-04-21"): {"ai_link": "ai_pivot_market"},  # AI-generated music
    ("AI21 Labs",    "2026-05-18"): {"ai_link": "ai_pivot_market"},  # foundation models → agent orchestration

    # 2 more found in second audit (2026-06-04): denied AI but no evidence of AI investment.
    # Epic Games: Fortnite engagement collapse — explicit AI denial, demand collapse driver.
    # Remarkable: AI mentioned as macroeconomic cost pressure (chip shortage), not their investment.
    ("Epic Games",   "2026-03-24"): {"ai_link": "unrelated"},
    ("Remarkable",   "2026-04-22"): {"ai_link": "unrelated"},

    # ------------------------------------------------------------------
    # Data-fix pass (2026-07-10): pin the hand-appended Jun/Jul events so they
    # survive pipeline re-runs, normalize their off-schema label values, and
    # fix the Zupee mislabel.
    # ------------------------------------------------------------------
    # Zupee: rule misfired to shutdown_bankruptcy ("banned" in reason text);
    # it's a partial layoff (~200) driven by India's online-gaming ban — the
    # schema's own canonical `regulatory` example.
    ("Zupee", "2026-01-30"): {"reason_primary": "regulatory"},
    ("GitLab", "2026-06-03"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding",
        "narrative_source": "news_with_quote",
        "hire_overcorrection": True,  # Track-2 audit: +30.7% FY22→24, +21.1% FY24→26 (10-K)
    },
    ("Robinhood", "2026-06-16"): {
        "reason_primary": "ai_substitution_claim",
        "ai_link": "direct_substitution",  # normalized from off-schema "substitution_claim"
        "narrative_source": "ceo_memo",
        # Headcount 2,300 (Dec 2024) → ~2,900 (2025) = +26% in the year before the 10% cut.
        "hire_overcorrection": True,
    },
    ("Bungie", "2026-06-25"): {
        "reason_primary": "strategic_pivot",
        "ai_link": "unrelated",
        "narrative_source": "news_inferred",  # normalized from off-schema "news_confirmed"
    },
    ("Microsoft (Xbox)", "2026-07-06"): {
        "reason_primary": "strategic_pivot",
        "ai_link": "unrelated",
        "narrative_source": "news_with_quote",  # Xbox CEO Asha Sharma: "our business today is not healthy"
    },
    ("Microsoft (corporate)", "2026-07-06"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding",
        "narrative_source": "press_release_sec",
    },

    # ------------------------------------------------------------------
    # Track-2 over-hiring audit extension (2026-07-10): stated-AI companies
    # the SEC-only audit never covered. Same >=15%-in-any-2yr-window criterion;
    # filings where public, LinkedIn/press headcount series where not.
    # (Upwork/Kraken/GitLab/Robinhood flags live in their entries above.)
    # ------------------------------------------------------------------
    ("Livspace", "2026-02-20"): {"hire_overcorrection": True},   # +112.8% May'20→Mar'22
    ("Cisco", "2026-05-13"): {"hire_overcorrection": False},     # +8.5% raw, flat organic ex-Splunk
    ("WiseTech", "2026-02-24"): {"hire_overcorrection": False},  # organic; raw +75% is pure M&A stacking (E2open et al.)
    ("Playtika", "2026-01-14"): {"hire_overcorrection": False},  # shrinking every year since 2020
    ("Zendesk", "2026-03-24"): {"hire_overcorrection": False},   # +8.3% best window (Revelio/LinkedIn-derived)
}

# ---------------------------------------------------------------------------
# Axis 5 — ai_link_basis: WHO established the AI connection (added 2026-07-10)
# ---------------------------------------------------------------------------
# The old ai_link axis conflated the mechanism with who claims it. This axis
# separates them so the labels are honest about what is known vs inferred:
#   company_stated  — the company itself made/supported the ai_link reading
#                     (memo, filing, earnings call, named exec quote)
#   company_denied  — the company explicitly denied AI as the cause
#   analyst_inferred— this dataset's analyst inferred the link (none currently:
#                     the two events that lived on inference — Amazon, Oracle —
#                     resolved to company_denied / company_stated on adjudication)
#   press_inferred  — press made the connection; company said nothing
#   unknown         — source not accessible
#
# ai_link vocabulary migration (same pass): mechanism axis no longer carries
# denial/pivot framing — that information lives in ai_link_basis now.
#   ai_denied_but_adjacent -> ai_narrative_only (+ basis=company_denied)
#   ai_pivot_market        -> ai_narrative_only
# Final ai_link vocabulary: direct_substitution / capex_funding /
# ai_narrative_only / unrelated (/ unknown, reserved).
AI_LINK_MIGRATION = {
    "ai_denied_but_adjacent": "ai_narrative_only",
    "ai_pivot_market": "ai_narrative_only",
}

def default_ai_link_basis(ai_link, narrative):
    """Default basis for non-adjudicated events, from the evidence axis.
    company_denied is NEVER defaulted — the referee pass (2026-07-10) found the
    legacy rule (ai_denied_but_adjacent -> company_denied) stamped 15 records
    with no denial evidence (some even AFFIRM AI, e.g. MRI Software). Verified
    denials are assigned only via ADJUDICATION (currently Amazon, Intuit,
    Autodesk). Known failure mode that remains: ceo_memo does not imply the
    memo makes the AI claim (Amazon, Meta-Jan had AI-silent memos) — spot-check
    small ceo_memo events whose reason text lacks an AI verb."""
    if narrative in ("ceo_memo", "press_release_sec", "news_with_quote"):
        return "company_stated"
    if narrative == "news_inferred":
        return "press_inferred"
    return "unknown"

# ---------------------------------------------------------------------------
# ADJUDICATION pass (2026-07-10): 25 contested events (>=500 heads or Amazon),
# covering 94.9% of AI-linked headcount, re-verdicted against PRIMARY sources
# (memos, SEC/ASX filings, earnings-call transcripts). Applied AFTER MANUAL —
# this layer is authoritative for the fields it sets. One-line decisive
# evidence + source per entry. Rubric: M1 = AI does the work, M2 = AI gets
# the money, M3 = AI in the story only, M4 = not AI.
# ---------------------------------------------------------------------------
ADJUDICATION = {
    # M3/company_denied. Galetti memo 100% AI-silent; spokesperson to AP (~Feb 1):
    # AI "not the reason behind the vast majority of these reductions".
    # aboutamazon.com/news/company-news/amazon-layoffs-corporate-jan-2026
    ("Amazon", "2026-01-28"): {
        "ai_link": "ai_narrative_only", "ai_link_basis": "company_denied",
    },
    # M1/company_stated (CAVEAT: year-level, not event-specific — Oracle declined
    # all event comment). FY26 10-K: AI deployment "resulted... in reductions to
    # our workforce" in the FY where this cut was ~all the reduction (162k->141k).
    # The viral Catz "generational reallocation of capital" / Ellison "choosing
    # the chips" capex quotes could NOT be traced to any real source (likely
    # content-mill fabrications) — the M2 capex story is therefore unsupported.
    # sec.gov orcl-20260531.htm
    ("Oracle", "2026-03-31"): {
        "reason_primary": "ai_substitution_claim",
        "ai_link": "direct_substitution", "ai_link_basis": "company_stated",
        "narrative_source": "press_release_sec",
    },
    # M4/company_stated. 10-K Human Capital cites only "disciplined cost
    # management... employee reorganizations" — zero AI. AI-server link was
    # press inference. Dell FY26 10-K (dell-20260130.htm)
    ("Dell", "2026-03-16"): {
        "reason_primary": "cost_cutting",
        "ai_link": "unrelated", "ai_link_basis": "company_stated",
    },
    # M4/company_stated. Full statement: "reinvest across our business and align
    # our structure with strategic priorities" — no AI anywhere. retaildive/cnbc
    ("eBay", "2026-02-26"): {
        "ai_link": "unrelated", "ai_link_basis": "company_stated",
    },
    # M4/company_stated. Shapero memo + spokesperson: zero AI language ("regular
    # business planning"); even the "not AI" line was an anonymous source, not a
    # company denial. reuters.com 2026-05-13
    ("LinkedIn", "2026-05-13"): {
        "ai_link": "unrelated", "ai_link_basis": "company_stated",
    },
    # M4/company_stated. Bosworth memo has zero AI language: VR to be "leaner,
    # flatter... sustainability"; "AI wearables" was press framing. Bloomberg/Yahoo
    ("Meta", "2026-01-13"): {
        "ai_link": "unrelated", "ai_link_basis": "company_stated",
    },
    # M3/press_inferred. No first-party AI statement exists for this round; the
    # "free up resources for AI" quote belongs to the 04-23 Gale memo (05-20 event).
    ("Meta", "2026-03-25"): {
        "reason_primary": "restructuring_vague",
        "ai_link": "ai_narrative_only", "ai_link_basis": "press_inferred",
        "narrative_source": "news_inferred",
    },
    # Follows the 03-25 downgrade: WARN filings are AI-silent; this round is the
    # formal IC processing of that wave.
    ("Meta", "2026-04-02"): {
        "reason_primary": "restructuring_vague",
        "ai_link": "ai_narrative_only", "ai_link_basis": "press_inferred",
    },
    # M2/company_stated. CFO Susan Li, Q1 call 4/29: leaner model "helping to
    # offset the substantial investments we are making" ($125-145B AI capex,
    # same call); CPO Gale memo 4/23 same language. fool.com Meta Q1-2026
    ("Meta", "2026-05-20"): {
        "ai_link": "capex_funding", "ai_link_basis": "company_stated",
    },
    # M1/company_stated — no denial ever existed. CEO Lores, Q1 call: "With AI,
    # we believe we can both reduce cost and improve the experience"; AI
    # transformation "function by function, process by process". fool.com
    ("PayPal", "2026-05-05"): {
        "ai_link": "direct_substitution", "ai_link_basis": "company_stated",
    },
    # M3/company_denied. Goodarzi on CNBC: "None of it had to do with AI"; no
    # first-party link from savings to the same-day Anthropic/OpenAI deals.
    ("Intuit", "2026-05-20"): {
        "ai_link": "ai_narrative_only", "ai_link_basis": "company_denied",
    },
    # M3/company_denied. Anagnost email (SEC-filed): changes "not driven by...
    # an effort to replace people with AI". adsknews.autodesk.com 012226
    ("Autodesk", "2026-01-22"): {
        "ai_link": "ai_narrative_only", "ai_link_basis": "company_denied",
    },
    # M1/company_stated — no denial ever existed. Abrahami: "fewer layers...
    # also means a smaller number of people" (FX a stated co-driver). cnbc 05-28
    ("Wix", "2026-05-25"): {
        "reason_primary": "ai_substitution_claim",
        "ai_link": "direct_substitution", "ai_link_basis": "company_stated",
    },
    # M1/company_stated — no denial ever existed. Antokol letter (8-K exhibit):
    # "streamlined teams powered by AI and automation... do more with less".
    ("Playtika", "2026-01-14"): {
        "ai_link": "direct_substitution", "ai_link_basis": "company_stated",
        "narrative_source": "press_release_sec",
    },
    # M3/company_stated. Blog invokes "the agentic AI era" + 600% internal usage
    # but never states AI performs the cut roles' work, and explicitly says
    # "not a cost-cutting exercise" (ruling out M2 too). blog.cloudflare.com
    ("Cloudflare", "2026-05-07"): {
        "reason_primary": "restructuring_vague",
        "ai_link": "ai_narrative_only", "ai_link_basis": "company_stated",
    },
    # M2/company_stated. Cannon-Brookes memo: "We are doing this to self-fund
    # further investment in AI and enterprise sales" (+M1 ack: AI changes "the
    # number of roles required in certain areas. It does.") atlassian.com/blog
    ("Atlassian", "2026-03-11"): {
        "reason_primary": "ai_capex_reallocation",
        "ai_link": "capex_funding", "ai_link_basis": "company_stated",
    },
    # M3/company_stated (weak: PR spokesperson only; no Morgan quote exists).
    # "market shifts — including changes in technology driven by AI"; "AI-first
    # company" is brand copy, not layoff language. cbs12/hrexecutive
    ("UKG", "2026-04-15"): {
        "ai_link": "ai_narrative_only", "ai_link_basis": "company_stated",
    },
    # M1(+M2)/company_stated, M1 dominant. Schuck, Q1 call: "we do not need as
    # many front-end developers" thanks to coding agents (8-K memo AI-silent).
    ("ZoomInfo", "2026-05-11"): {
        "reason_primary": "ai_substitution_claim",
        "ai_link": "direct_substitution", "ai_link_basis": "company_stated",
        "narrative_source": "news_with_quote",
    },
    # M1/company_stated. Armstrong (own X post): "rebuilding Coinbase as an
    # intelligence, with humans around the edge" (crypto downturn co-driver).
    ("Coinbase", "2026-05-05"): {
        "ai_link_basis": "company_stated", "narrative_source": "news_with_quote",
    },
    # M2/company_stated. 8-K Item 2.05: "reallocating resources to AI-focused
    # roles and teams". sec.gov pins-20260122.htm
    ("Pinterest", "2026-01-27"): {
        "ai_link_basis": "company_stated", "narrative_source": "press_release_sec",
    },
    # M1/company_stated (core claim first-party via spokesperson; per-function
    # detail is press elaboration). inc42/entrackr
    ("Livspace", "2026-02-20"): {
        "ai_link_basis": "company_stated", "narrative_source": "news_with_quote",
    },
    # M1/company_stated. Dorsey, SEC 8-K shareholder letter: teams "using AI to
    # automate more work". sec.gov d108590dex991.htm
    ("Block", "2026-02-26"): {
        "ai_link_basis": "company_stated", "narrative_source": "press_release_sec",
    },
    # M1/company_stated. ASX release + CEO Appoo: roles "where we have seen AI
    # dramatically improve throughput". wisetechglobal.com wtc-1h26-asx
    ("WiseTech", "2026-02-24"): {
        "ai_link_basis": "company_stated", "narrative_source": "press_release_sec",
    },
    # M2/company_stated. Robbins company blog: investments in "silicon, optics,
    # security, and... AI"; CFO: "not a savings-driven restructure".
    ("Cisco", "2026-05-13"): {
        "ai_link_basis": "company_stated", "narrative_source": "press_release_sec",
    },
    # M1/company_stated. Spiegel memo: AI "enable[s] our teams to reduce
    # repetitive work... small squads leveraging AI tools". newsroom.snap.com
    ("Snap", "2026-04-15"): {
        "ai_link_basis": "company_stated",
    },
    # M1/company_stated. Woodside: "Over half of our code is written by AI".
    ("Freshworks", "2026-05-05"): {
        "ai_link_basis": "company_stated",
    },

    # --- Cross-check corrections (2026-07-10, external-evidence pass) ---
    # Tenev's memo pointedly avoided the word "AI" ("frontier technologies");
    # the AI attribution came from press interpretation (TechCrunch et al.).
    ("Robinhood", "2026-06-16"): {
        "ai_link_basis": "press_inferred",
    },
    # "AI broke the product", not labor substitution: CEO Mezzell said AI agents
    # and bot spam overwhelmed Digg's voting model, forcing retool + app shutdown.
    ("Digg", "2026-03-13"): {
        "reason_primary": "strategic_pivot",
        "ai_link": "ai_narrative_only", "ai_link_basis": "company_stated",
    },
    # Event has NO external footprint (no press, no WARN, absent from trackers;
    # sole source "Internal memo") — basis unknown, reason text carries the flag.
    ("Zendesk", "2026-03-24"): {
        "ai_link_basis": "unknown",
    },

    # --- Referee-pass corrections (2026-07-10, blind re-inspection) ---
    # Clearest substitution text in the dataset ("workers reported training the
    # AI that replaced them") was sitting under restructuring_vague.
    ("MercadoLibre", "2026-01-12"): {
        "reason_primary": "ai_substitution_claim",
    },
    # Robotics-unit cut: reason text says "routine organizational reviews";
    # the substitution reading is press framing (basis already press_inferred).
    ("Amazon", "2026-03-04"): {
        "reason_primary": "restructuring_vague",
    },
}

# ---------------------------------------------------------------------------
# External cross-check columns (2026-07-10): three verdicts per stated-AI event,
# from the three-track external evidence pass (12 sub-agent research batches).
#   revenue_health   — last reported quarter BEFORE the layoff:
#                      strength (growing + profitable) / mixed / weakness / unknown
#   backfill_verdict — hiring behavior post-cut: ai_only / frozen / rehiring_same /
#                      offshore_swap / mixed / unknown  (null for capex events —
#                      backfill doesn't test a capex claim)
#   story_integrity  — the combined call: holds / cracked / busted / unknown.
#                      "cracked" = at least one material fact contradicts the
#                      clean AI narrative (inflated headline number, same-day
#                      guidance cut, M&A-synergy cuts rebranded, documented rehires).
# Sparse: only the adjudicated company-stated AI events carry values.
# ---------------------------------------------------------------------------
CROSS_CHECK = {
    ("Oracle", "2026-03-31"):     {"revenue_health": "strength", "backfill_verdict": "ai_only",       "story_integrity": "cracked"},  # 30k headline ~43% above audited 10-K net 21k
    ("Meta", "2026-05-20"):       {"revenue_health": "strength", "backfill_verdict": None,            "story_integrity": "holds"},    # 7k redeployed; capex raised — money goes where the story says
    ("PayPal", "2026-05-05"):     {"revenue_health": "mixed",    "backfill_verdict": "unknown",       "story_integrity": "cracked"},  # same-day weak GAAP + EPS guided down; cuts phased to 2028
    ("Block", "2026-02-26"):      {"revenue_health": "strength", "backfill_verdict": "ai_only",       "story_integrity": "cracked"},  # >=4 named rehires into same roles; non-AI reqs during stated freeze
    ("Cisco", "2026-05-13"):      {"revenue_health": "strength", "backfill_verdict": None,            "story_integrity": "holds"},    # record quarter; AI order book matches claim
    ("WiseTech", "2026-02-24"):   {"revenue_health": "mixed",    "backfill_verdict": "frozen",        "story_integrity": "cracked"},  # up to half the cut is E2open M&A synergy in AI clothing
    ("Atlassian", "2026-03-11"):  {"revenue_health": "mixed",    "backfill_verdict": None,            "story_integrity": "cracked"},  # over-hirer, chronic GAAP losses, no verifiable AI-capex commitment
    ("Livspace", "2026-02-20"):   {"revenue_health": "strength", "backfill_verdict": "rehiring_same", "story_integrity": "busted"},   # 138 live listings in the exact cut role families
    ("Snap", "2026-04-15"):       {"revenue_health": "strength", "backfill_verdict": "mixed",         "story_integrity": "cracked"},  # 250+ broad reqs = backfill, not substitution
    ("Wix", "2026-05-25"):        {"revenue_health": "mixed",    "backfill_verdict": "ai_only",       "story_integrity": "holds"},    # weak holds; co-stated FX driver honestly
    ("Pinterest", "2026-01-27"):  {"revenue_health": "strength", "backfill_verdict": None,            "story_integrity": "holds"},
    ("Coinbase", "2026-05-05"):   {"revenue_health": "mixed",    "backfill_verdict": "frozen",        "story_integrity": "holds"},    # weak holds; co-stated crypto downturn
    ("ZoomInfo", "2026-05-11"):   {"revenue_health": "weakness", "backfill_verdict": "offshore_swap", "story_integrity": "busted"},   # own 8-K: Israel R&D closed, roles reallocated incl. India; guidance cut to ~1%
    ("Playtika", "2026-01-14"):   {"revenue_health": "mixed",    "backfill_verdict": "offshore_swap", "story_integrity": "cracked"},  # 6th round of secular decline; Israel->Bucharest (thin)
    ("Freshworks", "2026-05-05"): {"revenue_health": "strength", "backfill_verdict": "rehiring_same", "story_integrity": "busted"},   # Chennai support trainee req on own ATS ~7 weeks post-cut
    ("GitLab", "2026-06-03"):     {"revenue_health": "mixed",    "backfill_verdict": None,            "story_integrity": "cracked"},  # cut 14% a day after raising guidance; narrative flip May->June
    ("Robinhood", "2026-06-16"):  {"revenue_health": "strength", "backfill_verdict": "rehiring_same", "story_integrity": "busted"},   # CX reqs in layoff-hit hub cities, one posted layoff day
    ("C3.ai", "2026-02-25"):      {"revenue_health": "weakness", "backfill_verdict": "frozen",        "story_integrity": "cracked"},  # distress cut with AI garnish ("burning too much money")
    ("Upwork", "2026-05-07"):     {"revenue_health": "mixed",    "backfill_verdict": "ai_only",       "story_integrity": "cracked"},  # same-day ~9% guidance cut on +1% growth
    ("Kraken", "2026-05-15"):     {"revenue_health": "mixed",    "backfill_verdict": "ai_only",       "story_integrity": "cracked"},  # Q1 EBITDA -90% disclosed 3 days post-layoff; IPO frozen
    ("MercadoLibre", "2026-01-12"): {"revenue_health": "strength", "backfill_verdict": "ai_only",     "story_integrity": "holds"},    # narrow honest claim while net-adding ~42k jobs
    ("Zendesk", "2026-03-24"):    {"revenue_health": "unknown",  "backfill_verdict": "unknown",       "story_integrity": "unknown"},  # event itself externally unverifiable
    ("Digg", "2026-03-13"):       {"revenue_health": "weakness", "backfill_verdict": "frozen",        "story_integrity": "cracked"},  # ~3M visits vs Reddit 3.84B; bot-spam accelerated a low-traction relaunch
    ("Crypto.com", "2026-03-19"): {"revenue_health": "weakness", "backfill_verdict": "frozen",        "story_integrity": "cracked"},  # 3rd round since 2022; crypto-cycle downturn; generic "adapt or leave" language
    ("Cloudflare", "2026-05-07"): {"revenue_health": "strength", "backfill_verdict": "rehiring_same", "story_integrity": "cracked"},  # record +34% rev but gross margin 76->71%; sales spared; CEO vowed to exceed 2026 headcount by 2027
    ("UKG", "2026-04-15"):        {"revenue_health": "strength", "backfill_verdict": "offshore_swap", "story_integrity": "cracked"},  # +3,100 cut since 2024; PE-owned pre-IPO; AI one of 3 vague factors
    ("Epidemic Sound", "2026-04-21"): {"revenue_health": "weakness", "backfill_verdict": "frozen",    "story_integrity": "cracked"},  # 2025 growth 29->3%, neg EBITDA; "positive" H1'26 right after cuts; real AI product too
}

# ---------------------------------------------------------------------------
# ai_link_basis refinement (2026-07): events where the AI attribution came from
# the COMPANY itself but through an INFORMAL channel (CEO/founder tweet, LinkedIn
# post, blog, "AI-native" self-positioning, spokesperson quote) rather than a
# formal memo/filing/earnings call. These were previously lumped into
# press_inferred; company_informal separates "the company said it, casually"
# from "the press added the AI angle". Only upgrades press_inferred -> never
# overrides company_stated / company_denied. Verdict per-event read of each
# reason + source. The other 16 press-linked-AI events stay press_inferred.
INFORMAL_AI = {
    ("Angi", "2026-01-07"), ("Hailo", "2026-01-08"), ("Firebolt", "2026-02-15"),
    ("Zap Africa", "2026-02-28"), ("Stone", "2026-03-13"),
    ("Snowflake", "2026-03-19"), ("Monte Carlo", "2026-03-26"),
    ("Yupp", "2026-03-31"), ("Bolt", "2026-04-05"), ("Pendo", "2026-04-07"),
    ("Productboard", "2026-04-15"), ("Pentera", "2026-04-27"), ("ApnaMart", "2026-05-06"),
    ("DeepL", "2026-05-07"), ("Ticketmaster", "2026-05-07"), ("MRI Software", "2026-05-11"),
    ("Jumia", "2026-05-13"), ("Dune", "2026-05-14"), ("Gambling.com Group", "2026-05-14"),
    ("Innovaccer", "2026-05-14"), ("AI21 Labs", "2026-05-18"), ("ClickUp", "2026-05-21"),
    ("Robinhood", "2026-06-16"),
}

# ---------------------------------------------------------------------------
# Rule-based categorizer
# ---------------------------------------------------------------------------

def normalize(text):
    return (text or "").lower()

def classify_reason_primary(reason, theme, pct):
    """Pick a single root-cause label."""
    r = normalize(reason)
    t = normalize(theme)

    # 100% layoffs are shutdowns
    if pct == 1.0 or "shutdown" in t or "shut down" in r or "wind down" in r or "winding down" in r \
       or "bankrupt" in r or "ceased operations" in r or "cease operations" in r \
       or "filed for bankruptcy" in r or "closed entirely" in r:
        return "shutdown_bankruptcy"

    if "ipo" in r and ("pre-ipo" in r or "ahead of" in r or "planned ipo" in r or "pre ipo" in r) or "ipo prep" in t:
        return "ipo_prep"

    if any(k in t for k in ["post-acq", "m&a", "post acquisition", "post merger"]) \
       or "post-acquisition" in r or "post-merger" in r or "post merger" in r \
       or "after the" in r and "acquisition" in r or "after acquisition" in r \
       or "overlapping roles" in r and "acquisition" in r:
        return "m_and_a_consolidation"

    if "regulatory" in t or "compliance" in r and "drove" in r:
        return "regulatory"

    if any(k in r for k in ["offshoring", "closing german", "relocate", "relocating", "consolidat", "moved closer to us"]) and any(k in r for k in ["abroad", "overseas", "us customers", "europe", "germany"]):
        if "offshor" in r or "closing" in r and "office" in r or "relocat" in r:
            return "geographic_relocation"

    if ("lost" in r and ("contract" in r or "client" in r or "major client" in r)) \
       or "meta terminated" in r \
       or "market exit" in t \
       or ("exiting" in r and ("market" in r or "country" in r or "operations" in r)) \
       or ("doordash" in r and ("closed" in r or "qatar" in r)) \
       or ("market exit" in r):
        return "lost_contract_market_exit"

    # AI capex reallocation — requires (a) explicit redirect/shift action, and (b) AI infra/capex target
    redirect_action = any(k in r for k in [
        "redirect", "redirected", "redirecting",
        "shift investment toward", "shifts investment toward", "shifting investment toward",
        "free up resources for ai", "fund the ai", "fund ai",
        "redirect headcount spend", "redirect spending toward",
        "areas of strongest demand in the ai era",
    ])
    capex_target = any(k in r for k in [
        "ai capex", "ai infrastructure", "ai-enabled engineering", "ai engineering",
        "gpus", "data-center", "data center", "silicon",
        "ai-optim", "ai-focused roles", "stargate", "trainium", "gb300", "mi355x", "rainier", "4.5gw",
        "$50b", "$125b", "$145b", "$115b",
        "free up resources for ai",
    ])
    if redirect_action and capex_target:
        return "ai_capex_reallocation"
    if any(k in r for k in ["stargate", "trainium", "rainier", "gb300", "mi355x", "4.5gw",
                             "redirect headcount spend", "redirect spending toward ai",
                             "fund ai capex"]):
        return "ai_capex_reallocation"

    # AI substitution claim — CEO explicitly says AI does the work
    if any(k in r for k in ["smaller teams using ai", "smaller, highly talented teams using ai", "ai to automate more work",
                            "ai displacing", "ai replac", "ai does", "ai agents", "agents that can",
                            "manually writing code is over", "automate more work", "ai is helping staff work faster",
                            "smaller teams can do more", "ai-generated code", "ai is enabling smaller teams",
                            "ai-embedded teams", "agentic ai era", "internal ai usage grew",
                            "ai tools so smaller", "leveraging ai tools so smaller", "ai-driven", "ai-led"]):
        return "ai_substitution_claim"

    if "new ceo" in r or "took the helm" in r or "took over" in r and ("ceo" in r or "month") or \
       any(name in r for name in ["lores", "shapero", "jennifer morgan"]):
        return "new_ceo_turnaround"

    if "pivot" in t or "pivot" in r or "shifting focus" in r or "becoming an ai-first" in r \
       or "pivoting to" in r or "shifting some of our investment" in r or "transitioning into" in r \
       or "strategic repositioning" in r and "expand" in r:
        return "strategic_pivot"

    if any(k in r for k in ["cash-flow positive", "cash flow positive", "operating profit", "path to profitability",
                            "achieve profitability", "cash-generative", "operating profit", "to profitability"]):
        return "path_to_profitability"

    if any(k in r for k in ["downturn", "5g network investments", "fortnite engagement", "weakening demand",
                            "demand collapse", "weak earnings", "rising inflation", "stock decline"]):
        return "demand_collapse"

    if any(k in r for k in ["cost cut", "cost-cut", "cost structure", "savings", "annualized savings",
                            "cost discipline", "reduce its costs", "reducing costs", "margin pressure",
                            "$500m+ in annualized cost savings", "$1.5b in annualized", "$150m",
                            "operating leverage", "reducing complexity", "economic reasons"]) \
       or "cost cutting" in t:
        return "cost_cutting"

    if any(k in r for k in ["reducing layers", "removing bureaucracy", "simplifying", "simplif",
                            "aligning with strategic priorities", "align organizational structure",
                            "streamlining", "streamline", "operational efficiency", "operating model",
                            "restructuring", "realign", "reorganizing", "reorganization",
                            "consolidat", "right-sizing"]):
        return "restructuring_vague"

    if "not accessible" in r or "no public reason" in r:
        return "unknown"

    return "restructuring_vague"  # last resort


def classify_ai_link(reason, theme, primary):
    r = normalize(reason)
    t = normalize(theme)

    if primary == "shutdown_bankruptcy":
        # most shutdowns are unrelated; AI-eaten-market is the exception
        if any(k in r for k in ["ai models improved", "ai bot spam", "outcompeted", "specialized experts",
                                 "advanced image generation models", "ai-bot"]):
            return "ai_pivot_market"
        return "unrelated"

    if primary == "ai_substitution_claim":
        return "direct_substitution"
    if primary == "ai_capex_reallocation":
        return "capex_funding"

    # explicit denial
    if any(k in r for k in ["none of it had to do with ai", "not the cause", "ai automation was not",
                            "was not ai", "had nothing to do with ai", "was not driven by ai"]):
        return "ai_denied_but_adjacent"

    # AI pivot (the company changes its product/market to be AI)
    if any(k in r for k in ["ai-forward", "ai-first company", "ai-first", "ai-native", "ai pivot",
                            "physical ai", "robotics", "agentic ai era", "ai-native operating model",
                            "becoming an ai", "transformation accelerator", "ai transformation",
                            "double down on an ai", "ai integration"]) \
       or t == "ai pivot" or "pivot to ai" in r:
        return "ai_pivot_market"

    # direct substitution language
    if any(k in r for k in ["smaller teams", "agents", "automate", "ai displacing", "ai replac",
                             "65% of new code is now ai-generated", "ai-generated code", "ai is helping staff"]):
        return "direct_substitution"

    # capex funding — savings explicitly directed to AI (must mention AI)
    if any(k in r for k in ["savings into ai", "fund ai", "ai capex", "redirect resources to ai",
                             "directed toward ai", "redirect... ai", "ai investment", "ai capex",
                             "stargate", "trainium", "rainier", "$50b", "$125b", "$145b", "$115b",
                             "shift investment toward... ai", "ai infrastructure"]) \
       or ("redirect" in r and "ai" in r) \
       or ("reinvest" in r and "ai" in r):
        return "capex_funding"

    # AI mentioned but role is unclear
    if "ai" in r or "ml " in r or "artificial intelligence" in r:
        return "ai_denied_but_adjacent"

    return "unrelated"


def classify_narrative_source(reason, source_used):
    r = normalize(reason)
    if not r or "not accessible" in r or "no public reason" in r:
        return "not_accessible"
    # ceo_memo: leak with quote or named memo
    if any(k in r for k in ["memo:", "in a memo", "memo,", "internal memo", "wrote in", "ceo memo",
                              "wrote to staff", "told staff", "wrote in a post"]):
        return "ceo_memo"
    if any(k in r for k in ["sec filing", "8-k", "annual filing", "earnings call", "press release"]):
        return "press_release_sec"
    # quoted exec — name + "said" or "said in"
    if re.search(r"(ceo|cto|cpo|founder)\s+[a-z'.\- ]+(said|told|stated)", r) \
       or re.search(r"[a-z]\.\s*[a-z'.\- ]+\s+(said|told)", r) \
       or "spiegel" in r or "dorsey" in r or "zuckerberg" in r or "appoo" in r or "ellison" in r:
        return "news_with_quote"
    # if the source we actually used was a press release / SEC / company blog
    s = (source_used or "").lower()
    if "sec.gov" in s or "/news/" in s and any(d in s for d in ["blogs.cisco", "snap.com/news", "aboutamazon", "newsroom"]):
        return "press_release_sec"
    return "news_inferred"


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

with open(ROOT / "2026-enriched.json") as f:
    entries = json.load(f)

def classify_ai_position(company, primary, ai_link, industry):
    """Classify business-model relationship to the AI economy."""
    if company in AI_POSITION:
        return AI_POSITION[company]
    # rule-based fallback
    if primary in ("shutdown_bankruptcy", "regulatory", "geographic_relocation",
                   "lost_contract_market_exit", "m_and_a_consolidation"):
        if ai_link in ("direct_substitution", "capex_funding", "ai_pivot_market"):
            return "token_buyer"  # AI-related shutdowns / pivots
        return "n/a"
    if ai_link == "unrelated":
        return "n/a"
    if ai_link in ("direct_substitution", "ai_denied_but_adjacent", "ai_pivot_market"):
        return "token_buyer"
    if ai_link == "capex_funding":
        return "vertical_builder"  # rare default
    return "unknown"


out = []
for e in entries:
    primary = classify_reason_primary(e["reason"], e["theme_original"], e.get("pct"))
    ai_link = classify_ai_link(e["reason"], e["theme_original"], primary)
    narrative = classify_narrative_source(e["reason"], e.get("source_used"))
    ai_position = classify_ai_position(e["company"], primary, ai_link, e.get("industry"))

    key = (e["company"], e["date"])
    if key in MANUAL:
        m = MANUAL[key]
        primary = m.get("reason_primary", primary)
        ai_link = m.get("ai_link", ai_link)
        narrative = m.get("narrative_source", narrative)
        profiles_cut = m.get("profiles_cut", [])
        profiles_hired = m.get("profiles_hired", [])
        hire_overcorrection = m.get("hire_overcorrection")
        reassignment_observed = m.get("reassignment_observed", False)
    else:
        profiles_cut = []
        profiles_hired = []
        hire_overcorrection = None
        reassignment_observed = None

    # Axis 5: who established the AI connection (default from evidence axis,
    # computed on the PRE-migration ai_link so legacy denials map to company_denied)
    basis = default_ai_link_basis(ai_link, narrative)
    # Adjudication layer (primary-source verdicts) is authoritative
    if key in ADJUDICATION:
        a = ADJUDICATION[key]
        primary = a.get("reason_primary", primary)
        ai_link = a.get("ai_link", ai_link)
        narrative = a.get("narrative_source", narrative)
        basis = a.get("ai_link_basis", basis)
    # Legacy vocabulary migration: denial/pivot framing moved to ai_link_basis
    ai_link = AI_LINK_MIGRATION.get(ai_link, ai_link)

    # Informal-company AI attribution: upgrade press_inferred -> company_informal
    # for events where the company itself invoked AI casually (tweet/blog/quote).
    if key in INFORMAL_AI and basis == "press_inferred":
        basis = "company_informal"

    xc = CROSS_CHECK.get(key, {})

    e = {k: v for k, v in e.items() if k != "$_raised_mm"}  # byte-identical duplicate of raised_mm

    out.append({
        **e,
        "reason_primary": primary,
        "ai_link": ai_link,
        "ai_link_basis": basis,
        "revenue_health": xc.get("revenue_health"),
        "backfill_verdict": xc.get("backfill_verdict"),
        "story_integrity": xc.get("story_integrity"),
        "narrative_source": narrative,
        "ai_position": ai_position,
        "profiles_cut": profiles_cut,
        "profiles_hired": profiles_hired,
        "hire_overcorrection": hire_overcorrection,
        "reassignment_observed": reassignment_observed,
    })

# Guard: every override key must match a real (company, date) — a typo here
# silently drops a verdict (this exact failure mode shipped the Intuit mislabel)
_events = {(e["company"], e["date"]) for e in entries}
for name, d in (("MANUAL", MANUAL), ("ADJUDICATION", ADJUDICATION), ("CROSS_CHECK", CROSS_CHECK), ("INFORMAL_AI", INFORMAL_AI)):
    stale = set(d) - _events
    if stale:
        raise SystemExit(f"{name} keys match no event: {sorted(stale)}")
# AI_POSITION is keyed by company name (not company+date) — guard it too so a
# miscased/renamed key (e.g. "CyberArk" vs event "Cyberark") fails loudly instead
# of silently shipping the default position.
_companies = {e["company"] for e in entries}
stale_pos = set(AI_POSITION) - _companies
if stale_pos:
    raise SystemExit(f"AI_POSITION keys match no event company: {sorted(stale_pos)}")

# Write JSON
with open(ROOT / "2026-categorized.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# Write CSV
cols_csv = ["date", "company", "laid_off", "pct", "industry", "stage", "country",
            "reason_primary", "ai_link", "ai_link_basis", "narrative_source", "ai_position",
            "revenue_health", "backfill_verdict", "story_integrity",
            "hire_overcorrection", "reassignment_observed",
            "profiles_cut", "profiles_hired",
            "reason", "theme_original", "source_url", "source_used"]
with open(ROOT / "2026-categorized.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols_csv, extrasaction="ignore")
    w.writeheader()
    for r in out:
        row = dict(r)
        row["profiles_cut"] = "|".join(row.get("profiles_cut") or [])
        row["profiles_hired"] = "|".join(row.get("profiles_hired") or [])
        w.writerow(row)

# ---------- Write sources.md (per-event audit table) ----------
def _src_short(url):
    if not url:
        return ""
    if not str(url).startswith("http"):
        return f"`{url}`"  # e.g. "Internal memo"
    from urllib.parse import urlparse
    dom = urlparse(url).netloc.replace("www.", "")
    return f"[{dom}]({url})"

src_rows = sorted(out, key=lambda r: r["date"], reverse=True)
src_md = [
    "# Sources — fuente de cada evento de layoff",
    "",
    "*Mapping auditable de los eventos del dataset 2026. Cada fila lista la empresa, el count, "
    "la fuente original de layoffs.fyi, y (si la original estaba bloqueada) la fuente alternativa "
    "usada para recuperar la razón. **Generado automáticamente por `categorize.py`** — no editar a mano.*",
    "",
    "Referenciado desde [`methodology.md`](methodology.md) sección 2.",
    "",
    "Columnas: **fuente original** = el campo `Source` de layoffs.fyi. "
    "**fuente recovery** = fuente alternativa cuando la original era paywall/blocked (vacío si la original era accesible).",
    "",
    "| Fecha | Empresa | # | narrative_source | Fuente original | Fuente recovery (si aplica) |",
    "|---|---|---:|---|---|---|",
]
for r in src_rows:
    n = r.get("laid_off") or "—"
    orig = _src_short(r.get("source_url")) or "—"
    recov = _src_short(r.get("source_used"))
    src_md.append(
        f"| {r['date']} | {r['company']} | {n} | {r['narrative_source']} | {orig} | {recov} |"
    )
with open(ROOT / "sources.md", "w") as f:
    f.write("\n".join(src_md) + "\n")

# ---------- Cross-tabs ----------
from collections import Counter, defaultdict

print(f"Total entries: {len(out)}\n")

print("=== reason_primary ===")
for k, v in Counter(r["reason_primary"] for r in out).most_common():
    n = sum(r.get("laid_off") or 0 for r in out if r["reason_primary"] == k)
    print(f"  {k:<30} {v:>4}   {n:>7,} people")

print("\n=== ai_link ===")
for k, v in Counter(r["ai_link"] for r in out).most_common():
    n = sum(r.get("laid_off") or 0 for r in out if r["ai_link"] == k)
    print(f"  {k:<30} {v:>4}   {n:>7,} people")

print("\n=== ai_link x ai_link_basis (people) ===")
for k, v in Counter(r["ai_link_basis"] for r in out).most_common():
    n = sum(r.get("laid_off") or 0 for r in out if r["ai_link_basis"] == k)
    print(f"  {k:<30} {v:>4}   {n:>7,} people")

print("\n=== narrative_source ===")
for k, v in Counter(r["narrative_source"] for r in out).most_common():
    print(f"  {k:<30} {v:>4}")

print("\n=== ai_position (companies + people) ===")
positions = ["compute_seller","infra_seller","vertical_builder","hybrid","token_buyer","n/a","unknown"]
for p in positions:
    n_co = sum(1 for r in out if r["ai_position"] == p)
    n_pp = sum((r.get("laid_off") or 0) for r in out if r["ai_position"] == p)
    print(f"  {p:<22} {n_co:>4} companies   {n_pp:>7,} people")

print("\n=== ai_position x ai_link (companies) ===")
xtab2 = defaultdict(lambda: Counter())
for r in out:
    xtab2[r["ai_position"]][r["ai_link"]] += 1
ai_keys = ["direct_substitution","capex_funding","ai_pivot_market","ai_denied_but_adjacent","unrelated","unknown"]
print(f"{'':<22}" + " ".join(f"{k[:14]:>15}" for k in ai_keys))
for p in positions:
    if sum(xtab2[p].values()) == 0: continue
    print(f"  {p:<20}" + " ".join(f"{xtab2[p][ak]:>15}" for ak in ai_keys))

print("\n=== reason_primary x ai_link (companies) ===")
xtab = defaultdict(lambda: Counter())
for r in out:
    xtab[r["reason_primary"]][r["ai_link"]] += 1
ai_keys = ["direct_substitution","capex_funding","ai_pivot_market","ai_denied_but_adjacent","unrelated","unknown"]
print(f"{'':<32}" + " ".join(f"{k[:14]:>15}" for k in ai_keys))
for rk in sorted(xtab.keys()):
    print(f"  {rk:<30}" + " ".join(f"{xtab[rk][ak]:>15}" for ak in ai_keys))
