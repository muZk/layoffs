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
from matplotlib.patches import Rectangle

ROOT = Path("/Users/muzk/code/layoffs")
CHARTS = ROOT / "charts"
CHARTS.mkdir(exist_ok=True)

_JOST = ROOT / "assets" / "Jost-Bold.ttf"
FAM = "sans-serif"
if _JOST.exists():
    font_manager.fontManager.addfont(str(_JOST))
    FAM = "Jost"

# paleta "color pop": acento vivo sobre grises fríos
INK    = "#16181D"
MUTED  = "#9AA3B2"   # neutral / privadas / causas no-IA
ACCENT = "#3D5AFE"   # índigo eléctrico / IA / públicas / hilo del embudo
POP2   = "#FF5247"   # coral / el remate (MercadoLibre)
GRID   = "#EBEDF2"

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
        ("La IA hace el trabajo",            "ai_substitution_claim",    True),
        ("Mención vaga de la IA",            "ai_framing_vague",         True),
        ("El vínculo lo pone la prensa",     "ai_press_narrative",       True),
        ("Fusión o adquisición",             "m_and_a",                  False),
    ]
    labels = [r[0] for r in rows]
    vals = [freq(D, r[1]) for r in rows]
    counts = [sum(1 for e in D if has(e, r[1])) for r in rows]
    cols = [ACCENT if r[2] else MUTED for r in rows]

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    y = range(len(rows))
    ax.barh(y, vals, color=cols, height=0.66, zorder=3)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, max(vals) * 1.32)
    for i, v in enumerate(vals):
        ax.annotate(f"  {counts[i]}", (v, i), va="center", ha="left",
                    fontsize=14, color=INK, fontweight="bold")
        ax.annotate(f"  ({v:.0f}%)", (v, i), va="center", ha="left",
                    fontsize=10.5, color=MUTED,
                    xytext=(28, 0), textcoords="offset points")
    ax.set_xticks([])
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID)
    fig.text(0.035, 0.925, "Los motivos de los 161 despidos",
             fontsize=16, fontweight="bold", color=INK)
    fig.text(0.035, 0.865, "Número de anuncios (de 161) en que aparece cada motivo, de mayor a menor · uno puede tener varios · en azul, la IA",
             fontsize=10.5, color=MUTED)
    fig.text(0.99, 0.02, "trabajoremoto.cl · 161 despidos tech, ene–jun 2026",
             ha="right", fontsize=8.5, color=MUTED)
    fig.subplots_adjust(left=0.345, right=0.97, top=0.80, bottom=0.10)
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

    STEP, BH = 1.5, 0.5
    y = [i * STEP for i in range(len(rows))]
    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    ax.barh(y, [-v for v in priv], color=MUTED, height=BH, zorder=3)
    ax.barh(y, pub, color=ACCENT, height=BH, zorder=3)
    ax.axvline(0, color="#C9CDD6", lw=1, zorder=2)
    ax.set_xlim(-mx, mx)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ("top", "right", "bottom", "left"):
        ax.spines[s].set_visible(False)

    for i, yy in enumerate(y):
        # etiqueta de la causa: en el aire, arriba de cada par de barras
        ax.text(0, yy - BH / 2 - 0.14, labels[i], ha="center", va="bottom",
                fontsize=11.5, color=INK, fontweight="bold", zorder=6)
        if priv[i] > 0.4:
            ax.text(-priv[i] - mx * 0.02, yy, f"{priv[i]:.0f}%", ha="right", va="center",
                    fontsize=10.5, color=MUTED, fontweight="bold")
        if pub[i] > 0.4:
            ax.text(pub[i] + mx * 0.02, yy, f"{pub[i]:.0f}%", ha="left", va="center",
                    fontsize=10.5, color=ACCENT, fontweight="bold")

    top = y[0] - 1.05
    ax.text(-mx, top, "PRIVADAS", ha="left", va="center", fontsize=12,
            color=MUTED, fontweight="bold")
    ax.text(mx, top, "PÚBLICAS", ha="right", va="center", fontsize=12,
            color=ACCENT, fontweight="bold")
    ax.set_ylim(y[-1] + BH / 2 + 0.35, y[0] - 1.5)
    fig.text(0.035, 0.945, "Las causas se separan por tipo de empresa",
             fontsize=16, fontweight="bold", color=INK)
    fig.text(0.035, 0.895, "Las públicas concentran el 88% de las personas · el capex de IA es solo público; el cierre, solo privado",
             fontsize=10, color=MUTED)
    fig.text(0.99, 0.02, "trabajoremoto.cl · 161 despidos tech, ene–jun 2026",
             ha="right", fontsize=8.5, color=MUTED)
    fig.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.07)
    fig.savefig(CHARTS / "publico_privado.png")
    plt.close(fig)
    print("publico_privado.png: pub", [f"{v:.0f}" for v in pub], "priv", [f"{v:.0f}" for v in priv])


def embudo():
    # (cuenta, descripción, texto de lo que sale antes de este paso, ancho 0-1)
    stages = [
        (161, "anuncios de despidos", None, 0.90),
        (70,  "mencionan la IA de alguna forma", "91 no la nombraron (ni la empresa ni la prensa)", 0.60),
        (26,  'la empresa dice: "la IA hace el trabajo"',
              "16 solo la prensa · 3 la negaron · 19 mención vaga · 6 recorte para invertir en IA", 0.40),
        (3,   "se sostienen al revisar los hechos", "11 se contradicen · 12 sin forma de verificar", 0.22),
        (1,   "MercadoLibre — 116 personas (0,1%)", "Coinbase y Wix: la IA convive con otras causas", 0.14),
    ]
    yc = [0.79, 0.625, 0.46, 0.295, 0.135]
    BH = 0.11
    fig, ax = plt.subplots(figsize=(8.8, 7.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for i, (cnt, desc, drop, w) in enumerate(stages):
        y = yc[i]
        color = POP2 if cnt == 1 else ACCENT
        ax.add_patch(Rectangle((0.5 - w / 2, y - BH / 2), w, BH, fc=color,
                               ec="none", zorder=3))
        if w >= 0.38:  # cabe adentro
            ax.text(0.5, y + 0.016, str(cnt), ha="center", va="center",
                    color="white", fontsize=25, fontweight="bold", zorder=4)
            ax.text(0.5, y - 0.028, desc, ha="center", va="center",
                    color="white", fontsize=10, zorder=4)
        else:  # barra chica: número adentro, descripción a la derecha
            ax.text(0.5, y, str(cnt), ha="center", va="center",
                    color="white", fontsize=19, fontweight="bold", zorder=4)
            ax.text(0.5 + w / 2 + 0.02, y, desc, ha="left", va="center",
                    color=(POP2 if cnt == 1 else INK), fontsize=10.5,
                    fontweight="bold", zorder=4)
        if drop:
            ax.text(0.5, (yc[i - 1] + y) / 2, "salen  " + drop, ha="center",
                    va="center", color=MUTED, fontsize=8.8, zorder=4)

    fig.text(0.035, 0.955, "¿Cuántos despidos fueron realmente por la IA?",
             fontsize=17, fontweight="bold", color=INK)
    fig.text(0.035, 0.905, "Filtramos los 161 anuncios hasta los casos donde la IA es realmente la causa del despido.",
             fontsize=10.5, color=MUTED)
    fig.text(0.99, 0.02, "trabajoremoto.cl · 161 despidos tech, ene–jun 2026",
             ha="right", fontsize=8.5, color=MUTED)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.01)
    fig.savefig(CHARTS / "embudo.png")
    plt.close(fig)
    print("embudo.png ok")


if __name__ == "__main__":
    causas_mapa()
    publico_privado()
    embudo()
    print("OK ->", CHARTS)
