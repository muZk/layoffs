"""
Verificación de los datos agregados del resumen "161 despidos, uno por uno".

Cada función reproduce un dato citado en el resumen, con la consulta exacta
sobre el dataset y el resultado. Correr:  python3 verificacion.py
(requiere el intérprete con acceso a 2026-categorized.json; sin dependencias externas)

Ventana: date < 2026-07-01  ->  161 eventos, 108.089 personas con cifra.
"""
import json, statistics, collections

D = [e for e in json.load(open("2026-categorized.json")) if e["date"] < "2026-07-01"]
HEADS = sum(e["laid_off"] for e in D if e.get("laid_off"))


def has(e, tag):
    return tag in (e.get("causes") or [])


def dato_1_casi_la_mitad():
    """Casi la mitad de las personas trabajaba en empresas que dieron a la IA como motivo."""
    comp_ai = [e for e in D if e.get("ai_link_basis") in ("company_stated", "company_informal")
               and e.get("ai_link") in ("direct_substitution", "capex_funding")]
    h = sum(e["laid_off"] for e in comp_ai if e.get("laid_off"))
    subs = [e for e in D if has(e, "ai_substitution_claim")]
    hs = sum(e["laid_off"] for e in subs if e.get("laid_off"))
    print(f"[1] empresa invocó la IA (reemplazo o inversión): {len(comp_ai)} eventos, "
          f"{h:,} personas = {100*h/HEADS:.1f}% de {HEADS:,}")
    print(f"    subconjunto solo 'sustitución': {len(subs)} eventos, {hs:,} = {100*hs/HEADS:.1f}%")


def dato_2_oracle():
    """Oracle: participación (19%) y su marco de marzo vs el reporte anual."""
    o = next(e for e in D if e["company"] == "Oracle")
    print(f"[2] Oracle: {o['laid_off']:,} personas = {100*o['laid_off']/HEADS:.1f}% del total")
    print(f"    causes={o['causes']}  verdict={o['ai_claim_verdict']}")
    print(f"    marzo (extracto reason): "
          f"...{'cambio organizacional' if 'organizational change' in o['reason'] else '?'}... "
          f"la frase de IA vive en el 10-K FY26 (Item 1A + Note 7)")


def dato_3_verdictos_27():
    """De las 27 que dijeron 'la IA hace ese trabajo': 3 se sostienen / 11 se contradicen / 13 thin."""
    subs = [e for e in D if has(e, "ai_substitution_claim")]
    vc = collections.Counter(e.get("ai_claim_verdict") for e in subs)
    hold = vc.get("plausible", 0)
    contra = vc.get("contradicted_soft", 0) + vc.get("contradicted_hard", 0)
    thin = vc.get("thin_evidence", 0)
    print(f"[3] claims de sustitución: {len(subs)}  ->  se sostienen(plausible)={hold} | "
          f"se contradicen(soft+hard)={contra} | sin verificar(thin)={thin}")
    print(f"    detalle: {dict(vc)}")


def dato_4_prensa_16():
    """En 16 casos el vínculo con la IA lo puso la prensa (no la empresa)."""
    press = [e for e in D if has(e, "ai_press_narrative")]
    print(f"[4] vínculo IA aportado por la prensa (causes 'ai_press_narrative'): {len(press)}")


def dato_5_sobrecontratacion():
    """Corregir la sobre-contratación es solo parte de la ecuación.

    No se reproduce desde este dataset: la dotación sale de los filings (10-K/20-F), empresa por
    empresa. Con la misma ventana para todas las públicas, la sobre-contratación reciente no
    distingue claim vs no-claim; para 2026 la mayoría venía plana o achicándose. Ver
    auditoria-sobrecontratacion.md."""
    print("[5] Dotación desde filings (no desde este dataset) — ver auditoria-sobrecontratacion.md")


def dato_6_sin_cifra_45_9():
    """45 anuncios sin cifra; los 9 cierres totales están entre ellos."""
    nocifra = [e for e in D if not e.get("laid_off")]
    shut = [e for e in D if has(e, "shutdown")]
    shut_nc = [e for e in shut if not e.get("laid_off")]
    print(f"[6] sin cifra: {len(nocifra)} | cierres (causes 'shutdown'): {len(shut)} | "
          f"cierres sin cifra: {len(shut_nc)}")


def dato_7_concentracion():
    """Diez anuncios reúnen ~70% de las personas; el anuncio típico (mediana) es 200."""
    vals = sorted((e["laid_off"] for e in D if e.get("laid_off")), reverse=True)
    top10 = sum(vals[:10])
    print(f"[7] top-10 anuncios = {top10:,} = {100*top10/HEADS:.1f}% del total | "
          f"mediana = {statistics.median(vals):.0f} | n con cifra = {len(vals)}")


def dato_8_proporcion_mensual():
    """Proporción mensual, dos definiciones (ene-may): sustitución 9-26% vs cualquier-IA 27-53%."""
    AI_ANY = {"ai_substitution_claim", "ai_capex_reallocation", "ai_framing_vague",
              "ai_press_narrative", "ai_denied"}
    bm = collections.defaultdict(lambda: [0, 0, 0])  # [substitution, any-AI, total]
    for e in D:
        m = e["date"][:7]
        if m >= "2026-06":
            continue
        bm[m][2] += 1
        if has(e, "ai_substitution_claim"):
            bm[m][0] += 1
        if set(e.get("causes") or []) & AI_ANY:
            bm[m][1] += 1
    sub, any_ = [], []
    for m in sorted(bm):
        s, a, t = bm[m]
        sub.append(100 * s / t); any_.append(100 * a / t)
        print(f"[8] {m}: sustitución {s}/{t}={100*s/t:.0f}% | cualquier-IA {a}/{t}={100*a/t:.0f}% (n={t})")
    print(f"    sustitución: {min(sub):.0f}-{max(sub):.0f}% (sin dirección) | "
          f"cualquier-IA: {min(any_):.0f}-{max(any_):.0f}% (sube)")


if __name__ == "__main__":
    print(f"Ventana in-window: {len(D)} eventos | {HEADS:,} personas con cifra\n")
    for fn in (dato_1_casi_la_mitad, dato_2_oracle, dato_3_verdictos_27, dato_4_prensa_16,
               dato_5_sobrecontratacion, dato_6_sin_cifra_45_9, dato_7_concentracion,
               dato_8_proporcion_mensual):
        print(f"--- {fn.__doc__}")
        fn()
        print()
