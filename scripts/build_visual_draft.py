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
assert [[len(v) for v in g.values()] for g in groups]==[[22,12],[40,27]]
colors=['#6741bd','#645d70'];author='By Nicolás Gómez from trabajoremoto.cl'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
maxval=max(v for group in groups for rows in group.values() for _,v in rows);upper=np.ceil(maxval/50)*50+20
for wi,window in enumerate(['2019–2022','2022–2025']):
 fig,ax=plt.subplots(figsize=(4.8,4.3));fig.patch.set_facecolor('#fbfafc');ax.set_facecolor('#fbfafc')
 for gi,(g,rows) in enumerate(groups[wi].items()):
  vals=[v for _,v in rows]; jitter=np.linspace(-.16,.16,len(vals));ax.scatter([gi+j for j in jitter],sorted(vals),s=36,color=colors[gi],alpha=.80,zorder=3)
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
assert (len(org_rows),org_ai,org_other)==(43,23,20)
labels.update({'org_ai':'Con alguna razón de IA registrada','org_other':'Sin una razón de IA registrada'})
org_examples=[('ASML','Cambiar la estructura de los equipos','Pasar de una organización matricial a equipos dedicados a productos y módulos; cambios en puestos de liderazgo.'),('Amazon','Reducir niveles y burocracia','El comunicado atribuye el recorte a simplificar la organización y mantiene contratación en áreas estratégicas.'),('Uber','Eliminar responsabilidades superpuestas','Reorganizar el área de personas para reducir duplicidades y fragmentación.'),('Zipcar','Concentrar operaciones','Consolidar operaciones de oficina en Nueva Jersey.')]
org_table='<div class="case-table">'
for name,change,detail in org_examples:
    source=next(r['url'] for r in org_rows if r['company_label']==name)
    org_table+=f'<div class="case org-case"><h4><a href="{html.escape(source)}">{name}</a></h4><div><strong>{change}</strong></div><div>{detail}</div></div>'
org_table+='</div>'
sections=[('¿Seguimos corrigiendo la sobrecontratación de pandemia?',figure('Crecimiento de plantilla: muestra disponible en cada período','<div class="panels">'+''.join(f'<img src="assets/visual-draft/hiring-{i}.svg" alt="Distribución del crecimiento de plantilla {w}; muestra disponible para este período">' for i,w in enumerate(['2019–2022','2022–2025']))+'</div>','Cada punto es una empresa; la línea negra marca la mediana. 2019–2022: 34 empresas (22 con razones de IA y 12 con otras razones). 2022–2025: 67 empresas (40 y 27). La composición cambia entre períodos: no es una trayectoria de las mismas empresas. Misma escala en ambos paneles. La comparación con las 31 empresas comunes se conserva en la sección de sensibilidad del notebook. Crecimiento no equivale a sobrecontratación; no se ajustan todas las adquisiciones.','contratacion')),
('¿Mi trabajo tiene que poder automatizarse para que la IA afecte a mi puesto?',figure('Seis categorías de vínculo con IA',bars(ai)+'<div class="examples"><p><strong>ZoomInfo</strong>Productividad y cambio del mercado</p><p><strong>Oracle</strong>Financiación de IA atribuida al plan de marzo</p><p><strong>Tailwind Labs</strong>Cambios en tráfico e ingresos atribuidos a IA</p></div>','113 asignaciones en 108 anuncios. Las categorías se solapan; cuentan explicaciones atribuidas, no puestos ni efectos verificados. Once vínculos generales proceden solo de la clasificación del tracker; no corroboramos por separado su mecanismo. Los tres casos ilustran vías distintas.','casos')+'<p class="chart-lead">Estas vías pueden formar parte de una decisión con varios motivos. En 80 de los 108 anuncios con IA también aparecen otras razones; 22 mencionan reducción de costos. Ahorro e IA pueden coexistir en la explicación del recorte, aunque esto no demuestra que los ahorros se hayan materializado.</p>'+figure('¿Qué otras razones acompañan a la IA?',bars(co),'Anuncios de enero–junio de 2026 con cada razón adicional. Las barras se solapan: un anuncio puede aparecer en varias. Se muestran todas las razones adicionales con al menos un caso.','razones-con-ia')),
('¿Qué cambia en la organización cuando se recorta plantilla?',figure('43 anuncios describen consolidación organizacional',bars([('org_ai',org_ai),('org_other',org_other)])+org_table,'Los dos grupos suman 43 anuncios y no se solapan. La categoría incluye cambios en equipos, niveles, duplicidades y sedes: no equivale a 43 recortes de managers. Los ejemplos son ilustrativos; no cuantifican subtipos. No tener una razón de IA registrada no demuestra ausencia de IA.','organizacion'))]

# Opening overview: compute all figures from the same announcement tables.
total=len(records)
reason_counts={r['record_id']:len({c['cause_code'] for c in reasons if c['record_id']==r['record_id']}) for r in records}
overview=[('Con alguna razón vinculada con IA',len(ai_ids)),('Solo otras razones registradas',sum(reason_counts[r['record_id']]>0 and r['record_id'] not in ai_ids for r in records)),('Sin explicación clasificable',sum(n==0 for n in reason_counts.values()))]
multi=sum(n>1 for n in reason_counts.values())
assert (total,[n for _,n in overview],multi)==(228,[108,98,22],108)
frequencies=sorted([(c,len({r['record_id'] for r in reasons if r['cause_code']==c})) for c in {r['cause_code'] for r in reasons}],key=lambda x:(-x[1],x[0]))
overview_bars='<div class="bars overview-bars">'+''.join(f'<div class="bar-row"><div class="bar-label"><span>{label}</span><strong>{n} <small>({str(round(100*n/total,1)).replace(".",",")}%)</small></strong></div><div class="track"><div style="width:{100*n/total}%"></div></div></div>' for label,n in overview)+'</div>'
opening='<div class="opening"><p class="intro-copy">Para entender qué hay detrás de los despidos en tech, analizamos <strong>228 anuncios de enero a junio de 2026</strong>, recopilados a partir de Layoffs.fyi y ampliados con comunicados, declaraciones y cobertura periodística.</p>'+figure('Una primera fotografía de los 228 anuncios',overview_bars,'Tres grupos sin solapamiento. Los porcentajes usan los 228 anuncios como base; cada barra completa representa el 100%. No tener una razón de IA registrada no demuestra ausencia de IA.','grupos')+figure('Las seis razones más frecuentes',bars(frequencies[:6]),f'Número de anuncios por razón. Se muestran las seis más frecuentes de {len(frequencies)} categorías. Las categorías se solapan: {multi} de los {total} anuncios incluyen más de una razón. Dos etiquetas pueden describir aspectos de una misma decisión; no son necesariamente motivos independientes.','razones')+'<p class="method-copy"><strong>Cómo lo analizamos.</strong> Partimos de la clasificación de IA de Layoffs.fyi, añadimos otras atribuciones documentadas y conservamos su procedencia. Las diferencias requieren una justificación concreta; no descartamos un vínculo por no recuperar una fuente. Contamos anuncios, no trabajadores afectados, y complementamos el análisis con datos históricos de plantilla cuando estaban disponibles. Las cifras describen esta colección y las explicaciones documentadas; no demuestran las causas reales de todos los despidos del sector. La evidencia se revisó hasta el 29 de septiembre de 2026. Los cálculos pueden reproducirse en el <a href="../notebooks/explorar_despidos.html">notebook</a>. <a href="#comparacion-tracker">Ver cómo ampliamos los datos del AI Layoffs Tracker</a>.</p><p class="intro-copy">De este análisis surgen tres temas: el crecimiento previo de las plantillas, las distintas vías de impacto de la IA y los cambios organizacionales que acompañan a los recortes.</p></div>'

opening=opening.replace('<h3>','<h2>').replace('</h3>','</h2>')
css='''@font-face{font-family:Jost;src:url(assets/Jost-VariableFont_wght.ttf)}*{box-sizing:border-box}body{margin:0;background:#fbfafc;color:#252333;font-family:Jost,system-ui,sans-serif}main{max-width:1040px;margin:auto;padding:48px 28px 90px}h1{font-size:clamp(34px,5vw,58px);line-height:1.1;letter-spacing:-.025em;max-width:850px;margin:0 0 20px}header>p{color:#645d70;font-size:16px}section{margin-top:85px;padding-top:25px;border-top:1px solid #dedbe5}h2{font-size:clamp(27px,3vw,38px);line-height:1.2;max-width:850px;margin:0 0 35px;text-wrap:balance}figure{margin:0}h3{font-size:22px;margin:0 0 25px;font-weight:600}.panels{display:grid;grid-template-columns:1fr 1fr;gap:20px}.panels img{width:100%;height:auto;display:block}figcaption,.author,.evidence{font-size:14px;line-height:1.5;color:#645d70}figcaption{max-width:78ch;margin-top:22px}.author{margin-top:20px}.evidence{display:inline-block;margin-top:8px}a{color:#6741bd;text-underline-offset:4px}a:focus-visible{outline:2px solid #6741bd;outline-offset:4px}.bars{max-width:760px}.bar-row{margin:20px 0}.bar-label{display:flex;justify-content:space-between;gap:20px;font-size:17px;margin-bottom:7px}.track{height:13px;background:#eee8f7}.track>div{height:100%;background:#6741bd}.chart-lead{font-size:21px}.examples{display:grid;grid-template-columns:repeat(3,1fr);gap:25px;margin-top:32px;border-top:1px solid #dedbe5}.examples p{font-size:16px;line-height:1.5}.examples strong{display:block;margin-bottom:5px}.case,.table-head{display:grid;grid-template-columns:.65fr 1.2fr 1.2fr 1.2fr;gap:20px;padding:20px 0;border-bottom:1px solid #dedbe5;font-size:16px;line-height:1.5}.table-head{font-weight:600}.org-case{grid-template-columns:.65fr 1.2fr 2.4fr}.case h4{margin:0}.mobile-label{display:none}::selection{background:#ddd0f4}@media(max-width:600px){main{padding:30px 20px 60px}.panels{grid-template-columns:1fr;gap:30px}section{margin-top:60px}.examples{grid-template-columns:1fr;gap:0}.table-head{display:none}.case,.org-case{grid-template-columns:1fr;gap:16px}.case h4{font-size:22px}.mobile-label{display:block;font-size:14px;color:#645d70;margin-bottom:3px}.bar-label{font-size:16px}h3{font-size:20px}}'''
css+=' .opening{margin-top:36px}.intro-copy,.method-copy{font-size:18px;line-height:1.65;max-width:72ch}.opening figure{margin:44px 0}.opening h2{max-width:32ch;font-size:22px;margin:0 0 25px;font-weight:600}.bar-label strong{white-space:nowrap;font-variant-numeric:tabular-nums}.bar-label small{font-size:14px;font-weight:400}.overview-bars .track{height:16px}.overview-bars .bar-row:nth-child(2) .track>div{background:#645d70}.overview-bars .bar-row:nth-child(3) .track>div{background:#aaa3b5}'
# Reuse the exact font asset shipped by the existing site.
import re
match=re.search(r'url\([\'\"]?([^\)\'\"]+)',(OUT/'report.css').read_text())
if match:css=css.replace('assets/Jost-VariableFont_wght.ttf',match[1])
# Methodological comparison; distinct from the three substantive findings.
import markdown
comparison_summary=json.loads((ROOT/'research/ai-tracker-comparison/summary.json').read_text())
comparison_labels={'both_ai':'Ambos registramos una razón de IA','tracker_only_ai':'Solo el tracker registra IA','ours_only_ai':'Solo nuestro análisis registra IA','excluded_period_measure':'Medidas de período excluidas de los anuncios'}
labels.update(comparison_labels)
comparison_chart=figure('Dónde coinciden y difieren las clasificaciones',bars([(k,comparison_summary['counts'][k]) for k in comparison_labels]),'Registros de enero–junio. Los cuatro grupos no se solapan. Se muestran los registros etiquetados con IA por al menos uno de los dos análisis, incluidas tres medidas de período fuera de nuestra población.','comparacion-tracker')
comparison_text=markdown.markdown((OUT/'tracker-comparison.md').read_text(),extensions=['tables'])
comparison_text=re.sub(r'<table>.*?</table>',lambda m:comparison_chart,comparison_text,flags=re.S)
comparison_section='<section class="comparison" id="comparacion-tracker">'+comparison_text+'</section>'
css+=' .comparison p,.comparison li{font-size:18px;line-height:1.65;max-width:72ch}.comparison figure{margin:36px 0}.comparison ul{padding-left:24px}.comparison li{margin:16px 0}'
page='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Despidos, IA y contratación · Borrador visual</title><style>'+css+'</style><main><header><h1>Despidos, IA y contratación</h1><p>Borrador visual · Enero–junio de 2026 · Evidencia revisada el 28 de septiembre</p></header>'+opening+''.join(f'<section><h2>{title}</h2>{content}</section>' for title,content in sections)+comparison_section+'</main></html>'
(OUT/'borrador-visual.html').write_text(page)
(AS/'data.json').write_text(json.dumps({'overview':{'total':total,'groups':overview,'multiple_reasons':multi,'reason_frequencies':frequencies},'period_company_groups':dict(zip(['2019_2022','2022_2025'],groups)),'other_reasons_with_ai':co,'ai_reasons':ai,'organizational_consolidation':org_rows,'tracker_comparison':comparison_summary},ensure_ascii=False,indent=2))
print('Built report/borrador-visual.html')
