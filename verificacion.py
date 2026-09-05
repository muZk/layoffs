"""
Verificación de los datos agregados del resumen "161 despidos, uno por uno".

Cada función reproduce un dato citado en el resumen, con la consulta exacta
sobre el dataset y el resultado. Correr:  python3 verificacion.py
(requiere el intérprete con acceso a 2026-categorized.json; sin dependencias externas)

Ventana: date < 2026-07-01  ->  161 eventos, 108.089 personas con cifra.
Público  = stage == "Post-IPO" (67).  Privado = stage conocido y no público (71);
"Unknown" (23) se excluye del corte público/privado.
"""
import json, statistics, collections

D = [e for e in json.load(open("2026-categorized.json")) if e["date"] < "2026-07-01"]
HEADS = sum(e["laid_off"] for e in D if e.get("laid_off"))
PUB = [e for e in D if e["stage"] == "Post-IPO"]
PRIV = [e for e in D if e["stage"] not in ("Post-IPO", "Unknown")]


def has(e, tag):
    return tag in (e.get("causes") or [])


def dato_1_mapa_de_causas():
    """El motivo más común es un no-motivo: 58% causa única, y suele ser vaga."""
    single = [e for e in D if len(e.get("causes") or []) == 1]
    vague = [e for e in single if e["causes"][0] in
             ("restructuring_unspecified", "cost_cutting", "unknown")]
    print(f"[1] causa única: {len(single)}/{len(D)} = {100*len(single)/len(D):.0f}% | "
          f"de esas, motivo genérico o ninguno: {len(vague)} "
          f"(reestructuración+costos+sin causa)")
    cf = collections.Counter(c for e in D for c in (e.get("causes") or []))
    print("    causas más nombradas (de 161):")
    for c, n in cf.most_common(6):
        print(f"      {n:3}  ({100*n/len(D):4.0f}%)  {c}")


def dato_2_meli_unica():
    """De 161, MercadoLibre es el único caso de causa única = IA que se sostiene."""
    ai_only = [e for e in D if e.get("causes") == ["ai_substitution_claim"]]
    print(f"[2] eventos con la IA como única causa etiquetada: {len(ai_only)}")
    for e in ai_only:
        print(f"      {e['ai_claim_verdict']:18} {e['company']:14} ({e.get('laid_off')})")
    plaus = [e for e in ai_only if e["ai_claim_verdict"] == "plausible"]
    print(f"    únicos 'plausible': {[e['company'] for e in plaus]} "
          f"= {plaus[0]['laid_off']} personas ({100*plaus[0]['laid_off']/HEADS:.1f}%)")


def dato_3_ia_casi_nunca_sola():
    """De las 26 que culparon a la IA, 16 (62%) traen otra causa; 3/11/12 en verdicto."""
    subs = [e for e in D if has(e, "ai_substitution_claim")]
    multi = [e for e in subs if len(e["causes"]) > 1]
    print(f"[3] reclamos de sustitución: {len(subs)} | multi-causa: {len(multi)} "
          f"= {100*len(multi)/len(subs):.0f}% | causa única: {len(subs)-len(multi)}")
    co = collections.Counter(c for e in subs for c in e["causes"]
                             if c != "ai_substitution_claim")
    print(f"    co-ocurre con la IA: {dict(co.most_common(4))}")
    vc = collections.Counter(e.get("ai_claim_verdict") for e in subs)
    contra = vc.get("contradicted_soft", 0) + vc.get("contradicted_hard", 0)
    print(f"    verdicto: se sostienen={vc.get('plausible',0)} | se contradicen={contra} | "
          f"sin verificar={vc.get('thin_evidence',0)}")


def dato_4_dos_caras():
    """Dos caras de 'culpar a la IA': reemplazo (26) vs gasto/capex (6). Oracle."""
    subs = [e for e in D if has(e, "ai_substitution_claim")]
    capex = [e for e in D if has(e, "ai_capex_reallocation")]
    print(f"[4] reemplazo (ai_substitution_claim): {len(subs)} | "
          f"gasto/capex (ai_capex_reallocation): {len(capex)} "
          f"-> {[e['company'] for e in capex]}")
    o = next(e for e in D if e["company"] == "Oracle")
    print(f"    Oracle: {o['laid_off']:,} = {100*o['laid_off']/HEADS:.0f}% del total | "
          f"causes={o['causes']} verdict={o['ai_claim_verdict']} "
          f"(mención propia = línea condicional en el 10-K, Item 1A + Note 7)")


def dato_5_sin_senal_ia():
    """En los 91 sin señal de IA, buscamos igual si el recorte pudo ser IA."""
    AI = {"ai_substitution_claim", "ai_capex_reallocation", "ai_framing_vague",
          "ai_press_narrative", "ai_denied"}
    nosig = [e for e in D if not (set(e["causes"]) & AI)]
    heads = sum(e["laid_off"] for e in nosig if e.get("laid_off"))
    conc = [e for e in nosig if set(e["causes"]) &
            {"shutdown", "m_and_a", "financial_distress", "market_exit", "demand_collapse"}]
    unk = [e for e in nosig if e["causes"] == ["unknown"]]
    print(f"[5] sin señal de IA: {len(nosig)} anuncios, {heads:,} personas = "
          f"{100*heads/HEADS:.0f}% del total")
    print(f"    motivo concreto/verificable: {len(conc)} | sin motivo alguno (unknown): {len(unk)} "
          f"| resto con motivo vago (reestructuración/costos)")
    print("    no hay test positivo para una sustitución no declarada ni reportada")


def dato_6_negaciones():
    """Dos grandes negaron la IA de frente; en 16 el vínculo lo puso solo la prensa."""
    denied = [e for e in D if has(e, "ai_denied")]
    press = [e for e in D if has(e, "ai_press_narrative")]
    press_cifra = [e["laid_off"] for e in press if e.get("laid_off")]
    print(f"[6] negaciones explícitas (ai_denied): {len(denied)} "
          f"-> {[e['company'] for e in denied]}")
    print(f"    vínculo puesto solo por la prensa (ai_press_narrative): {len(press)} | "
          f"con cifra: {len(press_cifra)}, suman {sum(press_cifra):,}")


def dato_7_sobrecontratacion():
    """La sobre-contratación entró como causa candidata y explica a un grupo, no al resto.

    No se reproduce desde este dataset: la dotación sale de los filings (10-K/20-F),
    empresa por empresa, en dos ventanas (2020-2022 y 2023 en adelante). Ver
    auditoria-sobrecontratacion.md."""
    print("[7] Dotación desde filings (no desde este dataset) — ver auditoria-sobrecontratacion.md")


def dato_8_publicas_vs_privadas():
    """El peso humano es casi todo público (88%); las causas se separan por tipo de empresa."""
    hp = sum(e["laid_off"] for e in PUB if e.get("laid_off"))
    hv = sum(e["laid_off"] for e in PRIV if e.get("laid_off"))
    mp = statistics.median([e["laid_off"] for e in PUB if e.get("laid_off")])
    mv = statistics.median([e["laid_off"] for e in PRIV if e.get("laid_off")])
    print(f"[8] público={len(PUB)} anuncios, {hp:,} personas = {100*hp/HEADS:.0f}% del total | "
          f"privado={len(PRIV)}, {hv:,} = {100*hv/HEADS:.0f}%")
    print(f"    mediana por anuncio: público={mp:.0f} | privado={mv:.0f}")

    def rate(g, c):
        return 100 * sum(1 for e in g if has(e, c)) / len(g)
    print("    sesgo de causas (público% vs privado%):")
    for c in ("cost_cutting", "ai_capex_reallocation", "ai_substitution_claim",
              "shutdown", "strategic_pivot", "ai_framing_vague", "m_and_a"):
        print(f"      {c:26} {rate(PUB,c):4.0f}% vs {rate(PRIV,c):4.0f}%")

    nocifra = [e for e in D if not e.get("laid_off")]
    vals = sorted((e["laid_off"] for e in D if e.get("laid_off")), reverse=True)
    top10 = sum(vals[:10])
    print(f"    concentración: {len(nocifra)} sin cifra | "
          f"top-10 = {top10:,} = {100*top10/HEADS:.0f}% del total")


if __name__ == "__main__":
    print(f"Ventana in-window: {len(D)} eventos | {HEADS:,} personas con cifra")
    print(f"Público (Post-IPO)={len(PUB)} | Privado={len(PRIV)} | "
          f"Unknown excluido={len(D)-len(PUB)-len(PRIV)}\n")
    for fn in (dato_1_mapa_de_causas, dato_2_meli_unica, dato_3_ia_casi_nunca_sola,
               dato_4_dos_caras, dato_5_sin_senal_ia, dato_6_negaciones,
               dato_7_sobrecontratacion, dato_8_publicas_vs_privadas):
        print(f"--- {fn.__doc__.splitlines()[0]}")
        fn()
        print()
