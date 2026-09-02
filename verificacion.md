# Verificación — "161 despidos, uno por uno"

Cada dato agregado del resumen sale de una consulta sobre el dataset abierto
([`2026-categorized.json`](2026-categorized.json)). Ventana: `date < "2026-07-01"`
→ **161 eventos, 108.089 personas con cifra**. Acá está, para cada dato, la consulta
exacta y su resultado.

Reproducir todo de una vez: [`python3 verificacion.py`](verificacion.py). Los números de
abajo son la salida de ese script sobre la versión actual del dataset.

Campos usados: `causes` (lista de causas por evento), `ai_link` y `ai_link_basis` (mecanismo
y quién hizo la afirmación de IA), `ai_claim_verdict` (veredicto de la afirmación de
sustitución), `hire_overcorrection` (auditoría de sobrecontratación contra reportes a la SEC),
`laid_off` (personas). El significado de cada campo está en [`schema.md`](schema.md).

---

## Dato 1

**"Casi la mitad de las personas despedidas trabajaba en empresas que dieron a la IA como parte del motivo del recorte."**

Empresas donde la propia empresa invocó la IA como motivo, sea como reemplazo (`direct_substitution`)
o como inversión (`capex_funding`):

```python
comp_ai = [e for e in D if e["ai_link_basis"] in ("company_stated", "company_informal")
           and e["ai_link"] in ("direct_substitution", "capex_funding")]
heads = sum(e["laid_off"] for e in comp_ai if e["laid_off"])
```

→ **32 eventos, 53.497 personas = 49,5 % de 108.089.**

El subconjunto que dijo específicamente "la IA hace el trabajo" (solo sustitución) son
**27 eventos = 35,5 %**; ver [Dato 3](#dato-3). Los eventos de inversión en IA (Meta, Cisco,
Pinterest, Atlassian, ZoomInfo, Amentum) se cuentan en el 49,5 % pero se tratan aparte en el
hallazgo 7, porque ahí la IA no reemplaza a nadie.

---

## Dato 2

**"Oracle despidió a 21.000 personas, el 19 % del total del semestre. En marzo lo describió como un cambio organizacional; su única mención a la IA llegó en el reporte anual."**

```python
o = next(e for e in D if e["company"] == "Oracle")
# o["laid_off"] = 21000  ->  21000 / 108089
```

→ **21.000 personas = 19,4 % del total.** `causes = ['ai_substitution_claim', 'cost_cutting', 'm_and_a']`,
`ai_claim_verdict = 'thin_evidence'`.

Del campo `reason` del evento: los correos de despido de marzo hablaron de *"a broader organizational
change"*; la frase de IA aparece recién en el 10-K FY26, en Item 1A Risk Factors + Note 7, en
condicional (*"have resulted, and may continue to result, in reductions to our workforce"*),
sin una cifra de personas atribuida. La fuente primaria de esa frase es el 10-K en SEC EDGAR.

---

## Dato 3

**"De las 27 empresas que dijeron 'la IA hace ese trabajo', 3 se sostienen, 11 se contradicen y 13 no se pueden verificar."**

```python
subs = [e for e in D if "ai_substitution_claim" in e["causes"]]           # 27
vc = collections.Counter(e["ai_claim_verdict"] for e in subs)
hold   = vc["plausible"]                                                   # se sostienen
contra = vc["contradicted_soft"] + vc["contradicted_hard"]                # se contradicen
thin   = vc["thin_evidence"]                                              # sin verificar
```

→ **27 claims → 3 se sostienen (`plausible`) · 11 se contradicen (7 `soft` + 4 `hard`) · 13 sin verificar (`thin_evidence`).**
Suma: 3 + 11 + 13 = 27.

---

## Dato 4

**"En 16 de los 161 casos, el vínculo con la IA lo puso la prensa, no la empresa."**

```python
press = [e for e in D if "ai_press_narrative" in e["causes"]]
```

→ **16 eventos.** Son los casos donde el ángulo de IA proviene de la cobertura, mientras la
empresa dio otro motivo o ninguno.

---

## Dato 5

**"De las 30 empresas grandes que pudimos revisar contra sus reportes, 24 venían de contratar de más."**

`hire_overcorrection` solo está poblado para las empresas que se pudieron auditar contra sus
reportes de dotación a la SEC (dos años antes del recorte):

```python
audited = [e for e in D if e["hire_overcorrection"] is not None]          # 30
over    = [e for e in audited if e["hire_overcorrection"] is True]        # 24
```

→ **30 auditadas, 24 con sobrecontratación (crecimiento ≥ 15 % antes del recorte).** Es descriptivo
de las grandes que se pudieron revisar, no de todas, y no establece causa (ver hallazgo 6).

---

## Dato 6

**"45 de los 161 anuncios no traen cifra, y los 9 cierres totales están entre ellos."**

```python
nocifra = [e for e in D if not e["laid_off"]]                             # 45
shut    = [e for e in D if "shutdown" in e["causes"]]                     # 9
shut_sin_cifra = [e for e in shut if not e["laid_off"]]                   # 9
```

→ **45 sin cifra · 9 cierres · los 9 cierres están dentro de los 45 sin cifra.**

---

## Dato 7

**"Diez anuncios reúnen el 70 % de las personas, y el anuncio típico es de 200."**

```python
vals  = sorted((e["laid_off"] for e in D if e["laid_off"]), reverse=True)  # 116 con cifra
top10 = sum(vals[:10])
mediana = statistics.median(vals)
```

→ **top-10 = 75.460 personas = 69,8 % del total · mediana = 200** (sobre 116 anuncios con cifra).

---

## Dato 8

**"Entre enero y mayo, la proporción de empresas que atribuye el recorte a la IA oscila entre 9 % y 26 % mes a mes."**

Proporción mensual de eventos que dieron la IA como reemplazo (`ai_substitution_claim`), enero a
mayo (junio se agregó a mano, se excluye):

```python
for m in ("2026-01", ..., "2026-05"):
    mes  = [e for e in D if e["date"][:7] == m]
    ai   = [e for e in mes if "ai_substitution_claim" in e["causes"]]
    # len(ai) / len(mes)
```

→ **ene 10 % · feb 22 % · mar 16 % · abr 9 % · may 26 %.** Rango 9 %–26 %, sin dirección clara.

---

*Los datos por empresa (MercadoLibre, Oracle, Block, Amazon, Intuit, Meta, etc.) no se listan acá:
cada evento trae su `source_url` en el dataset, y el resumen los enlaza uno por uno a su fuente
original.*
