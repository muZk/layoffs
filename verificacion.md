# Verificación — "161 despidos, uno por uno"

Cada dato agregado del resumen sale de una consulta sobre el dataset abierto
([`2026-categorized.json`](2026-categorized.json)). Ventana: `date < "2026-07-01"`
→ **161 eventos, 108.089 personas con cifra**. Acá está, para cada dato, la consulta
exacta y su resultado.

Reproducir todo de una vez: [`python3 verificacion.py`](verificacion.py). Los números de
abajo son la salida de ese script sobre la versión actual del dataset.

Campos usados: `causes` (lista de causas por evento), `ai_link` y `ai_link_basis` (mecanismo
y quién hizo la afirmación de IA), `ai_claim_verdict` (veredicto de la afirmación de
sustitución), `stage` (etapa; `Post-IPO` = cotiza en bolsa), `laid_off` (personas). El
significado de cada campo está en [`schema.md`](schema.md).

Corte público/privado: **público** = `stage == "Post-IPO"` (67 eventos); **privado** =
etapa privada conocida (71); los 23 de etapa `Unknown` se excluyen de ese corte.

---

## Dato 1

**"El motivo más común es un no-motivo: la mayoría trae una sola causa, y suele ser vaga."**

```python
single = [e for e in D if len(e["causes"]) == 1]                       # 94
vague  = [e for e in single if e["causes"][0] in
          ("restructuring_unspecified", "cost_cutting", "unknown")]    # 52
cf = collections.Counter(c for e in D for c in e["causes"])            # frecuencia
```

→ **94 de 161 (58 %) tienen una sola causa etiquetada.** De esos 94, **52** son un motivo
genérico o ninguno (25 "reestructuración sin especificar" + 17 "recorte de costos" + 10 "sin
causa identificable"), o sea uno de cada tres de los 161.

Causas más nombradas (contando cada causa, sola o acompañada, sobre los 161):

| causa | eventos | % |
|---|---|---|
| reestructuración sin especificar | 56 | 35 % |
| recorte de costos | 44 | 27 % |
| la empresa dice que la IA hace el trabajo (`ai_substitution_claim`) | 26 | 16 % |
| la empresa menciona la IA sin atribuirle nada (`ai_framing_vague`) | 19 | 12 % |
| el vínculo con la IA lo pone la prensa (`ai_press_narrative`) | 16 | 10 % |
| fusión / adquisición | 12 | 7 % |

---

## Dato 2

**"De los 161, MercadoLibre es el único caso de causa única = IA que resiste la revisión."**

```python
ai_only = [e for e in D if e["causes"] == ["ai_substitution_claim"]]   # 10
plaus   = [e for e in ai_only if e["ai_claim_verdict"] == "plausible"] # 1
```

→ **10 eventos tienen la IA como única causa etiquetada.** Sus veredictos: 1 `plausible`
(MercadoLibre, 116 personas = 0,1 %), 1 `contradicted_hard` (Livspace, 1.000, recontrató) y
8 `thin_evidence` (Angi, Firebolt, Monte Carlo, Pendo, Pentera, ApnaMart, DeepL, Dune) — en
general empresas chicas o privadas sin datos públicos para contrastar. **MercadoLibre es el
único de causa única, verificable y donde la causa es la IA reemplazando trabajo.**

---

## Dato 3

**"De las 26 que dijeron 'la IA hace ese trabajo', 16 nombraron otra causa; 3 se sostienen, 11 se contradicen, 12 no se pueden verificar."**

```python
subs  = [e for e in D if "ai_substitution_claim" in e["causes"]]       # 26
multi = [e for e in subs if len(e["causes"]) > 1]                      # 16
co    = collections.Counter(c for e in subs for c in e["causes"]
                            if c != "ai_substitution_claim")
vc    = collections.Counter(e["ai_claim_verdict"] for e in subs)
```

→ **26 reclamos → 16 (62 %) traen otra causa en el mismo anuncio.** Lo que co-ocurre con la
IA: recorte de costos (9), problemas financieros (6), reestructuración (5), caída de demanda
(4); algunos anuncios traen más de una, por eso la suma supera 16.

→ Verdicto de los 26: **3 se sostienen** (`plausible`: MercadoLibre, Coinbase, Wix) · **11 se
contradicen** (7 `soft` + 4 `hard`) · **12 sin verificar** (`thin_evidence`). "Sin verificar"
no es falso: es que no hay con qué comprobarlo ni desmentirlo (en general, empresas privadas o
chicas).

---

## Dato 4

**"Culpar a la IA tiene dos caras: reemplazo (26) y gasto/capex (6). Oracle no es ninguna de las dos por su propia voz."**

```python
subs  = [e for e in D if "ai_substitution_claim"  in e["causes"]]      # 26 reemplazo
capex = [e for e in D if "ai_capex_reallocation"  in e["causes"]]      # 6 gasto
oracle = next(e for e in D if e["company"] == "Oracle")
```

→ **Reemplazo ("la IA hace el trabajo"): 26.** **Recorte enmarcado como inversión en IA: 6** —
Meta, Cisco, Pinterest, Atlassian, ZoomInfo y GitLab, todas cotizan en bolsa. La etiqueta interna es
`ai_capex_reallocation`, pero "invertir en IA" no es lo mismo en cada una: solo **Meta** ata el
recorte a infraestructura verificable (guía de capex récord 2026, US$125-145B, más el traslado de
~7.000 personas a equipos de IA). En el resto es una intención declarada sin cifra: Pinterest habla
de "roles y productos con IA", Atlassian de "autofinanciar" la inversión *sin compromiso de capex*,
ZoomInfo/Cisco de reorientar el gasto "hacia la IA", y GitLab promete infraestructura tras haber
dicho un mes antes que el mismo recorte "no era una optimización por IA". El `cause_evidence` de cada
evento registra la cita.

→ **Oracle:** 21.000 personas = 19 % del total. `causes = ['ai_substitution_claim',
'cost_cutting', 'm_and_a']`, `ai_claim_verdict = 'thin_evidence'`. Los correos de marzo
hablaron de *"a broader organizational change"*; la única mención propia de la IA es una línea
condicional en el 10-K FY26 (Item 1A Risk Factors + Note 7: *"have resulted, and may continue
to result, in reductions to our workforce"*), sin cifra atribuida. Por eso su reclamo cae en
`thin_evidence` y no se cuenta como reemplazo real.

---

## Dato 5

**"En los 91 anuncios donde nadie nombró la IA, buscamos igual si el recorte pudo ser IA."**

```python
AI = {"ai_substitution_claim", "ai_capex_reallocation", "ai_framing_vague",
      "ai_press_narrative", "ai_denied"}
nosig = [e for e in D if not (set(e["causes"]) & AI)]                   # 91
conc  = [e for e in nosig if set(e["causes"]) &
         {"shutdown", "m_and_a", "financial_distress", "market_exit", "demand_collapse"}]  # 22
unk   = [e for e in nosig if e["causes"] == ["unknown"]]                # 10
```

→ **91 anuncios sin ninguna señal de IA** (ni de la empresa ni de la prensa), **28.467 personas =
26 %** del total. De ellos: **22** tienen un motivo concreto y verificable con hechos públicos
(cierre, fusión, contrato perdido, caída de demanda) que no necesita la IA para explicarse; en la
mayoría del resto el motivo es vago (reestructuración o costos, como en el [Dato 1](#dato-1));
**10** no dan motivo alguno.

Esto no prueba un negativo: ningún registro público descarta que un despido haya sido, en
silencio, por IA. Lo verificable es que en ninguno de los 91 aparece una señal de IA, ni siquiera
de la prensa. No hay un test positivo para una sustitución que nadie declaró ni reportó.

---

## Dato 6

**"Tres empresas negaron la IA de frente; en 16 el vínculo lo puso solo la prensa."**

```python
denied = [e for e in D if "ai_denied" in e["causes"]]                  # 3
press  = [e for e in D if "ai_press_narrative" in e["causes"]]         # 16
press_cifra = [e["laid_off"] for e in press if e["laid_off"]]          # 11 con cifra
```

→ **Negaciones explícitas (`ai_denied`): 3** — Autodesk (1.000), Amazon (16.000), Intuit
(3.000). **Vínculo aportado solo por la prensa (`ai_press_narrative`): 16;** de esos, 11 traen
cifra y suman **1.945 personas** (menos de 2.000).

(La numeración de los datos sigue el orden de los hallazgos; el hallazgo 5, Block, y el 7,
sobre-contratación, se documentan en sus propias fuentes: el evento de Block trae su
`source_url`, y la sobre-contratación en [auditoria-sobrecontratacion.md](auditoria-sobrecontratacion.md).)

---

## Dato 8

**"El peso humano está casi todo en empresas públicas; las causas se separan por tipo de empresa."**

```python
PUB  = [e for e in D if e["stage"] == "Post-IPO"]                      # 67
PRIV = [e for e in D if e["stage"] not in ("Post-IPO", "Unknown")]    # 71
```

→ **Público: 67 anuncios, 94.873 personas = 88 % del total.** Privado: 71 anuncios, 9.864 = 9 %
(el resto está en los 23 de etapa desconocida). **Mediana por anuncio: público 450, privado
110.**

Sesgo de causas (en qué % de los anuncios de cada grupo aparece la causa):

| causa | públicas | privadas |
|---|---|---|
| recorte de costos | 39 % | 18 % |
| gasto en IA (`ai_capex_reallocation`) | 9 % | 0 % |
| la IA hace el trabajo | 21 % | 13 % |
| cierre total (`shutdown`) | 0 % | 11 % |
| pivote de estrategia | 1 % | 10 % |
| mención vaga de la IA | 6 % | 18 % |
| fusión / adquisición | 4 % | 10 % |

Concentración: **45 de los 161 anuncios no traen cifra** (incluidos los 9 cierres totales); de
los 116 con cifra, **los diez más grandes reúnen 75.460 personas = 70 % del total.**

---

*Los datos por empresa (MercadoLibre, Oracle, Block, Amazon, Intuit, Meta, etc.) no se listan acá:
cada evento trae su `source_url` en el dataset, y el resumen los enlaza uno por uno a su fuente
original.*
