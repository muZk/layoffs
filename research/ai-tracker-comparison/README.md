# Nuestro dataset frente a Layoffs.fyi

**Usamos su clasificación de IA como punto de partida.** Conservamos los vínculos que registra Layoffs.fyi y añadimos los que encontramos en otras fuentes. Una diferencia requiere una razón documentada: otra ronda, un alcance distinto, una corrección o información posterior sobre el mismo anuncio. No poder recuperar una noticia no basta para descartar su clasificación.

Comparamos el [AI Layoffs Tracker](https://layoffs.fyi/ai-layoffs/), consultado el 28 de septiembre de 2026, con nuestros anuncios de enero–junio. El tracker etiqueta **95 de 231 eventos con IA (41,1%)**; nuestra colección contiene **108 de 228 (47,4%)**. Los universos no son idénticos.

| Resultado del cruce | Registros |
|---|---:|
| Ambos registramos una razón de IA | 91 |
| Solo el tracker registra IA, dentro de nuestra población | 1 |
| Solo nuestro análisis registra IA | 17 |
| Medidas de período del tracker excluidas de nuestros anuncios | 3 |

**La procedencia importa.** En 11 anuncios conservamos la etiqueta de IA del tracker sin corroborar por separado el mecanismo que describe. Se cuentan como vínculos generales atribuidos al tracker: no como sustitución demostrada ni como declaraciones de la empresa. En otros 8 casos, una fuente adicional o el contexto del plan permitió completar nuestra lectura anterior.

- **LinkedIn:** una fuente anónima niega que el recorte busque reemplazar puestos por IA. Otra cobertura de las comunicaciones internas del mismo anuncio describe cambios del trabajo de ingeniería en un entorno de desarrollo con IA. Conservamos ambas atribuciones: rediseñar el trabajo y reemplazar puestos no son la misma afirmación. [Cobertura posterior de ET](https://hr.economictimes.indiatimes.com/amp/news/workplace-4-0/talent-management/linkedin-cuts-350-jobs-in-india-amid-global-restructuring/131303309).
- **Verily:** mantenemos una diferencia de alcance. El tracker describe el cierre del programa de dispositivos, anunciado en agosto de 2025; nuestro registro corresponde al aviso de 58 puestos de junio de 2026. No trasladamos automáticamente la explicación de una ronda a otra. Esto no demuestra ausencia de IA en el recorte posterior. [Noticia del cierre de 2025](https://techcrunch.com/2025/08/26/verily-is-closing-its-medical-device-program-as-alphabet-shifts-more-resources-to-ai/).
- **Los 17 anuncios adicionales:** conservamos sus fuentes y atribuciones aunque no aparezcan en el listado de IA del tracker. Su ausencia no demuestra que Layoffs.fyi los haya investigado y descartado.
- **Oracle, Dell y Multiverse:** las tres entradas excluidas describen variaciones de plantilla o salidas de un período. Se conservan en la base, pero no cuentan como tres anuncios nuevos.

El gráfico de **empleados** del tracker cuenta **90.277 de 109.017 (82,8%)** en eventos etiquetados con IA durante el semestre. Pondera el tamaño de los eventos: no es un porcentaje de anuncios ni una estimación de cuántos puestos se deben a cada motivo.

[Reproducir el cruce y revisar la procedencia en el notebook](../../notebooks/explorar_despidos.html#comparacion-tracker) · [Descargar registros y decisiones](comparison.csv).

## Diferencias, caso por caso

Las fechas siguientes son las de los registros de nuestra colección; no necesariamente el día efectivo de las salidas. «Solo nosotros» significa ausente del **listado de IA del snapshot**, no ausente de todo Layoffs.fyi ni investigado y descartado por sus autores. Tampoco conocemos por qué no lo incluyeron: aquí explicamos por qué sí lo incluimos nosotros.

### Los 17 anuncios que añadimos al listado de IA

| Anuncio | ID | Por qué registramos IA | Quién lo atribuye y evidencia |
|---|---|---|---|
| Hailo · 2026-01-08 | `layoff-2026-004` | La empresa vincula el ajuste con reasignar inversión hacia robótica y Physical AI. | Empresa · [fuente](https://www.calcalistech.com/ctechnews/article/hyzk11etvwx) |
| Playtika · 2026-01-14 | `layoff-2026-013` | El CEO relaciona la reorganización con equipos menores apoyados en IA y automatización. | Empresa · [fuente](https://www.calcalistech.com/ctechnews/article/bkl6xzhswe) |
| Shopify · 2026-01-22 | `layoff-2026-019` | La cobertura vincula el recorte en alianzas con el giro hacia comercio con agentes de IA. | Prensa · [fuente](https://betakit.com/shopify-makes-more-job-cuts-this-time-targeting-partnerships-division/) |
| Gloo · 2026-01-29 | `layoff-2026-027` | La carta a inversionistas vincula reducciones de plantilla con eficiencias operativas mediante IA. | Empresa · [fuente](https://investors.gloo.com/static-files/6a6cee16-3074-4288-83a4-ce6487c4267f) |
| C3.ai · 2026-02-25 | `layoff-2026-052` | El CEO atribuye parte del recorte a productividad con IA, junto al programa de reducción de costos. | Empresa · [fuente](https://www.cio.com/article/4138095/c3-ai-slashes-26-of-its-workforce-ceo-attributes-the-move-in-part-to-ai-efficiency.html) |
| Digg · 2026-03-13 | `layoff-2026-068` | El fundador conecta los bots de IA con la inviabilidad del servicio que se cierra y rediseña. | Empresa · [fuente](https://techcrunch.com/2026/03/13/digg-lays-off-staff-and-shuts-down-app-as-company-retools/) |
| Stone · 2026-03-13 | `layoff-2026-070` | Una fuente anónima citada por la prensa atribuye parte de la decisión al avance de iniciativas de IA; no concreta el mecanismo. | Prensa · [fuente](https://jovempan.com.br/economia/macroeconomia/stone-faz-demissao-em-massa-e-desliga-cerca-de-400-funcionarios/) |
| Zendesk · 2026-03-24 | `layoff-2026-079` | La respuesta empresarial vincula la reorganización y el cierre con reasignar recursos a servicios habilitados por IA. | Empresa · [fuente](https://startit.rs/usred-pojacanog-fokusa-na-ai-zendesk-krajem-nedelje-gasi-svoju-kancelariju-u-srbiji-gde-imaju-60-zaposlenih/) |
| Oracle · 2026-03-31 | `layoff-2026-086` | La cobertura contemporánea vincula el plan de recortes de marzo con financiar infraestructura de IA; conservamos el alcance de plan y la inferencia de correspondencia con la ronda. | Prensa · [fuente](https://www.investing.com/news/stock-market-news/oracle-plans-thousands-of-job-cuts-as-data-center-costs-rise-bloomberg-news-reports-4544997) |
| Yupp · 2026-03-31 | `layoff-2026-088` | Los fundadores relacionan el cierre con avances de IA que reducen la utilidad del producto. | Empresa · [fuente](https://techcrunch.com/2026/03/31/yupp-ai-shuts-down-33m-a16z-crypto-chris-dixon/) |
| PayPal · 2026-05-05 | `layoff-2026-126` | El plan empresarial combina ahorro y rediseño de procesos con IA; no reparte los puestos entre cada componente. | Empresa · [fuente](https://s205.q4cdn.com/875401827/files/doc_financials/2026/ar/2026-Annual-Meeting-Posted-Q-A-FINAL.pdf) |
| ApnaMart · 2026-05-06 | `layoff-2026-127` | La empresa atribuye algunas redundancias a automatización con IA, además del traslado del trabajo. | Empresa · [fuente](https://entrackr.com/news/apna-mart-lays-off-10-of-workforce-shifts-base-from-bengaluru-to-gurugram-11805807) |
| AI21 Labs · 2026-05-18 | `layoff-2026-154` | La empresa explica un cambio de estrategia por la evolución de la economía de los modelos de IA. | Empresa · [fuente](https://www.calcalistech.com/ctechnews/article/rjwumhukfx) |
| Amdocs · 2026-05-28 | `layoff-2026-214` | Globes relaciona la ronda actual con adaptar procesos a la era de IA, sin precisar cuáles. | Prensa · [fuente](https://en.globes.co.il/en/article-amdocs-to-lay-off-3000-employees-1001544263) |
| FanDuel · 2026-06-05 | `layoff-2026-202` | Trabajadores despedidos mencionan mayor énfasis en IA entre las razones que atribuyen al recorte. | Trabajadores · [fuente](https://frontofficesports.com/fanduel-is-latest-gambling-company-to-cut-jobs/) |
| Hailo · 2026-06-08 | `layoff-2026-199` | La empresa conecta el recorte con un mayor foco en Physical AI y un cambio de distribución. | Empresa · [fuente](https://www.calcalistech.com/ctechnews/article/3hmpcioxj) |
| Elastic · 2026-06-24 | `layoff-2026-176` | El CEO relaciona equipos más pequeños y menos niveles con IA y automatización. | Empresa · [fuente](https://www.elastic.co/blog/ceo-ash-kulkarni-announcement-to-elastic-employees) |

### El anuncio que mantenemos diferente: Verily

| Anuncio | Lectura del tracker | Decisión y motivo |
|---|---|---|
| Verily · 2026-06-09 · `layoff-2026-197` | Cierre del programa de dispositivos y reasignación hacia IA. | Esa explicación describe un cierre anunciado en agosto de 2025. Nuestro registro recoge el aviso de 58 puestos de junio de 2026. No recuperamos evidencia que establezca que es la ejecución de aquel mismo plan; por eso no trasladamos esa razón. |

Es una diferencia de alcance pendiente de evidencia que conecte ambos eventos, **no una conclusión de que la IA no influyó**. Se conserva [la fuente de la entrada de 2026](https://www.bizjournals.com/sanfrancisco/news/2026/06/09/sfbt-digest-tuesday-salesforce-layoffs-ucsf-fine.html), la cobertura alternativa y la noticia de 2025 en el [cruce completo](comparison.csv).

### Tres diferencias de unidad de análisis

| Registro del tracker | Qué describe | Por qué queda fuera de nuestros anuncios |
|---|---|---|
| Oracle · 2026-06-23 · `layoff-2026-180` | Descenso neto anual de plantilla de 21.000 personas. | No es un anuncio nuevo de 21.000 despidos. El vínculo empresarial con IA no asigna toda la variación neta a ese motivo. |
| Dell · 2026-03-16 · `layoff-2026-071` | Descenso neto de plantilla durante el ejercicio fiscal. | Combina movimientos de personal y restricciones de contratación; no es una sola ronda de marzo. |
| Multiverse · 2026-01-05 · `layoff-2026-001` | Salidas de un período anterior informadas en enero. | La fecha de publicación no convierte esas salidas en un anuncio nuevo de 2026. |

Se conservan en el JSON y en [los registros excluidos de la exportación analítica](../../data/normalized/excluded_records.csv). Esta tabla explica las tres exclusiones **dentro del listado de IA**; no es una conciliación completa de los 231 y 228 registros de ambos universos.

### Coincidimos en la etiqueta, pero no afirmamos haber verificado todos sus detalles

Estos 11 anuncios **ya forman parte de las 91 coincidencias**. Conservamos la atribución general de IA de Layoffs.fyi; no asignamos por esa sola etiqueta un mecanismo específico de sustitución o productividad. Sus fichas identifican al tracker como fuente y guardan las limitaciones de la revisión.

| Anuncio | ID |
|---|---|
| Amazon · 2026-01-28 | `layoff-2026-026` |
| Clari · 2026-02-12 | `layoff-2026-041` |
| SSense · 2026-03-05 | `layoff-2026-064` |
| Snowflake · 2026-03-19 | `layoff-2026-074` |
| Meta · 2026-04-02 | `layoff-2026-091` |
| Shopify · 2026-05-04 | `layoff-2026-121` |
| Paytm · 2026-06-09 | `layoff-2026-196` |
| Salesforce · 2026-06-09 | `layoff-2026-198` |
| Shopee · 2026-06-10 | `layoff-2026-193` |
| ServiceNow · 2026-06-11 | `layoff-2026-192` |
| Culture Amp · 2026-06-26 | `layoff-2026-171` |

En los otros ocho desacuerdos resueltos —Meta en enero y marzo, DraftKings, Ticketmaster, One Identity, LinkedIn, Credit Karma y ZoomInfo— incorporamos una fuente adicional o contexto del plan. Las decisiones y enlaces están en [comparison.csv](comparison.csv). Una declaración que niega sustitución no borra automáticamente una atribución de inversión o rediseño con IA.

## Cómo se cambia una clasificación

1. Identificar la misma empresa, ronda y alcance; una noticia posterior puede describir un evento distinto.
2. Conservar la etiqueta del tracker salvo evidencia que justifique la diferencia. Una fuente inaccesible no es una refutación.
3. Incorporar atribuciones adicionales con su fuente y autoría, aunque no estén en el tracker.
4. Registrar el motivo, la evidencia y el antes/después; regenerar el cruce, los análisis y el notebook.

El cruce es una comparación de clasificaciones que comparten una fuente de partida, **no una validación independiente de Layoffs.fyi**. Las revisiones y sus resultados anteriores se conservan para que cualquier cambio sea auditable.

## Reproducibilidad

[Seguimiento de evidencia y cierre del 29 de septiembre](evidence-followup-2026-09-28.md).

`compare.py` reproduce el cruce desde el snapshot público y los registros canónicos. `consistency-review.json` conserva la decisión actual para cada ficha. `baseline-summary.json` y `pre-baseline-summary.json` son resultados históricos anteriores a las dos revisiones; no son resultados vigentes. `review_consistency.py` y `align_baseline.py` son aplicaciones de una sola vez, con auditorías antes/después en `coverage/`. La cadena se valida con `scripts/validate_causes.py`.

El snapshot procede de `https://layoffs-fyi.onrender.com/api/ai-layoffs-stats`. La fecha de actualización de la API no acredita la fecha de revisión de cada noticia. Se concilian dos diferencias de un día (ZoomInfo y GitLab). El cruce no reconstruye el 78% histórico ni es una tabla de confusión de poblaciones idénticas.
