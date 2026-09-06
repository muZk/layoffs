"""
Gráficos para el post de opinión (layoffs tech 2026).

Genera dos PNG en ./charts/ a partir de 2026-categorized.json:
  - causas_mapa.png            (frecuencia de causas; las 3 formas de IA resaltadas)
  - publico_privado.png        (tornado: causa por causa, privadas vs públicas)

Los números se calculan desde el dataset (mismos que verificacion.md).
Correr: python3.12 charts_post_2026.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path("/Users/muzk/code/layoffs")
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)

_JOST = ROOT / "assets" / "Jost-Bold.ttf"
FAM = "sans-serif"
if _JOST.exists():
    font_manager.fontManager.addfont(str(_JOST))
    FAM = "Jost"

INK    = "#191E28"
MUTED  = "#8992A1"   # neutral / privadas / causas no-IA
ACCENT = "#A96D0E"   # ámbar / IA / públicas
GRID   = "#E7E9EE"

plt.rcParams.update({
    "font.family": FAM,
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "text.color": INK,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": INK,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.dpi": 170,
    "figure.dpi": 130,
})

D = [e for e in json.load(open(ROOT / "2026-categorized.json")) if e["date"] < "2026-07-01"]
N = len(D)
PUB = [e for e in D if e["stage"] == "Post-IPO"]
PRIV = [e for e in D if e["stage"] not in ("Post-IPO", "Unknown")]


def has(e, c):
    return c in (e.get("causes") or [])


def freq(group, c):
    return 100 * sum(1 for e in group if has(e, c)) / len(group)


def causas_mapa():
    rows = [
        ("Reestructuración sin especificar", "restructuring_unspecified", False),
        ("Recorte de costos",                "cost_cutting",             False),
        ("La empresa: la IA hace el trabajo","ai_substitution_claim",    True),
        ("La empresa menciona la IA, vaga",  "ai_framing_vague",         True),
        ("El vínculo lo pone la prensa",     "ai_press_narrative",       True),
        ("Fusión o adquisición",             "m_and_a",                  False),
    ]
    labels = [r[0] for r in rows]
    vals = [freq(D, r[1]) for r in rows]
    cols = [ACCENT if r[2] else MUTED for r in rows]

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    y = range(len(rows))
    ax.barh(y, vals, color=cols, height=0.66, zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.16)
    for i, v in enumerate(vals):
        ax.text(v + max(vals) * 0.015, i, f"{v:.0f}%", va="center", ha="left",
                fontsize=12, color=INK, fontweight="bold")
    ax.set_xticks([])
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID)
    fig.text(0.035, 0.925, "El motivo más común es un no-motivo",
             fontsize=16, fontweight="bold", color=INK)
    fig.text(0.035, 0.865, "En qué % de los 161 despidos aparece cada causa · en ámbar, las tres formas de nombrar la IA",
             fontsize=10.5, color=MUTED)
    fig.text(0.99, 0.02, "trabajoremoto.cl · 161 despidos tech, ene–jun 2026",
             ha="right", fontsize=8.5, color=MUTED)
    fig.subplots_adjust(left=0.34, right=0.97, top=0.80, bottom=0.10)
    fig.savefig(CHARTS / "causas_mapa.png")
    plt.close(fig)
    print("causas_mapa.png:", [f"{v:.0f}" for v in vals])


def publico_privado():
    rows = [
        ("Recorte de costos",          "cost_cutting"),
        ("La IA hace el trabajo",      "ai_substitution_claim"),
        ("Recortar para invertir en IA","ai_capex_reallocation"),
        ("Fusión o adquisición",       "m_and_a"),
        ("La IA como marco vago",      "ai_framing_vague"),
        ("Pivote de estrategia",       "strategic_pivot"),
        ("Cierre total",               "shutdown"),
    ]
    labels = [r[0] for r in rows]
    pub = [freq(PUB, r[1]) for r in rows]
    priv = [freq(PRIV, r[1]) for r in rows]
    mx = max(max(pub), max(priv)) * 1.15

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    y = list(range(len(rows)))
    ax.barh(y, [-v for v in priv], color=MUTED, height=0.6, zorder=3)
    ax.barh(y, pub, color=ACCENT, height=0.6, zorder=3)
    ax.invert_yaxis()
    ax.axvline(0, color="#C9CDd6", lw=1, zorder=2)
    ax.set_xlim(-mx, mx)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)

    for i in y:
        # etiqueta de la causa, centrada, con caja blanca
        ax.text(0, i - 0.42, labels[i], ha="center", va="bottom", fontsize=10.5,
                color=INK, zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
        if priv[i] > 0.4:
            ax.text(-priv[i] - mx * 0.02, i, f"{priv[i]:.0f}%", ha="right", va="center",
                    fontsize=10, color=MUTED, fontweight="bold")
        if pub[i] > 0.4:
            ax.text(pub[i] + mx * 0.02, i, f"{pub[i]:.0f}%", ha="left", va="center",
                    fontsize=10, color=ACCENT, fontweight="bold")

    ax.text(-mx, -1.15, "PRIVADAS", ha="left", va="center", fontsize=11.5,
            color=MUTED, fontweight="bold")
    ax.text(mx, -1.15, "PÚBLICAS", ha="right", va="center", fontsize=11.5,
            color=ACCENT, fontweight="bold")
    ax.set_ylim(len(rows) - 0.4, -1.6)
    ax.set_title("Las causas se separan por tipo de empresa", pad=34, loc="left", x=-0.0)
    ax.text(0.5, 1.075, "Las públicas concentran el 88% de las personas · el capex de IA es solo público; el cierre, solo privado",
            transform=ax.transAxes, fontsize=10, color=MUTED, ha="center")
    fig.text(0.99, 0.02, "trabajoremoto.cl · 161 despidos tech, ene–jun 2026",
             ha="right", fontsize=8.5, color=MUTED)
    fig.subplots_adjust(left=0.04, right=0.96, top=0.80, bottom=0.08)
    fig.savefig(CHARTS / "publico_privado.png")
    plt.close(fig)
    print("publico_privado.png: pub", [f"{v:.0f}" for v in pub], "priv", [f"{v:.0f}" for v in priv])


if __name__ == "__main__":
    causas_mapa()
    publico_privado()
    print("OK ->", CHARTS)
