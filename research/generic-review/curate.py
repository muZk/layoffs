"""Manual, source-specific follow-up of all 46 generic-only announcements."""
import json,csv,copy,collections
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
b=P/'baseline.json'
if not b.exists():b.write_bytes((ROOT/'2026-categorized.json').read_bytes())
B=json.loads(b.read_text());D=copy.deepcopy(B);R={int(r['record_id'].split('-')[-1]):r for r in D};ids=[n for n,r in R.items() if r['cause_status']=='generic'];assert len(ids)==46
# Findings refer to this announcement, not the company's general AI use or other rounds.
notes={
11:'La declaración vincula la estructura con las necesidades del negocio; no identifica duplicidades, procesos ni áreas abandonadas. La salida a bolsa no demuestra una causa del recorte.',
12:'Eurofound conserva el anuncio, pero el enlace al comunicado original ahora redirige a la portada. La estrategia posterior de modelos especializados no basta para atribuir ese giro a los puestos eliminados en enero.',
23:'La empresa identifica dos unidades sujetas a revisión interna, pero no detalla qué cambia en sus procesos. Los ingresos récord son contexto, no el mecanismo.',
28:'El comunicado original y la cobertura adicional mantienen agilidad y rapidez de decisión. No identifican niveles eliminados ni tareas redistribuidas; los conflictos con aerolíneas no se convierten en causa por proximidad.',
35:'La declaración recuperada en GeekWire solo habla de prioridades a largo plazo. La compra por fondos y el recorte de octubre corresponden a contexto y otra ronda.',
36:'El aviso describe puestos que no generan ingresos en Global Customer Operations. Identificar el área y contabilizar indemnizaciones o deterioros de oficinas no demuestra un mecanismo de ahorro ni una consolidación específica.',
40:'Puck atribuye el recorte de febrero a alcanzar rentabilidad; se conserva como atribución periodística de reducción de costos. La empresa, por separado, habla de agilidad. Solo se recuperó la parte pública del artículo de Puck.',
49:'La empresa mantiene una explicación de prioridades. Un analista calcula ahorros posibles; calcular el efecto salarial del recorte no establece su motivo. Los usos de IA citados no se vinculan directamente a los puestos de esta ronda.',
60:'La cobertura confirma una revisión organizacional. El cierre de Blue Jay ocurrió antes y no se identifica de forma suficiente qué despidos de marzo responden a él. Tampoco se traslada la explicación de otras rondas de Amazon.',
64:'El aviso cita razones económicas. La insolvencia y la caída de ventas están documentadas como contexto, pero no se recuperó una atribución suficientemente específica para estos puestos.',
69:'La respuesta a BetaKit mantiene mercado y prioridades. No identifica un contrato perdido, una caída de demanda medida ni una línea de producto que se abandone.',
70:'La declaración empresarial confirma eficiencia; el vínculo con IA procede de una fuente anónima. Las republicaciones del mismo despacho no aportan un mecanismo independiente.',
74:'La fuente original de Business Insider no se recuperó íntegramente. Hay resúmenes y afirmaciones secundarias sobre automatización de documentación, pero no se verificó una fuente original que las vincule al recorte. Se mantiene la explicación general.',
78:'El testimonio sobre un equipo de soporte aporta funciones afectadas, pero no dice que el producto se cierre. El plan plurianual de optimización no se asigna automáticamente a cada puesto de marzo.',
80:'La declaración empresarial habla de reorganizar equipos para alcanzar sus objetivos. El gasto en IA y el recorte posterior de mayo no especifican el mecanismo de esta ronda.',
86:'El correo de marzo habla de reorganización. El informe anual vincula IA con un plan más amplio, sin asignar el recorte de marzo. No se convierte ese contexto en mecanismo del evento.',
91:'La declaración de reorganización es general. El aviso local puede solaparse con marzo; no se traslada el motivo de otra ronda ni se supone un evento independiente.',
94:'La fuente original recoge una versión anónima de reorganización y cambio de foco. Otras opiniones anónimas hablan de problemas de gestión, pero no aportan un mecanismo contrastable para este anuncio.',
95:'El mensaje del CEO anuncia una organización más pequeña y centrada en IA sin describir tareas o procesos. La entrevista posterior sobre eliminar RR. HH. no permite situar esa decisión dentro de esta ronda de abril.',
102:'La empresa vincula ajustes con acuerdos y clientes futuros. El periodista plantea dos posibilidades —alineación tras la venta y madurez tecnológica— sin establecer cuál explica el recorte.',
103:'El responsable de Eventbrite vincula la reducción del equipo previo a la compra con el modelo posterior e incorporación de personal de Bending Spoons para desarrollo. Se registra integración tras adquisición; no sustitución por IA ni duplicidades no declaradas.',
106:'La respuesta actual sigue siendo general. La disciplina de costos citada corresponde a julio de 2025; no se traslada a abril de 2026.',
111:'El comunicado de abril conserva cambios de mercado e IA. La cobertura menciona deslocalización dentro de la transformación más amplia, pero no identifica qué parte de los 950 puestos se traslada. Los foros anónimos no resuelven ese alcance.',
117:'La declaración de GeoComply describe adaptación y eficiencia con IA sin nombrar tareas sustituidas o un flujo de trabajo concreto. La lista de competidores no demuestra pérdida de demanda.',
120:'CTech atribuye explícitamente el movimiento a destinar más recursos a IA y desarrollo. La empresa confirma ajustes de estructura y asignación de recursos alrededor de sus productos de IA y contratación en esas áreas. Se registra reasignación de inversión, no sustitución.',
141:'Se conserva la declaración reproducida por Propmodo. No se pudo acceder al artículo original de Crain’s Cleveland; la afirmación de mayor escalabilidad no identifica tareas ni una relación medida entre producción y plantilla.',
147:'La declaración original en hebreo confirma preparación para la era de IA y rehúsa detallar puestos específicos. La automatización ofrecida a clientes por el producto no demuestra automatización del trabajo interno.',
149:'La empresa habla de planificación regular; una fuente anónima menciona trasladar personal hacia áreas de crecimiento sin precisar cuáles. Se conserva por separado la negación anónima del reemplazo por IA.',
152:'El correo reproducido y la declaración confirman una transición AI-native. Los artículos que describen grandes equipos manuales sustituidos no aportan una base primaria recuperada para ese detalle; no se adopta como mecanismo.',
168:'SAS nombra destinos de recursos —nube, ventas y producto—, pero no concreta qué actividad se reduce o qué presupuesto se transfiere. Su inversión anterior en IA no explica por sí sola esta ronda.',
169:'Los testimonios públicos identifican una reorganización de marketing. La empresa no respondió a la publicación; no se especifican equipos fusionados o funciones eliminadas.',
172:'El portavoz confirma que la IA cambia inversiones y composición del equipo. No identifica tareas, herramientas, ratios de productividad ni transferencias concretas de presupuesto.',
178:'La revisión de roles se explica por eficiencia y necesidades del negocio. No se publican funciones o cambios concretos; la atribución de que no es IA procede de información periodística, no de una nueva declaración empresarial.',
182:'La revisión posterior a la adquisición concluye que una organización menor será más flexible. No describe integración de equipos del comprador, duplicidades ni productos abandonados; adquirir la empresa no basta para clasificar integración.',
184:'Se recuperó el mensaje original del CEO: anuncia formación y herramientas de IA, pero no describe qué tareas o estructura pasan a otro modelo. Mejor acceso no equivale a mayor detalle causal.',
191:'La declaración menciona foco, decisiones y entrega de producto. Identifica el área Offering, pero no describe capas suprimidas. El lanzamiento simultáneo de agentes de IA es contexto.',
193:'La cobertura distingue expresamente entre el recorte y una conexión con IA que sigue incierta. El área de QA afectada no demuestra que sus tareas se automatizaran.',
200:'El correo remite a un town hall posterior para explicar la estrategia. No se recuperó una comunicación pública de esa reunión que detalle el motivo de los puestos eliminados.',
201:'Eficiencia es la atribución del titular de CTech; el cuerpo no aporta una declaración ni un mecanismo. La adquisición de Commonplace y el producto de IA son contexto.',
202:'La empresa describe agilidad; trabajadores señalan IA, competencia e incertidumbre sin un mecanismo específico. El cierre de FanDuel TV pertenece a otra actividad/ronda y no se asigna a todo este anuncio.',
206:'La empresa declara cambios en cómo trabaja con IA, pero no especifica qué proceso, tareas o responsabilidades cambian. La fórmula de flujos más rápidos sigue siendo general.',
208:'El 10-Q confirma el recorte del 1 de junio y repite eficiencia y prioridades. Los gastos de reestructuración describen el costo del despido, no qué cambio operativo lo motiva.',
214:'Globes vincula la ronda actual con reducir jerarquías y adaptar procesos a la era de IA. Se registra consolidación organizacional y una atribución genérica de IA a la prensa; la división de GenAI y las declaraciones de inversión citadas después son de 2025.',
217:'CRN recoge a un responsable de soporte que atribuye su despido a la cancelación de su proyecto. Se registra un cambio de actividad limitado a ese testimonio; no se generaliza a los 77 puestos ni se adopta la conjetura de un socio comercial.',
220:'El fundador nombra desarrollo y operaciones como ámbitos de adopción AI-first, pero no describe el cambio en tareas o dotación. El producto de gobernanza de datos no demuestra sustitución interna.',
228:'El comunicado y el informe trimestral permiten confirmar el recorte. La unificación de actividades y los activos del informe no se presentan como razones de los despidos; no se infiere insolvencia a partir del precio del token.'}
assert set(notes)==set(ids)
extra={12:['https://aleph-alpha.com/aleph-alpha-aligns-its-organization-with-strategic-priorities/','https://www.startbase.com/news/aleph-alpha-baut-rund-50-stellen-ab/'],28:['https://skift.com/2026/01/29/online-travel-agency-kiwi-lays-off-staff-in-latest-round-of-cuts/'],40:['https://puck.news/glossier-layoffs-signal-brand-reset/'],60:['https://www.moneycontrol.com/technology/amazon-cuts-over-100-jobs-in-robotics-division-as-it-shifts-warehouse-automation-strategy-article-13851339.html'],70:['https://www.cnnbrasil.com.br/economia/money/negocios/stone-demite-cerca-de-3-dos-funcionarios-e-elimina-vagas-de-tecnologia/'],74:['https://cncbnews.com/article/2026/03/snowflake-makes-cuts-as-part-of-targeted-adjustments-to-the-companys-strategy','https://www.kore1.com/snowflake-layoffs-2026/'],94:['https://www.glassdoor.com/Reviews/Employee-Review-Welltech-E7450280-RVW103391266.htm'],95:['https://www.paymentsdive.com/news/bolt-layoffs-ai-30-percent-breslow-valuation-drop/817040/'],103:['https://www.eventbrite.com/blog/whats-next-at-eventbrite/','https://www.iqmagazine.com/2026/04/eventbrite-makes-layoffs-following-bending-spoons-acquisition/'],111:['https://finance.yahoo.com/markets/stocks/articles/ukg-formerly-ultimate-software-lays-205200750.html'],117:['https://sbcamericas.com/2026/04/17/geocomply-job-cuts-global-workforce/'],152:['https://www.moneycontrol.com/news/trends/some-of-our-colleagues-indian-origin-ceo-announces-fresh-layoffs-at-3-45-billion-startup-13921433.html'],184:['https://www.linkedin.com/posts/piniyakuel_the-ai-era-is-changing-what-it-takes-to-build-activity-7472616123805405185-p-j_'],191:['https://thenextweb.com/news/pleo-layoffs-ai-agents-finance'],208:['https://www.sec.gov/Archives/edgar/data/1056696/000119312526327591/manh-20260630.htm'],214:['https://en.globes.co.il/en/article-amdocs-to-lay-off-3000-employees-1001544263'],228:['https://algorand.co/hubfs/Algorand%20Transparency%20Report%20Q1-2026.pdf']}
questions={n:'¿Qué proceso, actividad o criterio conecta la explicación publicada con estos puestos concretos?' for n in ids}
for n in [70,95,111,117,141,147,152,172,184,202,206,220]:questions[n]='¿Qué tareas cambian con IA y cómo modifica eso la necesidad de personal en esta ronda?'
questions.update({12:'¿Qué detalle contenía el comunicado original y qué áreas concretas perdieron recursos?',40:'¿Qué ahorro buscaba la dirección y qué parte corresponde al recorte de febrero?',74:'¿Quién asume la documentación y existe evidencia original que vincule esos puestos con automatización?',103:'¿Qué trabajo asume el equipo del comprador y qué capacidades deja de realizar el equipo anterior?',120:'¿Cuánto presupuesto se transfiere a IA y qué actividades dejan de recibirlo?',214:'¿Cuántas capas se eliminan y qué responsabilidades cambian?',217:'¿Qué proyecto se canceló y a cuántos de los 77 puestos afecta esa decisión?'})
def add(n,k,summary,url,attribution='company_stated',scope='event',specificity='concrete',replace=None,access='full'):
 r=R[n]
 if replace:
  r['causes'].remove(replace);del r['cause_details'][replace]
 r['causes'].append(k);r['cause_details'][k]=dict(summary=summary,source_url=url,attribution=attribution,scope=scope,specificity=specificity,evidence_access=access)
 if url not in r['review']['sources']:r['review']['sources'].append(url)
add(40,'cost_cutting','Puck attributes the February reduction to management seeking profitability. This is the publication’s causal account, separate from the company’s general agility explanation; no savings amount is established.',extra[40][0],'press_reported',access='partial')
add(103,'m_and_a','The new lead links a reduction of the pre-acquisition workforce with the post-acquisition operating model and incoming Bending Spoons product-development staff. This supports acquisition integration, without asserting duplicate roles or AI substitution.',extra[103][0],replace='organizational_realignment')
add(120,'ai_investment_reallocation','CTech reports that these cuts redirect resources toward AI and product development; the company statement links organizational and resource changes to AI-driven products while continuing to recruit in product, engineering and AI. No amount is assigned to the transfer.','https://www.calcalistech.com/ctechnews/article/b1ioncnpzl','press_reported',replace='strategic_priorities')
add(214,'organizational_consolidation','Globes attributes the May round to a strategy that includes a less hierarchical organization. It does not quantify layers or assign individual positions.',extra[214][0],'press_reported',replace='organizational_realignment')
add(214,'ai_transition','Globes also frames the current strategy around adapting work processes to the AI era, without specifying those processes. The separate GenAI division and investment statements later in the article refer to 2025 and are not transferred to this round.',extra[214][0],'press_reported',specificity='generic')
add(217,'strategic_pivot','CRN reports a support manager’s account that cancellation of his project led to his layoff. This is a worker-reported explanation for part of the event, not a reason established for all 77 positions.','https://www.crn.com/news/storage/2026/netapp-layoffs-will-impact-77-in-california-amid-strategic-realignment','worker_reported',scope='reported_worker_subset')
# The resource-allocation claim is now represented in causes, not duplicated as background.
R[120]['context']=[c for c in R[120]['context'] if c['kind']!='ai_product_strategy']
ledger=[]
for n in ids:
 r=R[n];concrete=any(d['specificity']=='concrete' for d in r['cause_details'].values());r['cause_status']='specified' if concrete else 'generic'
 outcome='mechanism_recovered' if concrete else 'investigation_limited' if n in [12,74,141] else 'published_reason_remains_general'
 sources=list(dict.fromkeys(r['review']['sources']+extra.get(n,[])))
 r['generic_review']=dict(review_date='2026-09-17',outcome=outcome,note_es=notes[n],open_question_es=questions[n],sources=sources,search_scope='Individual reread of event sources and search by company, announcement date and stated rationale; targeted primary-document checks where a relevant lead was found.')
 if concrete:
  r['reason']=' '.join(d['summary'] for d in r['cause_details'].values())
  r['review']['note']='Generic-explanation follow-up: concrete attributed detail recovered; see cause_details for speaker, event/subset scope and access limits. Existing count and overlap caveats remain.'
  r['explanation_review']['outcome']='concrete';r['explanation_review']['note']='Further source review identifies a concrete attributed mechanism; this is not independent causal verification.'
 ledger.append(dict(record_id=r['record_id'],company=r['company'],date=r['date'],**r['generic_review'],causes=r['causes'],details=r['cause_details']))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
save(P/'review.json',ledger);save(ROOT/'report/generic-review.json',ledger);save(ROOT/'2026-categorized.json',D)
save(ROOT/'coverage/generic-followup-2026-09-17.json',dict(reviewed='2026-09-17',method='Source-specific follow-up of all 46 generic-only announcements. Access limitations are separate from specificity; concrete accounts retain attribution and scope.',events=[dict(before=b,after=a) for b,a in zip(B,D) if b!=a]))
with (ROOT/'2026-categorized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in D for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in D)
for filename in ['explanation-review.json','explanation-recheck.json']:
 p=ROOT/'report'/filename;old=json.loads(p.read_text());byid={r['record_id']:r for r in D}
 for item in old:
  r=byid[item['record_id']];item.update(causes=r['causes'],details=r['cause_details'],outcome=r['explanation_review']['outcome'])
  if 'generic_review' in r:
   item['subsequent_review']=r['generic_review'];item['note']=r['generic_review']['note_es'];item['sources']=r['generic_review']['sources']
 save(p,old)
print(collections.Counter(x['outcome'] for x in ledger))
