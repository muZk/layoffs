"""Generate the section-and-chart draft from current observations and attributed reasons."""
from pathlib import Path
import json, sqlite3, html, statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'report'; AS=OUT/'assets/visual-draft';AS.mkdir(exist_ok=True)
db=sqlite3.connect(ROOT/'data/normalized/layoffs.sqlite');db.row_factory=sqlite3.Row
records=[dict(r) for r in db.execute('select * from announcements')]
reasons=[dict(r) for r in db.execute('select * from announcement_causes')]
ai_ids={r['record_id'] for r in reasons if r['cause_code'].startswith('ai_')}
company_reasons={r['company_label']:set() for r in records}
for r in records:company_reasons[r['company_label']].update(x['cause_code'] for x in reasons if x['record_id']==r['record_id'])
history=json.loads((ROOT/'research/hiring/company-history.json').read_text());groups=[{'IA':[],'Otras razones':[]} for _ in range(2)]
for r in history:
 codes=company_reasons[r['company']]; group='IA' if any(c.startswith('ai_') for c in codes) else 'Otras razones' if codes else None
 if group is None:continue
 endpoints={y:max([o for o in r['observations'] if o['date'].startswith(str(y))],key=lambda o:o['date'],default=None) for y in [2019,2022,2025]}
 for wi,(a,b) in enumerate([(2019,2022),(2022,2025)]):
  if endpoints[a] is None or endpoints[b] is None or endpoints[a]['value']<=0:continue
  if any(f'{a}_{b}' in issue.get('exclude_windows',[]) for issue in r['quality_issues']):continue
  growth=100*(endpoints[b]['value']/endpoints[a]['value']-1)
  groups[wi][group].append((r['company'],growth))
assert [[len(v) for v in g.values()] for g in groups]==[[15,18],[28,38]]
colors=['#6741bd','#645d70'];author='By Nicolás Gómez from trabajoremoto.cl'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
maxval=max(v for group in groups for rows in group.values() for _,v in rows);upper=np.ceil(maxval/50)*50+20
for wi,window in enumerate(['2019–2022','2022–2025']):
 fig,ax=plt.subplots(figsize=(4.8,4.3));fig.patch.set_facecolor('#fbfafc');ax.set_facecolor('#fbfafc')
 for gi,(g,rows) in enumerate(groups[wi].items()):
  vals=[v for _,v in rows]; jitter=np.linspace(-.16,.16,len(vals));ax.scatter([gi+j for j in jitter],sorted(vals),s=36,color=colors[gi],alpha=.78,zorder=3)
  med=statistics.median(vals);ax.plot([gi-.28,gi+.28],[med,med],lw=2.5,color='#252333',zorder=4)
  ax.annotate(f'Mediana {med:+.1f}%'.replace('.',','),(gi,med),xytext=(0,12),textcoords='offset points',ha='center',fontsize=10,bbox=dict(facecolor='#fbfafc',edgecolor='none',pad=1.5))
 ax.set_xticks([0,1],[f'Con razones de IA\nn = {len(groups[wi]["IA"])}',f'Solo otras razones\nn = {len(groups[wi]["Otras razones"])}']);ax.set_xlim(-.6,1.6);ax.set_ylim(-100,upper);ax.axhline(0,color='#aaa3b5',lw=.8);ax.set_ylabel('Cambio de plantilla (%)');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
 fig.text(.06,.95,window,weight='bold',fontsize=16);fig.text(.06,.025,author,fontsize=8,color='#645d70');fig.subplots_adjust(left=.18,right=.96,bottom=.20,top=.83)
 fig.savefig(AS/f'hiring-{wi}.svg');fig.savefig(AS/f'hiring-{wi}.png',dpi=180);plt.close(fig)
labels={'cost_cutting':'Reducción de costos','organizational_consolidation':'Consolidación organizacional','strategic_pivot':'Cambio de producto o negocio','ai_productivity':'Productividad con IA','ai_investment_reallocation':'Inversión hacia IA','ai_transition':'Transición hacia IA, sin mayor detalle','ai_work_redesign':'Rediseño del trabajo con IA','ai_substitution':'Sustitución de tareas','ai_market_disruption':'Cambio del mercado por IA','operational_efficiency':'Eficiencia y agilidad','work_relocation':'Traslado del trabajo','unit_closure':'Cierre de unidad o sede','financial_distress':'Dificultades financieras','shutdown':'Cierre de la empresa','strategic_priorities':'Prioridades estratégicas','organizational_realignment':'Reorganización general','demand_decline':'Caída de la demanda','market_conditions':'Condiciones del mercado','m_and_a':'Integración tras adquisición','market_exit':'Salida de un mercado','performance_cull':'Evaluación de desempeño','lost_contract':'Pérdida de contrato','regulatory':'Regulación','ipo_prep':'Preparación de salida a bolsa'}
def count_rows(ai):
 codes={r['cause_code'] for r in reasons if r['cause_code'].startswith('ai_')==ai}
 return sorted([(c,len({r['record_id'] for r in reasons if r['cause_code']==c and r['record_id'] in ai_ids})) for c in codes],key=lambda x:(-x[1],x[0]))
def bars(rows):
 rows=[(c,n) for c,n in rows if n]; ceiling=max(n for c,n in rows)
 return '<div class="bars">'+''.join(f'<div class="bar-row"><div class="bar-label"><span>{html.escape(labels[c])}</span><strong>{n}</strong></div><div class="track"><div style="width:{n/ceiling*100}%"></div></div></div>' for c,n in rows)+'</div>'
def figure(title,body,note,anchor):return f'<figure><h3>{title}</h3>{body}<figcaption>{note}</figcaption><div class="author">{author}</div><a class="evidence" href="../notebooks/explorar_despidos.html#{anchor}">Ver cálculos y registros</a></figure>'
co=count_rows(False);ai=count_rows(True)
org_rows=[dict(r) for r in db.execute("SELECT a.record_id,a.company_label,a.has_ai_reason,c.summary,s.url FROM announcements a JOIN announcement_causes c USING(record_id) LEFT JOIN sources s ON s.source_id=c.source_id WHERE c.cause_code='organizational_consolidation'")]
org_ai=sum(r['has_ai_reason'] for r in org_rows);org_other=len(org_rows)-org_ai
assert (len(org_rows),org_ai,org_other)==(43,18,25)
labels.update({'org_ai':'Con alguna razón de IA registrada','org_other':'Sin una razón de IA registrada'})
org_examples=[('ASML','Cambiar la estructura de los equipos','Pasar de una organización matricial a equipos dedicados a productos y módulos; cambios en puestos de liderazgo.'),('Amazon','Reducir niveles y burocracia','El comunicado atribuye el recorte a simplificar la organización y mantiene contratación en áreas estratégicas.'),('Uber','Eliminar responsabilidades superpuestas','Reorganizar el área de personas para reducir duplicidades y fragmentación.'),('Zipcar','Concentrar operaciones','Consolidar operaciones de oficina en Nueva Jersey.')]
org_table='<div class="case-table">'
for name,change,detail in org_examples:
    source=next(r['url'] for r in org_rows if r['company_label']==name)
    org_table+=f'<div class="case org-case"><h4><a href="{html.escape(source)}">{name}</a></h4><div><strong>{change}</strong></div><div>{detail}</div></div>'
org_table+='</div>'
sections=[('¿Seguimos corrigiendo la sobrecontratación de pandemia?',figure('Crecimiento de plantilla: muestra disponible en cada período','<div class="panels">'+''.join(f'<img src="assets/visual-draft/hiring-{i}.svg" alt="Distribución del crecimiento de plantilla {w}; muestra disponible para este período">' for i,w in enumerate(['2019–2022','2022–2025']))+'</div>','Cada punto es una empresa; la línea negra marca la mediana. 2019–2022: 33 empresas (15 con razones de IA y 18 con otras razones). 2022–2025: 66 empresas (28 y 38). La composición cambia entre períodos: no es una trayectoria de las mismas empresas. Misma escala en ambos paneles. La comparación con las 30 empresas comunes se conserva en la sección de sensibilidad del notebook. Crecimiento no equivale a sobrecontratación; no se ajustan todas las adquisiciones.','contratacion')),
('¿Es IA o simplemente quieren ahorrar?',figure('¿Qué otras razones acompañan a la IA?','<p class="chart-lead"><strong>48 de 72</strong> anuncios con IA incluyen también otras razones.</p>'+bars(co),'Anuncios de enero–junio de 2026 con cada razón adicional. Las barras se solapan: un anuncio puede aparecer en varias. Se muestran todas las razones adicionales con al menos un caso.','razones-con-ia')),
('¿Mi trabajo tiene que poder automatizarse para que la IA afecte a mi puesto?',figure('Seis explicaciones distintas vinculadas con IA',bars(ai)+'<div class="examples"><p><strong>Block</strong>Productividad con equipos menores</p><p><strong>Atlassian</strong>Reinversión hacia IA y ventas</p><p><strong>Tailwind Labs</strong>Cambios en tráfico e ingresos atribuidos a IA</p></div>','76 asignaciones en 72 anuncios. Las categorías se solapan; cuentan explicaciones atribuidas, no puestos ni efectos verificados. Los tres casos ilustran vías distintas.','casos')),
('¿Qué cambia en la organización cuando se recorta plantilla?',figure('43 anuncios describen consolidación organizacional',bars([('org_ai',org_ai),('org_other',org_other)])+org_table,'Los dos grupos suman 43 anuncios y no se solapan. La categoría incluye cambios en equipos, niveles, duplicidades y sedes: no equivale a 43 recortes de managers. Los ejemplos son ilustrativos; no cuantifican subtipos. No tener una razón de IA registrada no demuestra ausencia de IA.','organizacion'))]

css='''@font-face{font-family:Jost;src:url(assets/Jost-VariableFont_wght.ttf)}*{box-sizing:border-box}body{margin:0;background:#fbfafc;color:#252333;font-family:Jost,system-ui,sans-serif}main{max-width:1040px;margin:auto;padding:48px 28px 90px}h1{font-size:clamp(34px,5vw,58px);line-height:1.1;letter-spacing:-.025em;max-width:850px;margin:0 0 20px}header>p{color:#645d70;font-size:16px}section{margin-top:85px;padding-top:25px;border-top:1px solid #dedbe5}h2{font-size:clamp(27px,3vw,38px);line-height:1.2;max-width:850px;margin:0 0 35px;text-wrap:balance}figure{margin:0}h3{font-size:22px;margin:0 0 25px;font-weight:600}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}.panels img{width:100%;height:auto;display:block}figcaption,.author,.evidence{font-size:14px;line-height:1.5;color:#645d70}figcaption{max-width:78ch;margin-top:22px}.author{margin-top:20px}.evidence{display:inline-block;margin-top:8px}a{color:#6741bd;text-underline-offset:4px}a:focus-visible{outline:2px solid #6741bd;outline-offset:4px}.bars{max-width:760px}.bar-row{margin:20px 0}.bar-label{display:flex;justify-content:space-between;gap:20px;font-size:17px;margin-bottom:7px}.track{height:13px;background:#eee8f7}.track>div{height:100%;background:#6741bd}.chart-lead{font-size:21px}.examples{display:grid;grid-template-columns:repeat(3,1fr);gap:25px;margin-top:32px;border-top:1px solid #dedbe5}.examples p{font-size:16px;line-height:1.5}.examples strong{display:block;margin-bottom:5px}.case,.table-head{display:grid;grid-template-columns:.65fr 1.2fr 1.2fr 1.2fr;gap:20px;padding:20px 0;border-bottom:1px solid #dedbe5;font-size:16px;line-height:1.5}.table-head{font-weight:600}.org-case{grid-template-columns:.65fr 1.2fr 2.4fr}.case h4{margin:0}.mobile-label{display:none}::selection{background:#ddd0f4}@media(max-width:600px){main{padding:30px 20px 60px}.panels{grid-template-columns:1fr;gap:30px}section{margin-top:60px}.examples{grid-template-columns:1fr;gap:0}.table-head{display:none}.case,.org-case{grid-template-columns:1fr;gap:16px}.case h4{font-size:22px}.mobile-label{display:block;font-size:14px;color:#645d70;margin-bottom:3px}.bar-label{font-size:16px}h3{font-size:20px}}'''
# Reuse the exact font asset shipped by the existing site.
import re
match=re.search(r'url\([\'\"]?([^\)\'\"]+)',(OUT/'report.css').read_text())
if match:css=css.replace('assets/Jost-VariableFont_wght.ttf',match[1])
page='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Despidos, IA y contratación · Borrador visual</title><style>'+css+'</style><main><header><h1>Despidos, IA y contratación</h1><p>Borrador visual · Enero–junio de 2026 · Evidencia revisada el 17 de septiembre</p></header>'+''.join(f'<section><h2>{title}</h2>{content}</section>' for title,content in sections)+'</main></html>'
(OUT/'borrador-visual.html').write_text(page)
(AS/'data.json').write_text(json.dumps({'period_company_groups':dict(zip(['2019_2022','2022_2025'],groups)),'other_reasons_with_ai':co,'ai_reasons':ai,'organizational_consolidation':org_rows},ensure_ascii=False,indent=2))
print('Built report/borrador-visual.html')
