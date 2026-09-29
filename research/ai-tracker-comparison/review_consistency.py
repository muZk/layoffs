"""Apply individually documented AI consistency corrections; retain a before/after audit."""
import json,csv,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
AUDIT=ROOT/'coverage/ai-consistency-2026-09-28.json'
if AUDIT.exists(): raise SystemExit('Review already applied; do not replay against modified data.')
B=json.loads((ROOT/'2026-categorized.json').read_text());D=copy.deepcopy(B);by={int(r['record_id'].split('-')[-1]):r for r in D}
# Each decision links a particular reduction to AI; none asserts that displacement was verified.
fixes={
4:('ai_investment_reallocation','company_stated','Company explicitly reallocates investment from slower-adopting segments toward robotics and Physical AI and links the staffing adjustment to that reallocation.',None),
19:('ai_transition','press_reported','Reporting links the partnerships restructuring to a stronger agentic-commerce focus. This is a product-strategy transition, not evidence of employee task automation.',None),
79:('ai_investment_reallocation','company_stated','In its response about this reorganization and closure, the company links the changes to reallocating talent and resources toward priorities including AI-enabled services.',None),
90:('ai_investment_reallocation','company_stated','The CEO links the reduction to redirecting the business and resources toward the Starwood and Exaion initiatives, identified in the same report as AI and HPC infrastructure.',None),
97:('ai_transition','company_stated','The CEO connects this restructuring to adapting the company for customers building and using AI agents; no internal task replacement is established.',None),
116:('ai_transition','company_stated','The acting CEO attributes the reduction to aligning the company with AI developments and an expanded creative offering; this does not establish automation of employee jobs.',None),
119:('ai_transition','press_reported','Reporting links this restructuring to accelerating an AI-first organizational and product roadmap; no internal productivity gain is demonstrated.',None),
150:('ai_investment_reallocation','press_reported','The report explicitly identifies investment in AI-powered products as a motivating force for the reduction. It does not establish automation of the affected employees.', 'https://www.theblock.co/news/business/2026-05-14-crypto-data-firm-dune-cuts-25-of-staff-citing-ai-efficiencies-401322'),
155:('ai_investment_reallocation','company_stated','The employee letter links the announced reduction to reallocating resources toward three strategic priorities, including scaling an AI-native platform. This mixed plan does not assign every eliminated role to AI; the separate CEO denial is retained.','https://investors.intuit.com/sec-filings/all-sec-filings/content/0000896878-26-000024/fy26q3-ex9902.htm'),
158:('ai_transition','reported_inference','CTech interprets this round in relation to AI-era role redundancy and AI-related pressures. The company declined comment; the report does not identify the tasks replaced.',None),
174:('ai_investment_reallocation','company_stated','The CEO links the reduction to concentrating people and resources on security, trading, stablecoins, settlement and AI-powered infrastructure. AI is one destination within a mixed resource-allocation decision.','https://www.otcmarkets.com/filing/html?guid=L8F-kao64zjBB3h&id=19564086'),
175:('ai_transition','company_stated','The CEO connects team reductions and restructuring to the speed and security needs of AI-driven software development. This is adaptation to the AI market, not a claim that AI performs eliminated jobs.',None),
194:('ai_work_redesign','company_stated','The CEO links the India closure to returning operational work to the US and reorganizing into smaller AI-native teams; AI contribution and affected headcount are not quantified.',None),
199:('ai_transition','company_stated','The announcement links the reduction to a sharper focus on Physical AI, robotics and drones, alongside a changed distribution model; selling AI alone is not the inclusion criterion.',None),
211:('ai_transition','press_reported','Anonymous sources attribute the restructuring to increased AI automation, without specifying automated tasks. The cofounder disputes enrollment decline and the reported headcount; this is not his confirmation of AI displacement.',None),
212:('ai_investment_reallocation','company_stated','The CEO links the reduction to concentrating the company on its more profitable AI and data operations. The destination of resources supports AI investment reallocation, not employee replacement.',None),
}
for n,(code,attr,summary,url) in fixes.items():
 r=by[n];url=url or r['review']['sources'][0]
 r['causes'].append(code);r['cause_details'][code]=dict(summary=summary,attribution=attr,scope='announced_plan' if n==155 else 'event',source_url=url,specificity='generic' if code=='ai_transition' else 'concrete')
 r['review']['sources']=list(dict.fromkeys(r['review']['sources']+[url]));r['review']['date']='2026-09-28'
 r['review']['note']=summary+' Other count, scope and overlap caveats remain applicable.'
 r['reason']=' '.join(d['summary'] for d in r['cause_details'].values())
 r['context']=[c for c in r['context'] if c['kind']!='ai_product_strategy']
 r['cause_status']='specified' if any(d['specificity']=='concrete' for d in r['cause_details'].values()) else 'generic'
 r['consistency_review']=dict(date='2026-09-28',decision='add_attributed_ai_reason',note=summary,source_url=url)
# Veritone's prior prose conflated May's broader initiative with the June plan.
r=by[195];r['reason']='June plan targets operating-cost reductions. The later filing mentions AI tools in a broader initiative announced in May; it does not explicitly allocate the June reduction to that AI initiative. The 111 estimate uses an older workforce denominator.';r['review']['note']=r['reason'];r['review']['date']='2026-09-28'
r['consistency_review']=dict(date='2026-09-28',decision='retain_non_ai_correct_scope_note',note=r['reason'],source_url=r['review']['sources'][1])
notes={
26:('event_link_not_established','El comunicado de enero explica niveles y burocracia. El tracker añade una interpretación de IA sin fuente adicional en esa entrada.'),
9:('event_link_not_established','La explicación específica de Reality Labs apunta de VR hacia wearables. La inversión general en superinteligencia no asigna este recorte a IA.'),
149:('event_link_not_established','La declaración del anuncio es planificación y prioridades; la interpretación del tracker sobre funciones sustituidas no está sustentada en nuestra evidencia.'),
80:('event_link_not_established','Reorganización de equipos en marzo; no trasladamos la atribución de la ronda de mayo.'),
144:('event_link_not_established','La carta identifica traslado, clientes grandes y reinversión en plataforma; no especifica IA como destino de este ahorro.'),
196:('event_link_not_established','La fuente separa salidas por evaluación de desempeño de contratación nueva en IA, producto y tecnología.'),
135:('event_link_not_established','La fuente identifica capas y consolidación; no conecta suficientemente el anterior anuncio de estrategia IA con esta ronda.'),
64:('event_link_not_established','La notificación recuperada dice razones económicas; eliminar fotografía no demuestra que IA asuma su trabajo.'),
91:('event_link_not_established','El aviso local y la respuesta de Meta hablan de reorganización. Posible solapamiento; no trasladamos otras rondas.'),
210:('event_link_not_established','El plan matriz nombra esta filial para eliminar duplicidades. La reinversión IA global no se asigna específicamente a este aviso local; se conserva el posible solapamiento con Intuit.'),
49:('event_link_not_established','Prioridades empresariales en el anuncio; uso de IA y cálculos de ahorro en otro contexto no establecen la atribución para estos puestos.'),
193:('event_link_not_established','El cuerpo de la fuente deja explícitamente incierto el vínculo con IA pese al titular; no convertimos coincidencia en atribución.'),
41:('evidence_limited','La fuente completa no está recuperada. Un titular de fusión e inversión IA no valida la explicación detallada de automatización del tracker.'),
74:('evidence_limited','El original está restringido; no verificamos que IA reemplace el equipo de documentación de esta ronda.'),
171:('evidence_limited','Acceso parcial a esta ronda; una explicación de la ronda de 2024 no se transfiere a 2026.'),
198:('evidence_limited','Cobertura alternativa de WARN confirma salidas, pero no la explicación IA del original restringido.'),
197:('evidence_limited','Cobertura accesible confirma aviso de salidas, no el cierre de programa y redirección hacia IA afirmados por el tracker.'),
192:('evidence_limited','La fuente consultada confirma WARN; no fundamenta que los puestos se eliminen porque la plataforma los automatiza.'),
143:('evidence_limited','Extractos recuperados confirman traslado de desarrollo y soporte; falta acceso al relato completo para resolver el alcance de IA.'),
121:('evidence_limited','El reportaje de esta ronda sigue restringido. No trasladamos a mayo las razones del anuncio de enero.'),
110:('event_link_not_established','Taboola anuncia producto IA por separado; la fuente no vincula explícitamente ese producto con estos recortes.'),
112:('event_link_not_established','Quora reduce subsidios a Poe y busca autosuficiencia financiera. Ser un producto IA no demuestra inversión hacia IA, sustitución ni disrupción del mercado.'),
195:('event_link_not_established','El documento distingue la iniciativa amplia de mayo y el plan de junio. Se corrige nuestra prosa, manteniendo el límite de alcance.'),
}
ledger=[]
for b,r in zip(B,D):
 n=int(r['record_id'].split('-')[-1]);decision,note=notes.get(n,('existing_attribution_retained' if any(c.startswith('ai_') for c in r['causes']) else 'no_new_event_attribution','Se conserva la clasificación según el vínculo con el evento documentado en cause_details y review.'))
 if n in fixes:decision='added_ai_reason';note=fixes[n][2]
 ledger.append(dict(record_id=r['record_id'],company=r['company'],date=r['date'],decision=decision,note=note,source_review='fresh_targeted_reread' if n in fixes or n in [26,144,196,193,110,112,195,210] else 'existing_source_assessment_reassessed',sources=r['review']['sources'],before_causes=b['causes'],after_causes=r['causes']))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
save(AUDIT,dict(date='2026-09-28',method='Consistency screen of all 235 stored record assessments, with targeted source rereads; not a fresh retrieval of every source. Event-linked AI investment and general transitions count without proof of task replacement. Denials remain separate. Period measures remain excluded.',events=[dict(before=b,after=r) for b,r in zip(B,D) if b!=r]))
save(P/'consistency-review.json',ledger);save(ROOT/'2026-categorized.json',D)
with (ROOT/'2026-categorized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in D for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in D)
print('Added AI reasons:',len(fixes),'Other scope correction: Veritone; screened',len(ledger),'records')
