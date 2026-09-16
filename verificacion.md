# Verificación: "161 despidos, uno por uno"

Cada dato agregado del resumen sale de una consulta sobre el dataset abierto
([`2026-categorized.json`](2026-categorized.json)). Ventana: `date < "2026-07-01"`
→ 161 eventos, 108.089 personas con cifra. Acá está, para cada dato, la consulta
exacta y su resultado.

Estas consultas se calcularon a mano contra [`2026-categorized.json`](2026-categorized.json),
la fuente curada del dataset. No hay script que las corra: los números de abajo son el
resultado de aplicar cada consulta directamente sobre el JSON, y quedan descritos acá, dato
por dato.

Campos usados: `causes` (lista de causas por evento), `papel_ia` (qué papel juega la IA en
el anuncio: ninguna / vaga / eficiencia / disrupcion / reemplazo / inversion), `fuente_ia`
(quién vinculó la IA al recorte: empresa / prensa / desconocida / ninguna), `nego_ia` (la
empresa negó la IA), `es_causa_ia` (la IA es causa real), `ai_claim_verdict` (veredicto de
la afirmación de sustitución), `stage` (etapa; `Post-IPO` = cotiza en bolsa), `laid_off`
(personas). El campo `ai_mention` sigue en el dataset pero `papel_ia` lo reemplaza como
lente principal de IA (ver la reconciliación de septiembre de 2026 en `schema.md`). El
significado de cada campo está en [`schema.md`](schema.md).

Corte público/privado: público = `stage == "Post-IPO"` (67 eventos); privado = etapa
privada conocida (71); los 23 de etapa `Unknown` se excluyen de ese corte.

---

## Dato 1

"El motivo más común es un no-motivo: la mayoría trae una sola causa, y suele ser vaga."

```python
single = [e for e in D if len(e["causes"]) == 1]                       # 123
cf = collections.Counter(c for e in D for c in e["causes"])            # frecuencia
```

→ 123 de 161 (76 %) tienen una sola causa etiquetada. Las dos causas más nombradas en todo
el dataset son genéricas y no dicen qué provocó el recorte: reestructuración sin especificar
(69, 43 %) y recorte de costos (42, 26 %). Entre las dos cubren más de la mitad de las
menciones de causa (111 de 210).

Causas más nombradas (contando cada causa, sola o acompañada, sobre los 161):

| causa | eventos | % |
|---|---|---|
| reestructuración sin especificar | 69 | 43 % |
| recorte de costos | 42 | 26 % |
| pivote de estrategia | 15 | 9 % |
| fusión / adquisición | 12 | 7 % |
| problemas financieros | 11 | 7 % |
| reemplazo por IA (`ai_substitution_claim`) | 6 | 4 % |

---

## Dato 2

"De los 6 anuncios donde la empresa dice que la IA reemplaza personas, solo uno resiste
la revisión."

```python
subs = [e for e in D if "ai_substitution_claim" in e["causes"]]        # 6
vc   = collections.Counter(e["ai_claim_verdict"] for e in subs)
src  = collections.Counter(e["fuente_ia"] for e in subs)               # 6 empresa
```

→ 6 anuncios traen `ai_substitution_claim`, y en los 6 la afirmación la pone la propia
empresa (`fuente_ia = empresa`; 4 por canal formal, 2 por canal informal: Angi y Snowflake),
ninguno sale solo de una nota de prensa. Sus veredictos: 1 `plausible` (MercadoLibre, 116
personas, 0,1 % del total), 2 `contradicted_soft` (WiseTech, Kraken) y 3 `thin_evidence`
(Angi, Snowflake, Freshworks). Las 6 empresas: Angi, MercadoLibre, WiseTech, Snowflake,
Freshworks y Kraken. Los `thin_evidence` son empresas sin datos públicos para contrastar el
reclamo, o con un reclamo sin cifra.

Hasta septiembre de 2026 este tag cubría 16 anuncios. La reconciliación con el eje
`papel_ia` sacó a los 10 que solo hablaban de equipos más chicos o de eficiencia con IA sin
decir que la IA reemplazó a nadie (Block, Snap, Coinbase, Upwork, Playtika, Firebolt,
ApnaMart, Jumia, ClickUp, Stone); hoy están en `papel_ia = eficiencia` o `vaga` y llevan
solo su causa mundana. Block (4.000 personas) conserva `rehiring_same_roles` y su veredicto
`contradicted_hard` queda en el dataset como registro de esa revisión.

---

## Dato 3

"El embudo completo: 161 anuncios, 70 le dan algún papel a la IA, 16 la tienen como causa
real, 6 dicen reemplazo, uno se sostiene."

```python
touched = [e for e in D if e["papel_ia"] != "ninguna"]                 # 70
causa   = [e for e in D if e["es_causa_ia"]]                           # 16
subs    = [e for e in D if "ai_substitution_claim" in e["causes"]]     # 6
holds   = [e for e in subs if e["ai_claim_verdict"] == "plausible"]    # 1
```

→ De los 161 anuncios, en 70 la IA juega algún papel (`papel_ia`): mención vaga (28),
eficiencia o equipos más chicos (19), disrupción del mercado o pivote de producto (10),
reemplazo (8) o inversión en infraestructura de IA (5). En 16 la IA es una causa real
(`es_causa_ia`): los 6 donde la empresa dice que la IA reemplaza personas, los 4 donde el
recorte financia infraestructura de IA, y los 6 donde la IA dejó obsoleto el producto
(casi todos cierres). De los 6 reclamos de reemplazo, uno se sostiene contra los hechos:
MercadoLibre. El resto se reparte entre contradicho (2, suaves) y sin pruebas para
confirmar ni desmentir (3).

---

## Dato 4

"Culpar a la IA tiene dos caras: reemplazo (6) y gasto en capex (4). Oracle no es ninguna
de las dos por su propia voz."

```python
subs  = [e for e in D if "ai_substitution_claim"  in e["causes"]]      # 6 reemplazo
capex = [e for e in D if "ai_capex_reallocation"  in e["causes"]]      # 4 gasto
oracle = next(e for e in D if e["company"] == "Oracle")
```

→ Reemplazo ("la IA hace el trabajo"): 6. Recorte enmarcado como inversión en IA
(`ai_capex_reallocation`): 4, Meta, Pinterest, ZoomInfo y GitLab, todas cotizan en bolsa.
Pero "invertir en IA" no significa lo mismo en cada una. Solo Meta ata el recorte a
infraestructura verificable (guía de capex récord 2026, US$125-145B, más el traslado de
~7.000 personas a equipos de IA). En el resto es una intención declarada sin cifra: Pinterest
habla de "roles y productos con IA", ZoomInfo de reorientar el gasto hacia la IA, y GitLab
promete infraestructura después de haber dicho un mes antes que el mismo recorte "no era
una optimización por IA". Cisco llevaba este tag hasta septiembre de 2026; su mención ("áreas
de mayor demanda en la era de la IA") es de pasada y hoy está en `papel_ia = vaga` con
reestructuración sin especificar como única causa. El `cause_evidence` de cada evento
registra la cita.

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

"En los 84 anuncios donde nadie nombró la IA, buscamos igual si el recorte pudo ser IA."

```python
nosig = [e for e in D if e["fuente_ia"] == "ninguna"]                   # 84
conc  = [e for e in nosig if set(e["causes"]) &
         {"shutdown", "m_and_a", "financial_distress", "market_exit", "demand_collapse"}]  # 22
unk   = [e for e in nosig if e["causes"] == ["unknown"]]                # 7
```

→ 84 anuncios no traen ninguna señal de IA, ni de la empresa ni de la prensa: 13 % de las
personas despedidas. De ellos, 22 tienen un motivo concreto y verificable con hechos
públicos (cierre, fusión, contrato perdido, caída de demanda) que no necesita la IA para
explicarse; en la mayoría del resto el motivo es vago (reestructuración o costos, como en el
[Dato 1](#dato-1)); 7 no dan motivo alguno.

Si el corte es "la IA no opera en el anuncio" en vez de "nadie la nombró", el grupo sube a
91 (`papel_ia = ninguna`, 40 % de las personas): entran Amazon, Dell, LinkedIn y Epic
Games, donde la prensa mencionó la IA sin que fuera un mecanismo, y tres eventos con fuente
de IA desconocida.

Esto no prueba un negativo: ningún registro público descarta que un despido haya sido, en
silencio, por IA. Lo verificable es que en ninguno de los 84 aparece una señal de IA, ni
siquiera de la prensa. No hay un test positivo para una sustitución que nadie declaró ni
reportó.

---

## Dato 6

"Cuatro empresas negaron la IA de frente. De los 6 que dicen que la IA reemplaza personas,
ninguno viene solo de la prensa."

```python
denied = [e for e in D if e["nego_ia"]]                                # 4
subs_press = [e for e in D if "ai_substitution_claim" in e["causes"]
              and e["fuente_ia"] != "empresa"]                         # 0
reemplazo = [e for e in D if e["papel_ia"] == "reemplazo"]             # 8
```

→ Negaciones explícitas (`nego_ia`): 4. Amazon (16.000), Intuit (3.000), Epic Games (s/d)
y LinkedIn (875). El campo anterior, `ai_mention = denied`, también suma 4 pero con Autodesk
(1.000, por su correo presentado a la SEC) en lugar de LinkedIn; los dos campos coinciden en
Amazon, Intuit y Epic Games.

→ De los 6 reclamos de reemplazo por IA, el origen de la afirmación es siempre la propia
empresa: ninguno lo puso solo la prensa (ver [Dato 2](#dato-2)). El eje `papel_ia` registra
2 anuncios más con lectura de reemplazo que no cuentan como reclamo de la empresa:
DraftKings (lo dijo la prensa) y Zendesk (memo interno sin fuente pública).

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
| gasto en IA (`ai_capex_reallocation`) | 6 % | 0 % |
| reemplazo por IA (`ai_substitution_claim`) | 7 % | 0 % |
| cierre total (`shutdown`) | 0 % | 11 % |
| pivote de estrategia | 1 % | 17 % |
| mención vaga de la IA (`papel_ia = vaga`) | 24 % | 11 % |
| producto o mercado disrumpido por la IA (`papel_ia = disrupcion`) | 1 % | 13 % |
| fusión / adquisición | 4 % | 10 % |

Concentración: 45 de los 161 anuncios no traen cifra (incluidos los 9 cierres totales); de
los 116 con cifra, los diez más grandes reúnen 75.460 personas, 70 % del total.

---

Los datos por empresa (MercadoLibre, Oracle, Block, Amazon, Intuit, Meta, etc.) no se listan acá:
cada evento trae su `source_url` en el dataset, y el resumen los enlaza uno por uno a su fuente
original.
