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
AI_POSITION = {
    # ---- compute_seller (cloud / model APIs) ----
    "Oracle": "compute_seller",       # OCI; $300B OpenAI compute contract
    "Snowflake": "compute_seller",    # data cloud + AI services
    "C3.ai": "compute_seller",        # enterprise AI applications
    "AI21 Labs": "compute_seller",    # foundation model API
    "DeepL": "compute_seller",        # translation model API
    "Firebolt": "compute_seller",     # cloud data warehouse w/ AI features

    # ---- infra_seller (hardware/silicon/networking/data services) ----
    "Cisco": "infra_seller",          # silicon, optics, networking
    "Dell": "infra_seller",           # AI-optimized servers
    "ASML": "infra_seller",           # lithography — sells to TSMC for AI chips
    "Hailo": "infra_seller",          # AI inference chips
    "Sama": "infra_seller",           # data labeling for AI training
    "Foretellix": "infra_seller",     # AV simulation/validation toolchain

    # ---- vertical_builder (build own AI stack for own products) ----
    # Strict criterion: own foundation models + own silicon + own datacenters at hyperscaler scale.
    # MercadoLibre, Spotify, Netflix, LinkedIn etc. train task-specific models but don't qualify.
    # Apple/Tesla/ByteDance would qualify but had no 2026 layoffs.
    "Meta": "vertical_builder",       # Llama + MTIA + own datacenters + $125-145B capex
    "MercadoLibre": "token_buyer",    # reclassified: internal ML at scale but no foundation models / silicon

    # ---- hybrid (sells AI compute/services AND consumes internally) ----
    # Strict criterion (2026-06): "hybrid" requires selling AI infra/silicon/foundation
    # models to third parties — NOT just embedding LLM features into a SaaS product.
    # Companies like Atlassian/Autodesk/Shopify/Workday/GitLab/LinkedIn embed
    # Anthropic/OpenAI behind their features → they are token_buyers, not hybrids.
    "Amazon": "hybrid",               # AWS+Bedrock+Trainium+Nova+internal usage
    "Cloudflare": "hybrid",           # Workers AI sells inference + internal usage
    "Salesforce": "hybrid",           # Einstein + Agentforce + own xGen LLMs
    "LinkedIn": "token_buyer",        # consumes Azure AI internally — does not sell AI
    "Microsoft": "hybrid",            # would be hybrid if in dataset
    "Atlassian": "token_buyer",       # Rovo embeds Anthropic/OpenAI; no own infra
    "GitLab": "token_buyer",          # Duo AI embeds Anthropic; no own infra
    "Workday": "token_buyer",         # AI agents embed third-party LLMs
    "Smartsheet": "token_buyer",
    "Sonos": "n/a",                   # consumer audio, not AI-driven
    "Block": "token_buyer",           # Square/Cash App; uses AI via providers
    "WiseTech": "token_buyer",        # logistics SaaS using AI for code
    "PayPal": "token_buyer",          # AI integration partnerships
    "Intuit": "token_buyer",          # named Anthropic + OpenAI deals
    "Pinterest": "token_buyer",       # ad ranking via providers
    "Snap": "token_buyer",            # Snap My AI on OpenAI; AR hardware not AI silicon
    "Coinbase": "token_buyer",
    "ZoomInfo": "token_buyer",
    "Bill.com": "token_buyer",
    "UKG": "token_buyer",             # HR SaaS, AI-first via providers
    "Innovaccer": "token_buyer",      # healthtech AI partnerships
    "Wix": "token_buyer",             # Base44 acquisition + AI compute
    "Livspace": "token_buyer",
    "Pentera": "token_buyer",
    "Pendo": "token_buyer",
    "ApnaMart": "token_buyer",
    "Monte Carlo": "token_buyer",     # observability w/ AI
    "Digg": "token_buyer",            # AI agent reliance pre-shutdown
    "Zap Africa": "token_buyer",
    "Kraken": "token_buyer",
    "Flipkart": "token_buyer",
    "Playtika": "token_buyer",
    "CyberArk": "token_buyer",
    "Arctic Wolf": "token_buyer",
    "Adda247": "token_buyer",
    "Jumia": "token_buyer",
    "MRI Software": "token_buyer",
    "Envato": "token_buyer",
    "Stone": "token_buyer",
    "Coinbase": "token_buyer",
    "Tailwind Labs": "token_buyer",   # CSS framework, OSS lib; AI usage marginal
    "Adobe": "hybrid",
    "Pocket FM": "token_buyer",
    "GeoComply": "token_buyer",
    "Bolt": "token_buyer",
    "Acko": "token_buyer",
    "Productboard": "token_buyer",
    "Cars.com": "token_buyer",
    "Life360": "token_buyer",
    "DraftKings": "token_buyer",
    "Epidemic Sound": "token_buyer",  # music AI mentioned
    "Truecaller": "token_buyer",
    "MessageBird": "token_buyer",
    "LSports": "token_buyer",
    "Staffbase": "token_buyer",
    "Shopify": "token_buyer",         # Sidekick embeds third-party LLMs; SaaS w/ AI feature
    "Upwork": "token_buyer",
    "Eventbrite": "token_buyer",
    "Quora": "hybrid",                # Poe sells AI access + internal
    "GitLab": "token_buyer",
    "Crypto.com": "token_buyer",
    "Gemini": "token_buyer",          # crypto exchange, not Google Gemini
    "Atlassian": "token_buyer",
    "Envato": "token_buyer",

    # ---- n/a (AI not material to business model or layoff context) ----
    "Ericsson": "n/a",                # 5G telecom slowdown
    "Lucid Motors": "n/a",            # EV
    "Peloton": "n/a",                 # fitness hardware
    "GoPro": "n/a",                   # consumer cameras
    "Sonos": "n/a",
    "MicroVision": "n/a",             # LiDAR
    "StoreDot": "n/a",                # EV batteries
    "Remarkable": "n/a",              # e-ink tablets
    "Tamara Mellon": "n/a",
    "Easypost": "n/a",
    "TrueCar": "n/a",
    "Glossier": "n/a",
    "SSense": "n/a",                  # fashion e-commerce
    "Ocado": "n/a",                   # grocery automation
    "Careem": "n/a",                  # ride-hailing
    "Deliveroo": "n/a",
    "Zipcar": "n/a",
    "Welltech": "n/a",
    "Moon Active": "n/a",             # mobile games
    "Multiverse": "n/a",
    "Loopio": "n/a",
    "At-Bay": "n/a",
    "GoCardless": "n/a",
    "Epic Games": "n/a",              # Fortnite engagement
    "MARA": "n/a",                    # bitcoin mining
    "Polygon": "n/a",                 # crypto
    "Vimeo": "n/a",
    "Swyftx": "n/a",
    "Verint Systems": "n/a",
    "Clari": "token_buyer",
    "Dayforce": "n/a",
    "FormFactor": "n/a",
    "Tipalti": "n/a",
    "Zillow": "n/a",
    "Zupee": "n/a",
    "Zendesk": "token_buyer",
    "Ticketmaster": "n/a",
    "Angi": "n/a",
    "Kiwi.com": "n/a",
    "Codecademy/Skillsoft": "n/a",
    "Spotify": "hybrid",
    "Huawei": "hybrid",
    "OpenText": "hybrid",
    "eBay": "n/a",
    "Expedia": "n/a",
    "Autodesk": "token_buyer",        # AI features in Fusion/Forma; CAD/AEC core, not AI seller
    "Welltech": "n/a",
    "Roof Stacks": "n/a",
    "Kaseya": "n/a",
    "Enpal": "n/a",
    "Flipkart": "token_buyer",
    "Freshworks": "hybrid",           # Freddy AI sold + internal
    "InvestCloud": "n/a",
    "One Identity": "n/a",
    "Guesty": "n/a",
    "Breadfast": "n/a",
    "Gambling.com Group": "n/a",
    "Dune": "token_buyer",
    "Jumia": "token_buyer",
    "0G": "n/a",
    "Fi.Money": "n/a",
    "reAlpha": "token_buyer",
    "Quora": "hybrid",
    "Eventbrite": "token_buyer",
    "Esh Group": "n/a",
    "Rec Room": "n/a",
    "Yupp": "token_buyer",            # AI-feedback startup that lost PMF
    "NeuroPixel.AI": "compute_seller", # AI image gen for retail
    "Pepper Pay": "n/a",
    "Parker": "n/a",
    "Entropy": "n/a",
    "FranShares": "n/a",
    "Quandoo": "n/a",
    "Covrzy": "n/a",
    "Panda Squad": "n/a",
    "Supernal": "n/a",                # eVTOL
    "StarkWare": "n/a",               # ZK rollups
    "Polygon Labs": "n/a",
    "InvestCloud": "n/a",
    "Loopio": "n/a",
    "Bolt": "token_buyer",
    "IAC": "n/a",
    "SuperOps": "hybrid",
    "GeoComply": "token_buyer",
    "Productboard": "token_buyer",
    "ZoomInfo": "token_buyer",
    "Acko": "token_buyer",
    "Bolt": "token_buyer",
    "Cars.com": "token_buyer",
    "Life360": "token_buyer",
    "Oracle Health": "compute_seller",
    "Crypto.com": "token_buyer",
    "Gemini": "token_buyer",
    "Snowflake": "compute_seller",
    "Stone": "token_buyer",
    "Atlassian": "token_buyer",
    "Envato": "token_buyer",
    "Amazon": "hybrid",
    "Zap Africa": "token_buyer",
    "WiseTech": "token_buyer",
    "DraftKings": "token_buyer",
    "Livspace": "token_buyer",
    "Firebolt": "compute_seller",
    "Aleph Alpha": "compute_seller",  # German foundation model startup
    "eToro": "n/a",
    "Playtika": "token_buyer",
    "Bill.com": "token_buyer",
    "Hailo": "infra_seller",
    "Rewire": "n/a",
    "Foretellix": "infra_seller",
    "Pinterest": "token_buyer",
    "Cisco": "infra_seller",
    "Welltech": "n/a",
    "ASML": "infra_seller",
    "Amazon": "hybrid",
    "Kaseya": "n/a",
    "Multiverse": "n/a",
    "Axonius": "token_buyer",
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
        "narrative_source": "news_inferred",
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
        "ai_link": "direct_substitution",  # Claude Sonnet replacing dozens of mid-engineers cited
        "narrative_source": "ceo_memo",
        "profiles_cut": ["SDE_II", "middle_management_L6_L7", "PXT_HR_recruiting", "AWS_TAM_solutions_architects", "Alexa_AI_legacy", "Prime_Video_platform_eng", "Amazon_Pharmacy", "TPMs"],
        "profiles_hired": ["AGI_team_Nova", "Trainium_chip_team", "Bedrock_agents", "Frontier_AI_Robotics", "Project_Rainier_data_center"],
        "hire_overcorrection": False,  # Amazon was -1.3% in SWE last 2 yrs (Pragmatic Engineer)
        "reassignment_observed": False,
    },
    # ---------------------- Intuit ----------------------
    ("Intuit", "2026-05-20"): {
        "reason_primary": "restructuring_vague",
        "ai_link": "ai_denied_but_adjacent",  # CEO explicitly denied AI
        "narrative_source": "ceo_memo",
        "profiles_cut": ["engineering_CA", "customer_support", "marketing", "admin", "satellite_offices_Reno_WoodlandHills", "middle_management"],
        "profiles_hired": ["AI_ML_engineers_Mountain_View", "Anthropic_OpenAI_integration_roles"],
        "hire_overcorrection": False,
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
    },
    # Wix: "rising AI compute costs... roles becoming redundant in the AI era"
    ("Wix", "2026-05-25"): {
        "reason_primary": "cost_cutting",
        "ai_link": "ai_denied_but_adjacent",
        "narrative_source": "news_with_quote",
    },
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
    ("Salesforce",   "2026-02-09"): {"ai_link": "unrelated"},  # no public framing; Agentforce team cut
    ("Peloton",      "2026-01-30"): {"ai_link": "unrelated"},  # fitness hardware cost cuts
    ("Vimeo",        "2026-01-21"): {"ai_link": "unrelated"},  # Bending Spoons PE playbook
    ("StoreDot",     "2026-01-13"): {"ai_link": "unrelated"},  # SPAC merger prep, batteries

    # 4 cases that are direct_substitution (CEO openly said AI does the work):
    ("Freshworks",   "2026-05-05"): {"ai_link": "direct_substitution"},  # "over half of our code is written by AI"
    ("Upwork",       "2026-05-07"): {"ai_link": "direct_substitution"},  # "AI means smaller, differently resourced teams"
    ("Kraken",       "2026-05-15"): {"ai_link": "direct_substitution"},  # AI chatbot handles 80% of customer inquiries
    ("Crypto.com",   "2026-03-19"): {"ai_link": "direct_substitution"},  # "roles that do not adapt to AI"

    # 2 cases that are ai_pivot_market (product/market pivot to AI):
    ("Epidemic Sound","2026-04-21"): {"ai_link": "ai_pivot_market"},  # AI-generated music
    ("AI21 Labs",    "2026-05-18"): {"ai_link": "ai_pivot_market"},  # foundation models → agent orchestration

    # 2 more found in second audit (2026-06-04): denied AI but no evidence of AI investment.
    # Epic Games: Fortnite engagement collapse — explicit AI denial, demand collapse driver.
    # Remarkable: AI mentioned as macroeconomic cost pressure (chip shortage), not their investment.
    ("Epic Games",   "2026-03-24"): {"ai_link": "unrelated"},
    ("Remarkable",   "2026-04-22"): {"ai_link": "unrelated"},
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

    out.append({
        **e,
        "reason_primary": primary,
        "ai_link": ai_link,
        "narrative_source": narrative,
        "ai_position": ai_position,
        "profiles_cut": profiles_cut,
        "profiles_hired": profiles_hired,
        "hire_overcorrection": hire_overcorrection,
        "reassignment_observed": reassignment_observed,
    })

# Write JSON
with open(ROOT / "2026-categorized.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# Write CSV
cols_csv = ["date", "company", "laid_off", "pct", "industry", "stage", "country",
            "reason_primary", "ai_link", "narrative_source", "ai_position",
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
