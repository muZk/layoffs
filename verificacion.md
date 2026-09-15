# Verificación: "161 despidos, uno por uno"

Cada dato agregado del resumen sale de una consulta sobre el dataset abierto
([`2026-categorized.json`](2026-categorized.json)). Ventana: `date < "2026-07-01"`
→ 161 eventos, 108.089 personas con cifra. Acá está, para cada dato, la consulta
exacta y su resultado.

Estas consultas se calcularon a mano contra [`2026-categorized.json`](2026-categorized.json),
la fuente curada del dataset. No hay script que las corra: los números de abajo son el
resultado de aplicar cada consulta directamente sobre el JSON, y quedan descritos acá, dato
por dato.

Campos usados: `causes` (lista de causas por evento), `ai_mention` (cómo apareció la IA:
substitution / capex / framing / denied / none), `ai_link_basis` (quién hizo la afirmación
de IA), `ai_claim_verdict` (veredicto de la afirmación de sustitución), `stage` (etapa;
`Post-IPO` = cotiza en bolsa), `laid_off` (personas). El significado de cada campo está en
[`schema.md`](schema.md).

Corte público/privado: público = `stage == "Post-IPO"` (67 eventos); privado = etapa
privada conocida (71); los 23 de etapa `Unknown` se excluyen de ese corte.

---

## Dato 1

"El motivo más común es un no-motivo: la mayoría trae una sola causa, y suele ser vaga."

```python
single = [e for e in D if len(e["causes"]) == 1]                       # 125
cf = collections.Counter(c for e in D for c in e["causes"])            # frecuencia
```

→ 125 de 161 (78 %) tienen una sola causa etiquetada. Las dos causas más nombradas en todo
el dataset son genéricas y no dicen qué provocó el recorte: reestructuración sin especificar
(65, 40 %) y recorte de costos (42, 26 %). Entre las dos cubren casi dos de cada tres
menciones de causa.

Causas más nombradas (contando cada causa, sola o acompañada, sobre los 161):

| causa | eventos | % |
|---|---|---|
| reestructuración sin especificar | 65 | 40 % |
| recorte de costos | 42 | 26 % |
| reemplazo por IA (`ai_substitution_claim`) | 16 | 10 % |
| pivote de estrategia | 15 | 9 % |
| fusión / adquisición | 12 | 7 % |
| problemas financieros | 11 | 7 % |

---

## Dato 2

"De los 16 anuncios donde la empresa dice que la IA reemplaza personas, solo uno resiste
la revisión."

```python
subs = [e for e in D if "ai_substitution_claim" in e["causes"]]        # 16
vc   = collections.Counter(e["ai_claim_verdict"] for e in subs)
basis = collections.Counter(e["ai_link_basis"] for e in subs)          # 16 company_stated
```

→ 16 anuncios traen `ai_substitution_claim`, y en los 16 la afirmación la pone la propia
empresa (`ai_link_basis = company_stated`), ninguno sale solo de una nota de prensa. Sus
veredictos: 1 `plausible` (MercadoLibre, 116 personas, 0,1 % del total), 1
`contradicted_hard` (Block, 4.000 personas), 6 `contradicted_soft` y 8 `thin_evidence`. Las
16 empresas: Block, WiseTech, Snap, Coinbase, Playtika, Freshworks, Angi, ClickUp, Jumia,
Upwork, Kraken, MercadoLibre, ApnaMart, Stone, Firebolt y Snowflake. Los `thin_evidence` son
en general empresas chicas o privadas, sin datos públicos para contrastar el reclamo.

---

## Dato 3

"El embudo completo: 161 anuncios, 71 tocan la IA de alguna forma, 16 dicen reemplazo, uno
se sostiene."

```python
touched = [e for e in D if e["ai_mention"] != "none"]                  # 71
subs    = [e for e in D if "ai_substitution_claim" in e["causes"]]     # 16
holds   = [e for e in subs if e["ai_claim_verdict"] == "plausible"]    # 1
```

→ De los 161 anuncios, 71 mencionan la IA de alguna forma: como framing sin operar (46),
como reemplazo (16), como capex (5) o como negación explícita (4). De los 71, 16 dicen que
la IA reemplaza personas. De esos 16, uno se sostiene contra los hechos: MercadoLibre. El
resto se reparte entre contradicho (7, uno duro y seis suaves) y sin pruebas para confirmar
ni desmentir (8).

---

## Dato 4

"Culpar a la IA tiene dos caras: reemplazo (16) y gasto en capex (5). Oracle no es ninguna
de las dos por su propia voz."

```python
subs  = [e for e in D if "ai_substitution_claim"  in e["causes"]]      # 16 reemplazo
capex = [e for e in D if "ai_capex_reallocation"  in e["causes"]]      # 5 gasto
oracle = next(e for e in D if e["company"] == "Oracle")
```

→ Reemplazo ("la IA hace el trabajo"): 16. Recorte enmarcado como inversión en IA
(`ai_capex_reallocation`): 5, Meta, Cisco, Pinterest, ZoomInfo y GitLab, todas cotizan en
bolsa. Pero "invertir en IA" no significa lo mismo en cada una. Solo Meta ata el recorte a
infraestructura verificable (guía de capex récord 2026, US$125-145B, más el traslado de
~7.000 personas a equipos de IA). En el resto es una intención declarada sin cifra: Pinterest
habla de "roles y productos con IA", ZoomInfo y Cisco de reorientar el gasto hacia la IA, y
GitLab promete infraestructura después de haber dicho un mes antes que el mismo recorte "no
era una optimización por IA". El `cause_evidence` de cada evento registra la cita.

→ Oracle: 21.000 personas, 19 % del total (número interno del dataset, no viene de la
hoja de verificación). No lleva `ai_substitution_claim` en `causes`: su mención de IA
está clasificada como `ai_mention = framing` y `ai_claim_verdict = not_claimed`, porque la
única mención propia de IA aparece en una línea condicional del 10-K FY26 (Item 1A Risk
Factors + Note 7: "have resulted, and may continue to result, in reductions to our
workforce"), lenguaje de riesgo sin cifra atribuida, no una afirmación de que la IA causó
el recorte. Los correos de marzo hablaron de "a broader organizational change". Por eso
Oracle no cuenta como reemplazo por IA.

---

## Dato 5

"En los 90 anuncios donde nadie nombró la IA, buscamos igual si el recorte pudo ser IA."

```python
nosig = [e for e in D if e["ai_mention"] == "none"]                     # 90
conc  = [e for e in nosig if set(e["causes"]) &
         {"shutdown", "m_and_a", "financial_distress", "market_exit", "demand_collapse"}]
unk   = [e for e in nosig if e["causes"] == ["unknown"]]                # 10
```

→ 90 anuncios no traen ninguna señal de IA, ni de la empresa ni de la prensa: 25 % de las
personas despedidas. De ellos, un subconjunto tiene un motivo concreto y verificable con
hechos públicos (cierre, fusión, contrato perdido, caída de demanda) que no necesita la IA
para explicarse; en la mayoría del resto el motivo es vago (reestructuración o costos, como
en el [Dato 1](#dato-1)); 10 no dan motivo alguno.

Esto no prueba un negativo: ningún registro público descarta que un despido haya sido, en
silencio, por IA. Lo verificable es que en ninguno de los 90 aparece una señal de IA, ni
siquiera de la prensa. No hay un test positivo para una sustitución que nadie declaró ni
reportó.

---

## Dato 6

"Cuatro empresas negaron la IA de frente. De los 16 que dicen que la IA reemplaza personas,
ninguno viene solo de la prensa."

```python
denied = [e for e in D if e["ai_mention"] == "denied"]                 # 4
subs_press = [e for e in D if "ai_substitution_claim" in e["causes"]
              and e["ai_link_basis"] == "press_inferred"]              # 0
```

→ Negaciones explícitas (`ai_mention = denied`): 4. Amazon (16.000), Intuit (3.000),
Autodesk (1.000) y Epic Games (s/d).

→ De los 16 reclamos de reemplazo por IA, el origen de la afirmación es siempre la propia
empresa: ninguno lo puso solo la prensa (ver [Dato 2](#dato-2)).

(La numeración de los datos sigue el orden de los hallazgos; el hallazgo 5, Block, y el 7,
sobre-contratación, se documentan en sus propias fuentes: el evento de Block trae su
`source_url`, y la sobre-contratación en [auditoria-sobrecontratacion.md](auditoria-sobrecontratacion.md).)

---

## Dato 8

"El peso humano está casi todo en empresas públicas; las causas se separan por tipo de
empresa."

```python
PUB  = [e for e in D if e["stage"] == "Post-IPO"]                      # 67
PRIV = [e for e in D if e["stage"] not in ("Post-IPO", "Unknown")]    # 71
```

→ Público: 67 anuncios, 94.873 personas, 88 % del total. Privado: 71 anuncios, 9.864, 9 %
(el resto está en los 23 de etapa desconocida). Mediana por anuncio: público 450, privado
110.

Sesgo de causas (en qué % de los anuncios de cada grupo aparece la causa):

| causa | públicas | privadas |
|---|---|---|
| recorte de costos | 36 % | 18 % |
| gasto en IA (`ai_capex_reallocation`) | 7 % | 0 % |
| reemplazo por IA (`ai_substitution_claim`) | 18 % | 4 % |
| cierre total (`shutdown`) | 0 % | 11 % |
| pivote de estrategia | 1 % | 17 % |
| mención de IA sin causa operativa (`ai_mention = framing`) | 22 % | 35 % |
| fusión / adquisición | 4 % | 10 % |

Concentración: 45 de los 161 anuncios no traen cifra (incluidos los 9 cierres totales); de
los 116 con cifra, los diez más grandes reúnen 75.460 personas, 70 % del total.

---

Los datos por empresa (MercadoLibre, Oracle, Block, Amazon, Intuit, Meta, etc.) no se listan acá:
cada evento trae su `source_url` en el dataset, y el resumen los enlaza uno por uno a su fuente
original.
