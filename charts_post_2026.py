"""
Gráficos para el post de opinión (layoffs tech 2026).

Genera tres PNG en ./charts/ a partir de 2026-categorized.json:
  - causas_mapa.png       (frecuencia de causas; las formas de IA resaltadas)
  - publico_privado.png   (tornado: causa por causa, privadas vs públicas)
  - embudo.png            (161 -> 1)

Estilo de marca (quierodolares / trabajoremoto): fondo lavanda, barras
redondeadas con "track" detrás, lavanda + un violeta saturado para destacar.
Los números salen del dataset (mismos que verificacion.md).
Correr: python3.12 charts_post_2026.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

ROOT = Path("/Users/muzk/code/layoffs")
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)

_JOST = ROOT / "assets" / "Jost-Bold.ttf"
FAM = "sans-serif"
if _JOST.exists():
    font_manager.fontManager.addfont(str(_JOST))
    FAM = "Jost"

# paleta de marca
BG     = "#F4F2FB"   # fondo lavanda claro
TRACK  = "#E7E3F3"   # riel detrás de las barras
BAR    = "#A08CDB"   # lavanda (barra normal)
HILITE = "#5B3FD1"   # violeta saturado (lo que se destaca)
INK    = "#17182B"
MUTED  = "#9A93A8"

plt.rcParams.update({
    "font.family": FAM,
    "font.size": 12,
    "text.color": INK,
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "savefig.facecolor": BG,
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


def _rbar(ax, x, y, w, h, color, rpx=9, z=3):
    """Barra/rectángulo con esquinas redondeadas (en coords de datos del ax)."""
    fig = ax.figure
    win, hin = fig.get_size_inches()
    sp = fig.subplotpars
    wpx = win * fig.dpi * (sp.right - sp.left)
    hpx = hin * fig.dpi * (sp.top - sp.bottom)
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    dxpp = abs(x1 - x0) / wpx
    dypp = abs(y1 - y0) / hpx
    rsize = rpx * dxpp
    aspect = dypp / dxpp
    if w <= 0 or h == 0:
        return
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rsize}",
        mutation_aspect=aspect, fc=color, ec="none", zorder=z, clip_on=False))


def _footer(fig):
    fig.text(0.5, 0.03, "trabajoremoto.cl", ha="center", fontsize=11,
             color=INK, fontweight="bold")


def causas_mapa():
    rows = [
        ("Reestructuración sin especificar", "restructuring_unspecified", False),
        ("Recorte de costos",                "cost_cutting",             False),
        ("La IA hace el trabajo",            "ai_substitution_claim",    True),
        ("Mención vaga de la IA",            "ai_framing_vague",         True),
        ("El vínculo lo pone la prensa",     "ai_press_narrative",       True),
        ("Fusión o adquisición",             "m_and_a",                  False),
    ]
    labels = [r[0] for r in rows]
    vals = [freq(D, r[1]) for r in rows]
    counts = [sum(1 for e in D if has(e, r[1])) for r in rows]
    cols = [HILITE if r[2] else BAR for r in rows]

    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    fig.subplots_adjust(left=0.345, right=0.97, top=0.78, bottom=0.09)
    n = len(rows)
    BH = 0.62
    xmax = max(vals) * 1.30
    ax.set_xlim(0, xmax)
    ax.set_ylim(n - 0.5, -0.5)
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels, fontsize=13)
    ax.set_xticks([])
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)

    for i, v in enumerate(vals):
        _rbar(ax, 0, i - BH / 2, xmax, BH, TRACK, z=2)          # riel
        _rbar(ax, 0, i - BH / 2, v, BH, cols[i], z=3)           # barra
        ax.annotate(f"  {counts[i]}", (v, i), va="center", ha="left",
                    fontsize=15, color=INK, fontweight="bold", zorder=4)
        ax.annotate(f"({v:.0f}%)", (v, i), xytext=(34, 0),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=10.5, color=MUTED, zorder=4)

    fig.text(0.035, 0.925, "Los motivos de los 161 despidos",
             fontsize=17, fontweight="bold", color=INK)
    fig.text(0.035, 0.86, "Número de anuncios en que aparece cada motivo, de mayor a menor · uno puede tener varios · en violeta, la IA",
             fontsize=10.5, color=MUTED)
    _footer(fig)
    fig.savefig(CHARTS / "causas_mapa.png")
    plt.close(fig)
    print("causas_mapa.png:", [f"{v:.0f}" for v in vals])


def publico_privado():
    rows = [
        ("Recorte de costos",           "cost_cutting"),
        ("La IA hace el trabajo",       "ai_substitution_claim"),
        ("Recortar para invertir en IA","ai_capex_reallocation"),
        ("Fusión o adquisición",        "m_and_a"),
        ("Mención vaga de la IA",       "ai_framing_vague"),
        ("Pivote de estrategia",        "strategic_pivot"),
        ("Cierre total",                "shutdown"),
    ]
    labels = [r[0] for r in rows]
    pub = [freq(PUB, r[1]) for r in rows]
    priv = [freq(PRIV, r[1]) for r in rows]
    mx = max(max(pub), max(priv)) * 1.16
    BH, STEP = 0.5, 1.5
    y = [i * STEP for i in range(len(rows))]

    fig, ax = plt.subplots(figsize=(9.0, 6.6))
    fig.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.07)
    ax.set_xlim(-mx, mx)
    ax.set_ylim(y[-1] + 0.9, y[0] - 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)
    ax.axvline(0, color="#D6D0E6", lw=1.2, zorder=1)

    for i, yy in enumerate(y):
        if priv[i] > 0.4:
            _rbar(ax, -priv[i], yy - BH / 2, priv[i], BH, BAR, z=3)
            ax.text(-priv[i] - mx * 0.02, yy, f"{priv[i]:.0f}%", ha="right",
                    va="center", fontsize=10.5, color=MUTED, fontweight="bold")
        if pub[i] > 0.4:
            _rbar(ax, 0, yy - BH / 2, pub[i], BH, HILITE, z=3)
            ax.text(pub[i] + mx * 0.02, yy, f"{pub[i]:.0f}%", ha="left",
                    va="center", fontsize=10.5, color=HILITE, fontweight="bold")
        ax.text(0, yy - BH / 2 - 0.15, labels[i], ha="center", va="bottom",
                fontsize=11.5, color=INK, fontweight="bold", zorder=6)

    top = y[0] - 1.05
    ax.text(-mx, top, "PRIVADAS", ha="left", va="center", fontsize=12,
            color=MUTED, fontweight="bold")
    ax.text(mx, top, "PÚBLICAS", ha="right", va="center", fontsize=12,
            color=HILITE, fontweight="bold")
    fig.text(0.035, 0.945, "Las causas se separan por tipo de empresa",
             fontsize=17, fontweight="bold", color=INK)
    fig.text(0.035, 0.895, "Las públicas concentran el 88% de las personas · el capex de IA es solo público; el cierre, solo privado",
             fontsize=10, color=MUTED)
    _footer(fig)
    fig.savefig(CHARTS / "publico_privado.png")
    plt.close(fig)
    print("publico_privado.png ok")


def embudo():
    stages = [
        (161, "anuncios de despidos", None, 0.90),
        (70,  "mencionan la IA de alguna forma", "91 no la nombraron (ni la empresa ni la prensa)", 0.60),
        (26,  'la empresa dice: "la IA hace el trabajo"',
              "16 solo la prensa · 3 la negaron · 19 mención vaga · 6 recorte para invertir en IA", 0.40),
        (3,   "con respaldo en los hechos", "11 se contradicen · 12 sin respaldo", 0.22),
        (1,   "MercadoLibre — 116 personas (0,1%)", "Coinbase y Wix: la IA convive con otras causas", 0.14),
    ]
    yc = [0.79, 0.625, 0.46, 0.295, 0.135]
    BH = 0.115
    fig, ax = plt.subplots(figsize=(9.0, 7.4))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.02)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for i, (cnt, desc, drop, w) in enumerate(stages):
        y = yc[i]
        color = HILITE if cnt == 1 else BAR
        tcol = "white" if cnt == 1 else INK
        _rbar(ax, 0.5 - w / 2, y - BH / 2, w, BH, color, rpx=11, z=3)
        if w >= 0.38:
            ax.text(0.5, y + 0.016, str(cnt), ha="center", va="center",
                    color=tcol, fontsize=26, fontweight="bold", zorder=5)
            ax.text(0.5, y - 0.03, desc, ha="center", va="center",
                    color=tcol, fontsize=10, zorder=5)
        else:
            ax.text(0.5, y, str(cnt), ha="center", va="center",
                    color=tcol, fontsize=20, fontweight="bold", zorder=5)
            ax.text(0.5 + w / 2 + 0.02, y, desc, ha="left", va="center",
                    color=(HILITE if cnt == 1 else INK), fontsize=10.5,
                    fontweight="bold", zorder=5)
        if drop:
            ax.text(0.5, (yc[i - 1] + y) / 2, "salen  " + drop, ha="center",
                    va="center", color=MUTED, fontsize=8.8, zorder=4)

    fig.text(0.035, 0.955, "¿Cuántos despidos fueron realmente por la IA?",
             fontsize=17, fontweight="bold", color=INK)
    fig.text(0.035, 0.905, "Filtramos los 161 anuncios hasta los casos donde la IA es realmente la causa del despido.",
             fontsize=10.5, color=MUTED)
    _footer(fig)
    fig.savefig(CHARTS / "embudo.png")
    plt.close(fig)
    print("embudo.png ok")


if __name__ == "__main__":
    causas_mapa()
    publico_privado()
    embudo()
    print("OK ->", CHARTS)
