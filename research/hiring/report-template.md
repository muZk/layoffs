# ¿Las empresas que vinculan sus recortes con IA habían crecido más?

*Investigación exploratoria · 17 de septiembre de 2026*

**El grupo vinculado con IA creció más en 2019–2022, pero no en 2022–2025.** La expansión previa de plantilla aparece tanto en empresas con explicaciones vinculadas a IA como en empresas cuyos anuncios ofrecen otras explicaciones.

Cruzamos las causas de los anuncios con historiales de plantilla. Recuperamos pares utilizables para **71 empresas en 2022–2025** y **35 en 2019–2022**, de las 217 empresas de la colección. La comparación se basa principalmente en una compilación secundaria, con comprobaciones parciales en documentos originales. Es evidencia exploratoria: las cifras aún no están armonizadas por adquisiciones, tipo de trabajador ni sector.

[Explorar los anuncios](explorar.html) · [Datos y fuentes en CSV](hiring-research.csv) · [Datos completos y comprobaciones en JSON](hiring-research.json)

## Qué encontramos

Mediana del cambio porcentual de la plantilla reportada. Cada empresa pesa una vez, independientemente del número de anuncios o puestos afectados.

<!--RESULTS-->

**«IA registrada» significa que al menos un anuncio del semestre tiene una razón vinculada con IA atribuida en las fuentes**, incluida la transición hacia IA sin mayor detalle. Se utiliza el mismo criterio que en el artículo y el explorador. No basta con que la empresa venda IA o la mencione como contexto. «Solo otras causas» incluye las demás razones sin un vínculo atribuido con IA; no prueba ausencia de IA. Quienes no tienen una explicación clasificable forman un grupo separado.

La clasificación conserva quién hace la afirmación. Por ejemplo, el vínculo de Salesforce en febrero procede de un analista externo. Amdocs entra en el grupo de IA por la transición atribuida en la cobertura, aunque el papel concreto de la IA siga sin precisarse. Los grupos comparan explicaciones publicadas, no efectos demostrados.

![Distribución del crecimiento de plantilla por grupo y período. Cada punto es una empresa y los rombos marcan las medianas.](assets/hiring-distribution.svg)

*Las figuras conservan el inglés. El eje utiliza una escala logarítmica de la razón entre plantillas para mostrar expansiones y contracciones sin ocultar las empresas más pequeñas detrás de los valores extremos. [Abrir la figura](assets/hiring-distribution.svg).* 

Entre 2019 y 2022, **6 de las 15 empresas con IA registrada habían al menos duplicado su plantilla**, frente a **4 de las 18 con otras causas**. Es una diferencia descriptiva que merece atención, pero procede de un subconjunto pequeño y desigual. Angi, por ejemplo, figura en el grupo de IA aunque su plantilla reportada había disminuido en ese período.

Entre 2022 y 2025, **12 de las 28 empresas con IA registrada ya habían reducido su plantilla neta**. También habían disminuido 14 de las 38 con otras causas. No hay una única trayectoria de expansión continua hasta el anuncio de 2026.

## Cuánto depende del período y de las empresas incluidas

<!--SENSITIVITY-->

Al limitar la comparación a observaciones de diciembre, el grupo de IA presenta una mediana negativa y el de otras razones una positiva. Eso no demuestra que el calendario fiscal explique los despidos; **al restringir las fechas también cambia la composición del grupo**. Entre las mismas empresas observables en ambos períodos, las medianas de crecimiento reciente son aproximadamente 3,5% y 5,2%.

Las exclusiones por operaciones societarias utilizan solo las operaciones documentadas en esta revisión. No equivalen a un ajuste del crecimiento orgánico ni a una revisión exhaustiva de todas las adquisiciones. Las comprobaciones completas, incluidos tamaños de grupo, están en la descarga JSON.

La lectura respaldada es limitada: algunas comparaciones muestran mayor expansión previa en el grupo de IA, pero estas cifras no sostienen una caracterización general de ese grupo como «las empresas que sobrecontrataron».

## Más plantilla no significa necesariamente exceso de contratación

Los resultados del negocio cambian la interpretación. Estos cuatro casos ilustran esa diferencia; no son una muestra con la que estimar una relación para toda la colección.

| Empresa | Plantilla, 2019–2022 | Medida del negocio, 2019–2022 |
|---|---:|---:|
| Block | ≈ +224% | Beneficio bruto: ≈ +217% |
| Cloudflare | ≈ +153% | Ingresos: ≈ +240% |
| Meta | ≈ +92% | Ingresos: ≈ +65% |
| Shopify | ≈ +132% | Ingresos: ≈ +255% |

![Comparación de crecimiento de plantilla y una medida del negocio en cuatro empresas.](assets/hiring-business.svg)

*Variaciones calculadas a partir de cifras reportadas y redondeadas. Shopify incluye contratistas; su base de 2019 se reporta como más de 5.000. Block usa beneficio bruto; las demás filas, ingresos nominales. [Abrir la figura](assets/hiring-business.svg).* 

En Block, la expansión de plantilla y la del beneficio bruto fueron de un orden parecido. En Cloudflare, los ingresos aumentaron más que el personal. En Meta ocurrió lo contrario. Ninguna de esas comparaciones mide por sí sola cuántas personas necesitaba la empresa: influyen las adquisiciones, los precios, la mezcla de productos y las inversiones que todavía no generaban ingresos.

Shopify ofrece un contraste especialmente útil: sus ingresos crecieron más que su plantilla entre esos dos cierres, y aun así su CEO reconoció una apuesta equivocada por la persistencia del auge del comercio electrónico al anunciar recortes en julio de 2022. Un cociente simple entre ingresos y empleados tampoco resuelve la pregunta.

Fuentes financieras: Block [2019](https://www.sec.gov/Archives/edgar/data/1512673/000119312520050074/d888202dex991.htm) y [2022](https://investors.block.xyz/files/doc_financials/2022/q4/Block_Shareholder-Letter-4Q22.pdf); Cloudflare [2019](https://cloudflare.net/files/doc_financials/2019/q4/NET-Q419-Earnings-Press-Release.pdf) y [2022](https://www.cloudflare.com/en-gb/press/press-releases/2023/cloudflare-announces-fourth-quarter-and-fiscal-year-2022-financial-results/); Meta [2019](https://investor.atmeta.com/investor-news/press-release-details/2020/Facebook-Reports-Fourth-Quarter-and-Full-Year-2019-Results/default.aspx) y [2022](https://www.sec.gov/Archives/edgar/data/1326801/000132680123000013/meta-20221231.htm); Shopify [2019](https://www.shopify.com/news/shopify-announces-fourth-quarter-and-full-year-2019-financial-results) y [2022](https://www.shopify.com/news/shopify-announces-fourth-quarter-and-full-year-2022-financial-results). Las fuentes de plantilla aparecen en el registro de empresas.

## Sí encontramos reconocimientos anteriores, con fecha

| Empresa | Anuncio al que corresponde | Qué reconoció la dirección |
|---|---|---|
| [Shopify](https://www.shopify.com/news/changes-to-shopify-s-team) | Julio de 2022 | Amplió el equipo apostando por una aceleración duradera del comercio electrónico que no se materializó. |
| [Meta](https://about.fb.com/news/2022/11/mark-zuckerberg-layoff-message-to-employees/) | Noviembre de 2022 | Aumentó la inversión esperando que persistiera el auge de la actividad digital; Zuckerberg reconoció el error de previsión. |
| [Salesforce](https://d18rn0p25nwr6d.cloudfront.net/CIK-0001108524/6460bc13-bdbb-4bd4-a6f4-f7919b884f6b.pdf) | Enero de 2023 | Benioff afirmó explícitamente que habían contratado demasiadas personas durante la aceleración de ingresos de la pandemia. |

Son ejemplos de evidencia directa sobre las explicaciones de la dirección, no un recuento exhaustivo de empresas que reconocieron sobrecontratación. **No se transfieren como causas a los anuncios de 2026.** Lo investigable ahora es si esos anuncios corrigen el mismo exceso, afectan otras funciones o responden a decisiones nuevas.

## Problemas encontrados en los datos de plantilla

**Una fecha incorrecta puede cambiar la historia.** La compilación de MicroVision asigna 350 empleados a diciembre de 2022. El [informe original](https://www.sec.gov/Archives/edgar/data/65770/000119312523056723/d461483d10k.htm) sitúa esa cifra el 24 de febrero de 2023, ya incluyendo empleados incorporados con Ibeo. Excluimos ese caso de los cálculos. También corregimos el día de la observación de Salesforce de enero de 2019 según su [10-K](https://www.sec.gov/Archives/edgar/data/1108524/000110852419000009/crmq4fy1910-k.htm).

**«Empleados» no siempre mide lo mismo.** Shopify incluye contratistas; ASML reporta equivalentes a jornada completa con personal temporal; la serie de Spotify utiliza promedios anuales. Se mantienen señalados en la comparación amplia y se excluyen en una comprobación de sensibilidad. En Amazon y MercadoLibre, la plantilla total también incluye operaciones logísticas: no representa necesariamente las funciones afectadas por un recorte tecnológico.

**Comprar una empresa aumenta la plantilla sin contratar a todas esas personas.** Registramos ejemplos como Afterpay en Block, Mailchimp y Credit Karma en Intuit, Slack en Salesforce y Splunk en Cisco. También hay ventas de unidades, como Egencia en Expedia y el negocio logístico de Shopify. No contamos con un ajuste de empleados incorporados o transferidos para toda la muestra. La descarga identifica las operaciones, sus fechas y sus fuentes; ausencia de una anotación no significa ausencia de adquisiciones.

## Método y cobertura

La colección de 228 anuncios contiene **217 etiquetas de empresa**: 72 con alguna explicación vinculada a IA, 122 con solo otras razones y 23 sin explicación clasificable. No fusionamos subsidiarias con sus matrices ni sustituimos su plantilla por la del grupo. Tampoco garantizamos independencia entre empresas del mismo grupo corporativo.

Buscamos historiales para **88 empresas con una correspondencia identificada con informes de una entidad cotizada o anteriormente cotizada**, sin limitar la búsqueda a la etiqueta bursátil incompleta del dataset. Recuperamos observaciones numéricas para 84. Las otras 129 etiquetas no se incorporaron a esa recopilación de series públicas: eso no demuestra que sus datos sean inaccesibles. Las empresas privadas y las subsidiarias quedan infrarrepresentadas.

| Grupo en los anuncios | Empresas del conjunto | Con par 2019–2022 | Con par 2022–2025 |
|---|---:|---:|---:|
| IA registrada | 72 | 15 | 28 |
| Solo otras causas | 122 | 18 | 38 |
| Sin explicación clasificable | 23 | 2 | 5 |
| Total | 217 | 35 | 71 |

La base amplia procede de las tablas de plantilla de **Stock Analysis**, que declara recopilar cifras de documentos regulatorios y relaciones con inversionistas. Cada observación enlaza su fuente. Las adiciones y comprobaciones primarias se guardan por separado; no presentamos la compilación completa como verificada contra cada documento original. Las cifras tras acceso restringido se dejan sin recuperar y no se imputan.

Para cada año calendario tomamos la última observación numérica disponible dentro de ese año, salvo las correcciones documentadas. Los cierres fiscales pueden caer en meses diferentes; por eso mostramos las fechas y la comprobación limitada a diciembre. Los cambios son **netos de plantilla**, no contrataciones brutas ni despidos acumulados. Una fecha de cierre tampoco coincide necesariamente con el máximo de plantilla o con el día anterior al anuncio de 2026.

El cálculo por empresa es `(plantilla final / plantilla inicial − 1) × 100`. Resumimos con medianas, sin ponderar por tamaño. No calculamos un porcentaje de despidos causado por sobrecontratación ni trasladamos estos resultados a todas las empresas. La selección por disponibilidad, las diferencias sectoriales, las operaciones societarias y la medición desigual de las causas impiden esa extrapolación. Para estudiar el riesgo de despedir haría falta además un grupo de empresas que no anunció recortes.

<!--LEDGER-->

El CSV y el JSON incluyen las **217 empresas**, también las que no entran en la comparación, con su estado de cobertura. El registro desplegable muestra las 74 que tienen algún par utilizable; los tamaños de cada comparación son menores porque requieren años concretos.

## Qué pregunta merece seguirse

Más que buscar un umbral universal de «sobrecontratación», conviene preguntar: **¿qué parte del crecimiento de personal respondió a una expectativa de negocio que después no se cumplió, y qué funciones se están reduciendo ahora?**

Para esa pregunta ya hay evidencia histórica en casos concretos. Para explicar las diferencias entre los anuncios de 2026 falta extender las comprobaciones primarias, reconstruir los cambios por adquisiciones y medir actividad del negocio y empleo de las mismas unidades. El análisis disponible deja una observación defendible: las trayectorias de expansión y contracción se superponen entre grupos, y el crecimiento previo por sí solo no distingue de forma estable las explicaciones de IA.
