# ¿Qué cuentan las empresas cuando recortan empleo?

*Cobertura general: 17 de septiembre de 2026 · Clasificaciones revisadas: 29 de septiembre de 2026*

228 anuncios de despidos, todas sus razones atribuidas y los patrones que aparecen al cruzarlas.

Cuando una empresa vincula un recorte con IA, el titular parece ofrecer una explicación completa. Pero puede estar hablando de equipos que producen con menos personas, dinero destinado a otros productos, tareas sustituidas o clientes que ya no necesitan el mismo servicio.

En esta colección, **108 de 228 anuncios tienen alguna explicación vinculada a IA**. En **80 de esos 108 —cerca de tres de cada cuatro— también se atribuye otra razón**, como ahorro, consolidación o eficiencia. La IA aparece con frecuencia dentro de una decisión con varios motivos.

Partimos de las etiquetas de IA de Layoffs.fyi y añadimos atribuciones documentadas. Once de los 108 vínculos se conservan por la clasificación del tracker, sin corroborar por separado su mecanismo. Esa coexistencia es el punto de partida. El análisis cuenta todas las razones atribuidas al anuncio, incluida una transición hacia IA sin mayor detalle. No distribuye puestos entre causas ni convierte las declaraciones de las fuentes en hechos causales demostrados.

Los recuentos y ejemplos tienen una consulta reproducible en el [notebook con código, resultados y fuentes](../notebooks/explorar_despidos.html). Los cálculos verifican lo registrado; no demuestran que las explicaciones atribuidas sean las causas reales.

Los tres hallazgos principales son las distintas trayectorias previas de plantilla, las vías por las que IA puede afectar al empleo y los cambios de organización descritos al recortar.

## Primero, ¿qué estamos contando?

Analizamos **228 registros de anuncios de enero a junio de 2026**. Partimos de [Layoffs.fyi](https://layoffs.fyi/2026-layoffs/) y contrastamos o ampliamos cada registro con otras fuentes. Hay una explicación clasificable en **206 anuncios**; los otros **22** permanecen en el conjunto y se muestran por separado.

La unidad es el anuncio, no la empresa ni el trabajador. Hay posibles solapamientos entre rondas de Expedia, Meta y Vimeo, además de Credit Karma dentro del plan de Intuit. Algunos planes se extienden más allá de junio. Esta colección no representa todos los despidos ni permite comparar meses como si la cobertura fuera uniforme.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#poblacion)

## Ahorro y cambios organizacionales encabezan las explicaciones

**Reducir costos aparece en 46 anuncios; consolidar equipos, niveles o sedes, en 43; y cambiar de producto o negocio, en 29.** Ahorro y consolidación encabezan el conjunto; el vínculo general con IA aparece en 34 anuncios, por delante del cambio de producto o negocio.

![Todas las razones atribuidas a los 228 anuncios.](assets/mechanisms.svg)

*Figura 1. Incluye todas las razones atribuidas, también reorganización general, eficiencia y transición hacia IA sin mayor detalle. Las barras cuentan anuncios y se solapan; sumarlas no produce un total de anuncios únicos.*

Las categorías conservan lo que dice cada fuente. Una reorganización sin más detalle se cuenta como tal; no se convierte por suposición en eliminación de duplicidades. Esto permite incluir el anuncio sin inventar la decisión que hay detrás.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#razones)

## Las explicaciones se superponen

**108 anuncios contienen más de una razón atribuida.** El cruce más frecuente es ahorro y consolidación organizacional, en 13 anuncios. También aparecen productividad con IA y ahorro, en 13, y dificultades financieras y cierre, en 9.

Un giro hacia productos de IA puede figurar como cambio de negocio y como inversión o transición hacia IA. Son descripciones que se solapan, no necesariamente motivos independientes.

![80 anuncios con IA y otra razón, 28 solo con razones de IA, 98 solo con otras razones y 22 sin explicación clasificable.](assets/overlap.svg)

*Figura 2. Estos cuatro grupos cuentan cada anuncio una sola vez. «Solo» describe las razones recogidas en las fuentes; no establece que fueran las únicas causas reales.*

La coexistencia también domina los anuncios vinculados con IA: **80 combinan IA con otra razón y 28 solo tienen razones de IA registradas**. Los 98 que únicamente contienen otras razones no prueban ausencia de IA. Los 22 sin una explicación clasificable tampoco se interpretan como «sin IA».

Estos son los cruces de IA más frecuentes; se incluyen todos los empates en el quinto puesto:

| Explicaciones que aparecen juntas | Anuncios |
|---|---:|
| Productividad con IA + Reducción de costos | 13 |
| Productividad con IA + Consolidación organizacional | 8 |
| Inversión hacia IA + Cambio de producto o negocio | 7 |
| Inversión hacia IA + Reducción de costos | 6 |
| Transición hacia IA + Cambio de producto o negocio | 6 |

Son coincidencias dentro de las explicaciones de un anuncio. No indican qué motivo pesó más ni demuestran que una combinación sea más frecuente en el conjunto de empresas que no despiden. La matriz permite abrir los registros de cada cruce.

![Matriz de todas las explicaciones ajenas a la IA y vinculadas con IA.](assets/matrix.svg)

*Figura 3. Cada cifra abre los anuncios correspondientes. Las filas y columnas se solapan; no deben sumarse como si fueran grupos independientes.*

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#cruces)

## La IA aparece en seis tipos de explicación

La transición hacia IA sin mecanismo precisado es la categoría de IA más frecuente, en **34 anuncios**. La productividad aparece en 25 anuncios; las demás categorías son la inversión hacia IA (25), el rediseño del trabajo (13), la sustitución de tareas (8) y los cambios del mercado por IA (8).

![Seis explicaciones vinculadas con IA en 108 anuncios.](assets/ai-mechanisms.svg)

*Figura 4. Las barras suman 113 asignaciones en 108 anuncios. Productboard, Lastminute, Rapyd, Zap Africa y ZoomInfo tienen dos explicaciones de IA cada uno.*

**Una expectativa de productividad aparece aproximadamente tres veces más que una atribución de sustitución de tareas: 25 frente a 8 anuncios.** Esto describe cómo se explican los recortes. No mide cuántas sustituciones ocurrieron ni si se cumplieron las mejoras prometidas.

Tampoco es un vínculo construido únicamente por comentaristas externos: **23 de las 25 atribuciones de productividad proceden de la empresa**, al igual que 19 de las 25 de inversión. Entre las 34 transiciones hacia IA sin mayor detalle, 14 son declaraciones empresariales. La procedencia de la explicación y su veracidad son cuestiones distintas.

Por ejemplo, el [CEO de Optimove](https://www.linkedin.com/posts/piniyakuel_the-ai-era-is-changing-what-it-takes-to-build-activity-7472616123805405185-p-j_) conecta el recorte del 10% con una orientación hacia IA y anuncia herramientas y formación. Se cuenta como transición hacia IA. Su mensaje no permite asignarlo a sustitución de tareas por automatización.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#atribuciones)

## Equipos más pequeños, menores costos

La productividad aparece en **25 anuncios**. Es la explicación de que la IA permite hacer más con una plantilla menor, o mantener la producción. Veintitrés de esas explicaciones se atribuyen a la empresa; una, a la prensa; y otra es una inferencia explícita.

La sustitución concreta aparece atribuida en ocho anuncios, incluido el caso de Salesforce interpretado por un analista externo. Usamos esa categoría cuando la fuente vincula la ejecución o eliminación de tareas mediante IA o automatización con los puestos afectados. Es una afirmación más específica que esperar que un equipo más pequeño sea más productivo. Su menor frecuencia no debe interpretarse como un censo de las sustituciones que realmente ocurrieron.

**La atribución también importa:** en Salesforce (febrero), un analista de Forrester interpreta los recortes como sustitución por IA. Ese registro se cuenta como inferencia externa, no como declaración de Salesforce ni como sustitución demostrada. Zencity tiene una explicación de eficiencia atribuida por el titular de CTech, sin una declaración de la empresa.

[La carta de Block a sus accionistas](https://www.sec.gov/Archives/edgar/data/1512673/000119312526076557/d108590dex991.htm) vincula una plantilla menor con la producción que permiten las herramientas de inteligencia. Eso respalda una atribución de productividad. No asigna cada puesto eliminado a una tarea automatizada concreta.

[El mensaje de Snap a sus empleados](https://newsroom.snap.com/organizational-changes-at-snap) relaciona equipos más pequeños con la productividad mediante IA y el ahorro de costos operativos. Es uno de los 13 registros en los que ambas explicaciones coexisten. Conviene registrar tanto el objetivo de ahorro como el medio propuesto para conseguirlo.

LSports ofrece una variante especialmente útil. Su CEO menciona el trabajo apoyado por IA y el aumento de los costos laborales. Afirma que los recortes habrían sido necesarios sin IA, pero que el crecimiento habría sido más lento. En esa explicación, la IA cambia lo que puede producir la plantilla restante. No se presenta como la única razón para reducir personal. [Entrevista a la empresa en Geektime](https://www.geektime.co.il/l-sports-lays-off-40-employees-in-israel/).

Para un equipo de ingeniería, las preguntas son prácticas. ¿La capacidad de entrega mejoró antes de la decisión o se espera que mejore después? ¿Disminuyó el trabajo pendiente o quedó en manos de menos personas? ¿Las mediciones incluyen fiabilidad, carga de soporte y trabajo que hay que rehacer, o solo volumen de producción?

Los datos no responden a esas preguntas de forma consistente. El hallazgo es que la productividad se usa repetidamente para explicar equipos más pequeños. Un siguiente paso de investigación sería contrastar las mejoras declaradas con lo que esos equipos entregaron después del recorte.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#casos)

## Cambiar el destino del dinero

Catorce registros vinculan explícitamente los recortes con la inversión en IA. Sus destinos incluyen productos, capacidades y puestos de trabajo, además de infraestructura. Describirlos todos como «recortes para financiar infraestructura de IA» borraría esa distinción.

[El CEO de Atlassian](https://www.atlassian.com/blog/company-news/atlassian-team-update-march-2026) vincula la reducción con financiar inversiones en IA y ventas a grandes empresas, al tiempo que mejora la rentabilidad. La IA es uno de los destinos de una decisión más amplia sobre cómo distribuir recursos.

[El mensaje de Autodesk a sus empleados](https://adsknews.autodesk.com/en/news/012226-employee-message/) describe la culminación de una transformación comercial y la inversión en IA, plataforma y capacidades de nube para distintas industrias. Tanto el cambio organizacional como la reinversión aparecen en el registro.

[La explicación de GitLab sobre su reestructuración](https://about.gitlab.com/blog/gitlab-act-2/) también vincula el ahorro con su estrategia de productos basados en agentes, junto con menos niveles jerárquicos y una reducción de los países donde emplea personal. Se registra con el alcance del plan anunciado. No establece cuánto de una salida concreta financió IA.

Estos casos sugieren una línea de investigación distinta de la sustitución de tareas: **¿qué decide comprar, desarrollar o contratar la empresa a continuación?** Una reducción en un área puede coexistir con expansión en otra. Para evaluar ese cambio necesitaríamos conocer las contrataciones, el gasto y la composición de puestos posteriores, además del tamaño del anuncio de despidos.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#casos)

## Cuando la IA cambia el negocio

En ZoomInfo, la misma explicación ejecutiva reúne productividad de desarrollo mediante IA y presión sobre el negocio de licencias. La empresa describe menor necesidad de desarrollo de interfaces y un giro hacia el consumo de datos. Por eso el anuncio registra tanto productividad como cambio del mercado, junto con ahorro, traslado y cambio de negocio. No asignamos sus 600 puestos a una sola razón. [Transcripción de resultados del 11 de mayo](https://www.fool.com/earnings/call-transcripts/2026/05/11/zoominfo-gtm-q1-2026-earnings-call-transcript/).

Siete registros describen cómo la IA altera el mercado, la distribución o la viabilidad de un producto. Cuatro también describen un cambio estratégico. Es otra vía por la que la IA puede entrar en la explicación de un despido, aunque no se hayan automatizado las tareas de los trabajadores afectados.

En [Tailwind Labs](https://www.businessinsider.com/tailwind-engineer-layoffs-ai-github-2026-1), el fundador relaciona la IA con una caída del tráfico web y de las conversiones de pago, y luego vincula la caída de ingresos con limitaciones para sostener la nómina futura. La cadena que propone pasa por la distribución y la economía del negocio.

[El CEO de Productboard](https://www.linkedin.com/pulse/productboard-going-ai-only-heres-what-means-hubert-palan-h1ozc/) describe cómo los agentes de IA restan valor a la gestión de procesos que cubría el producto anterior, un giro hacia Spark y un equipo más pequeño que trabaja con IA. Ese registro contiene mecanismos distintos de disrupción del mercado y productividad interna, además del cambio de producto.

Yupp ofrece un ejemplo de cierre: sus fundadores relacionan la menor utilidad del servicio con el rápido avance de la IA. [Cobertura de TechCrunch](https://techcrunch.com/2026/03/31/yupp-ai-shuts-down-33m-a16z-crypto-chris-dixon/).

Vender un producto de IA no basta para entrar en esta categoría. Tampoco anunciar un giro hacia la IA. La fuente debe conectar un cambio del mercado o de la viabilidad del negocio con la decisión sobre el personal. De lo contrario, casi cualquier actualización estratégica de una empresa de software podría convertirse en evidencia de despidos causados por IA.

La pregunta abierta es si la IA está cambiando la cantidad de trabajo necesaria, el valor que los clientes le atribuyen o la vía por la que la empresa llega a ellos. Cada cambio exige respuestas diferentes de un equipo de ingeniería.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#casos)

## ¿Qué se niega al negar un vínculo con la IA?

Seis registros del primer semestre contienen una negación atribuida a la empresa sobre un vínculo con la IA. Cuatro también incluyen una explicación de inversión en IA. Leer qué niega exactamente cada declaración resuelve buena parte de la aparente contradicción.

| Empresa | Qué niega la declaración registrada | Otra explicación en el registro |
|---|---|---|
| Autodesk | Sustituir personas por IA | Cambios comerciales e inversión que incluye IA |
| Atlassian | La sustitución directa por IA | Rentabilidad e inversión en IA y ventas a grandes empresas |
| GitLab | Que el objetivo sea optimizar mediante IA o reducir costos | Reinversión, menos niveles jerárquicos y cambios en los lugares de contratación |
| Epic Games | Una causa relacionada con la IA en términos amplios | Menor participación de usuarios y gastos superiores a los ingresos |
| Intuit | Una causa relacionada con la IA en términos amplios | Simplificación y reasignación hacia tres prioridades, incluida una plataforma de IA |
| Uber | Una causa relacionada con la IA en términos amplios | Eliminar responsabilidades superpuestas y equipos fragmentados |

*Fuentes: los mensajes de las empresas enlazados arriba; [Epic Games](https://www.epicgames.com/site/en-US/news/todays-layoffs); [la declaración del CEO de Intuit, recogida por India Today](https://www.indiatoday.in/jobs/story/software-maker-intuit-to-cut-3000-jobs-ceo-says-layoff-has-nothing-to-do-with-ai-tchc-2914758-2026-05-21). [La declaración de Uber, recogida por CNBC](https://www.cnbc.com/2026/06/03/uber-layoffs-people-division-ai.html). Las negaciones de LinkedIn y Trend Micro se atribuyen a fuentes anónimas y quedan fuera de este recuento de declaraciones de empresas.*

Negar la sustitución no equivale a negar toda conexión posible con la IA. Puede coexistir con destinar dinero a productos de IA. Por eso cada negación debe leerse junto con su objeto: sustitución, productividad, inversión o una conexión con la IA en términos amplios.

¿Ocurre más entre empresas que cotizan en bolsa? La evidencia es insuficiente para responder. Cinco de estos seis registros tienen la etiqueta Post-IPO; la etapa de Epic figura como desconocida en la lista de Layoffs.fyi. Las declaraciones no se recabaron de manera uniforme, la ausencia de una negación no implica aceptación y una matriz cotizada y una filial adquirida son unidades distintas. Es una pregunta de investigación, no una comparación respaldada entre tipos de empresa.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#negaciones)

## Oracle muestra por qué importa el alcance

Oracle permite distinguir dos vínculos. La [cobertura del plan de marzo](https://www.investing.com/news/stock-market-news/oracle-plans-thousands-of-job-cuts-as-data-center-costs-rise-bloomberg-news-reports-4544997) relaciona los recortes previstos con financiar infraestructura de IA. Registramos esa atribución periodística con alcance de plan; vincularla con la ejecución del 31 de marzo es una inferencia documental explícita.

Además, el [comunicado oficial del 10 de marzo](https://www.oracle.com/news/announcement/q3fy26-earnings-release-2026-03-10/) describe equipos de desarrollo menores gracias a generación de código con IA. Esa declaración se conserva como contexto del plan: no asigna todos los puestos de la ronda a productividad ni a sustitución.

El registro de marzo incluye reorganización general e inversión hacia IA atribuida a la prensa. La disminución neta anual de 21.000 personas permanece separada y excluida del recuento de anuncios: combina contrataciones y salidas, y no equivale a un anuncio nuevo de despidos.

[Ver evidencia y alcance en el notebook](../notebooks/explorar_despidos.html#oracle)


## Las dificultades financieras aparecen sobre todo junto a cierres

**9 de los 10 anuncios que citan dificultades financieras también incluyen el cierre de la empresa.** A la inversa, 9 de los 14 cierres tienen esa explicación. Es una concentración en esta colección, no una estimación del riesgo de cierre de una empresa con problemas financieros.

Las fuentes describen situaciones distintas: en [Covrzy](https://inc42.com/buzz/antler-backed-covrzy-shuts-down-due-to-cash-crunch/), el fundador relata intentos fallidos de financiación o adquisición; en [Rec Room](https://techcrunch.com/2026/03/31/social-gaming-platform-rec-room-once-valued-at-3-5b-is-shutting-down/), la empresa explica que no consigue operar de forma rentable. El caso restante del grupo financiero es Tailwind Labs: la fuente conecta la caída de ingresos con las dificultades para sostener la nómina, sin anunciar el cierre de la empresa.

Este cruce distingue una situación empresarial útil para el lector: **recortar para continuar operando y despedir al cerrar no son la misma decisión**. La etiqueta «despidos» reúne ambas.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#cierres)

## ¿Qué trabajo se recorta?

Identificamos funciones afectadas en **62 de los 228 anuncios**. Ingeniería e I+D aparece en 32, producto y diseño en 20, y marketing en 13. Las categorías se solapan porque un anuncio puede afectar a varias funciones.

Entre esos registros, ingeniería aparece junto con una explicación de IA en 15 anuncios; producto y diseño, en 11; y marketing, en 9. Esos recuentos no permiten ordenar profesiones por riesgo: no conocemos el total de trabajadores expuestos ni contamos con cobertura uniforme de las funciones.

El límite principal es anterior a cualquier comparación: **en 80 de los 108 anuncios vinculados con IA no identificamos funciones concretas afectadas**. Saber que una empresa invoca IA no basta para saber qué trabajo desaparece. [Explorar funciones × explicaciones](explorar.html#affected-functions).

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#funciones)

## Los vacíos también son parte de los hallazgos

En **22 anuncios no tenemos una explicación clasificable**: 11 no ofrecen una razón en el material recuperado, 9 tienen evidencia insuficiente y 2 carecen de una fuente causal recuperada. Se mantienen en el denominador de 228.

![11 anuncios sin explicación identificada, 9 con evidencia limitada y 2 sin fuente causal recuperada.](assets/evidence-gaps.svg)

*Figura 5. Son límites de la información recuperada. No demuestran que esos anuncios carezcan de una razón ni de un vínculo con IA.*

El aviso de **ADP** informa de las salidas sin explicar el motivo. En **Xero (febrero)**, la [vista previa de BusinessDesk](https://businessdesk.co.nz/article/markets/xero-restructures-with-250-jobs-on-the-line) describe una reestructuración propuesta, pero no recuperamos el artículo completo ni una explicación suficiente por otra vía. En **Dayforce**, la lista remite a un memo interno no disponible para revisión. Son problemas de evidencia diferentes, conservados en cada ficha.

También hay preguntas que estos cruces no responden. La industria figura como desconocida en 66 anuncios, de modo que una clasificación de sectores ocultaría una parte considerable del conjunto. Las negaciones sobre IA no se recopilaron de forma uniforme, por lo que no permiten medir si cotizadas y privadas se comportan de manera distinta. Los anuncios tampoco contienen una medición consistente de la productividad posterior a los recortes.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#vacios)

## El crecimiento previo no sigue una sola trayectoria

Al cruzar las razones de los anuncios con los historiales de plantilla, la mediana de crecimiento de **2019–2022** es **+88,2% en el grupo vinculado con IA y +22,0% en el grupo con otras razones**. Los grupos tienen 22 y 12 empresas, respectivamente.

En **2022–2025**, las medianas son cercanas: **+6,7% con IA y +3,7% con otras razones**, sobre 40 y 27 empresas. Quince de esas 40 empresas vinculadas con IA ya habían reducido su plantilla neta durante ese período. Una sola historia de expansión continua antes del recorte no describe al grupo.

Estas comparaciones no demuestran sobrecontratación: cambian las empresas observables, no se han ajustado todas las adquisiciones y una plantilla mayor puede acompañar a un negocio mayor. La [investigación de contratación](contratacion.html) presenta las fuentes, distribuciones y comprobaciones de sensibilidad. Utiliza todas las razones atribuidas, igual que este artículo, pero cuenta cada empresa una vez.

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#contratacion)

## Registro completo y metodología

El artículo y el explorador cuentan todas las razones atribuidas a los mismos **228 anuncios**. Se conservan por separado las observaciones de contexto, las negaciones, quién formula cada explicación y su alcance. El nivel de detalle permanece en los datos para revisar las clasificaciones; no divide los hallazgos en dos poblaciones.

Las razones generales no se recodificaron exhaustivamente junto a todas las explicaciones que ya describían una decisión específica. Sus recuentos y cruces reflejan lo registrado y pueden omitir formulaciones adicionales de las fuentes.

Los recuentos se generan a partir de los registros. De los 228 anuncios, 212 tienen fuentes revisadas, 14 evidencia parcial y 2 fuentes no recuperadas. Ese estado no equivale a una corroboración independiente de cada afirmación o cifra de personal.

[Explorar todos los registros](explorar.html) · [Recuentos y cruces del análisis](analysis.json) · [Datos JSON](records.json) · [CSV](records.csv) · [Metodología](methodology.md) · [Revisión individual de fuentes](explorar.html#revision-de-las-explicaciones-generales)

[Ver cálculos y evidencia en el notebook](../notebooks/explorar_despidos.html#comprobaciones)

<!--TRACKER-COMPARISON-->
## ¿Cómo ampliamos los datos de Layoffs.fyi?

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

[Reproducir el cruce y revisar la procedencia en el notebook](../notebooks/explorar_despidos.html#comparacion-tracker) · [Descargar registros y decisiones](../research/ai-tracker-comparison/comparison.csv).
<!--/TRACKER-COMPARISON-->
